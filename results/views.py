from typing import Any
from django.views import generic
import json
from django.http import JsonResponse

from divisions.models import States, LGA, Ward, PollingUnit
from .models import AnnouncedPuResults
from elections.models import Party



class ResultsView(generic.TemplateView):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['states'] = States.objects.all()
        return context



class PollingUnitResultsView(ResultsView):
    template_name = 'results/polling_unit_results.html'

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        data: dict = json.loads(request.body.decode())
        polling_unit_id = data.get('polling-unit')

        if not polling_unit_id:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': 'Polling unit id is required'
                },
                status=400
            )
        
        polling_unit = PollingUnit.objects.filter(polling_unit_id=polling_unit_id).first()
        if not polling_unit:
            return JsonResponse(
            data={
                'status': 'error',
                'detail': f'Polling unit with polling unit id {polling_unit_id} does not exist',
            },
            status=404
        )

        polling_unit_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=polling_unit.uniqueid)
        results = polling_unit_results.values('party_abbreviation', 'party_score')
        return JsonResponse(
            data={
                'status': 'success',
                'detail': 'Polling unit results retrieved successfully',
                'data': {
                    "results": list(results)
                }
            },
            status=200
        )


DIVISION_NAME_TO_MODEL = {
    'state': States,
    'lga': LGA,
    'ward': Ward,
    'polling_unit': PollingUnit
}


def fetch_next_division_by_previous_division_view(request, *args, **kwargs):
    if request.method != 'POST':
        return JsonResponse(
            data={
                'status': 'error',
                'detail': 'Only POST requests are allowed'
            },
            status=405
        )
    
    data: dict = json.loads(request.body.decode())
    previous: dict = data.get('previous')
    nxt: dict = data.get('next')
    if not (previous and nxt):
        return JsonResponse(
            data={
                'status': 'error',
                'detail': f'Invalid request data!'
            },
            status=400
        )

    nxt_name = nxt.get('name').replace('-', '_')
    NextDivisionModel = DIVISION_NAME_TO_MODEL.get(nxt_name, None)

    if not NextDivisionModel:
        return JsonResponse(
            data={
                'status': 'error',
                'detail': f'Invalid division: {nxt_name}.'
            },
            status=400
        )
    
    previous_name = previous.get('name').replace('-', '_')
    previous_value = previous.get('value')
    filter_kwargs = {
        f'{previous_name}_id': str(previous_value)
    }


    divisions = NextDivisionModel.objects.filter(**filter_kwargs)
    results = divisions.values(f'{nxt_name}_name', f'{nxt_name}_id')
    return JsonResponse(
        data={
            'status': "success",
            "detail": f"Values for {nxt.get('name')} based on {previous_name} retrieved successfully",
            "data": {
                "results": list(results)
            }
        },
        status=200
    )



class LGAResultsView(ResultsView):
    template_name = 'results/lga_results.html'

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        data: dict = json.loads(request.body.decode())
        lga_id = data.get('lga')

        if not lga_id:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': 'LGA id is required'
                },
                status=400
            )

        lga_polling_units = PollingUnit.objects.filter(lga_id=lga_id)
        lga_polling_unit_ids = lga_polling_units.values_list('uniqueid', flat=True)
        lga_polling_units_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=lga_polling_unit_ids)

        parties = Party.objects.all()
        results = []
        for party in parties:
            party_lga_polling_units_results = lga_polling_units_results.filter(party_abbreviation=party.partyid)
            party_lga_score = sum(
                map(lambda x: int(x), party_lga_polling_units_results.values_list('party_score', flat=True))
            )
            party_result = {
                'party_abbreviation': party.partyid,
                'party_score': party_lga_score
            }
            results.append(party_result)
        
        return JsonResponse(
            data={
                'status': 'success',
                'detail': 'LGA results retrieved successfully',
                'data': {
                    "results": results
                }
            },
            status=200
        )



class StorePartyResultsView(ResultsView):
    template_name = 'results/store_party_results.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['parties'] = Party.objects.all()
        return context
    

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        data: dict = json.loads(request.body.decode())
        polling_unit_id = data.get('polling-unit')
        party_id = data.get('party')
        party_score = data.get('party-score')

        if not (polling_unit_id and party_id and party_score):
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': 'Polling unit uniqueid, party abbreviation and party score are required'
                },
                status=400
            )
        
        polling_unit = PollingUnit.objects.filter(polling_unit_id=polling_unit_id).first()
        if not polling_unit:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': 'Polling unit does not exist'
                },
                status=404
            )
        
        party = Party.objects.filter(pk=party_id).first()
        if not party:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': f"Party with id '{party_id}' does not exist"
                },
                status=404
            )
        
        already_stored = AnnouncedPuResults.objects.filter(
            polling_unit_uniqueid=polling_unit.uniqueid,
            party_abbreviation=party.partyid
        ).exists()
        if already_stored:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': f'Result for {party.partyname} party in this polling unit already exists'
                },
                status=400
            )

        AnnouncedPuResults.objects.create(
            polling_unit_uniqueid=polling_unit.uniqueid,
            party_abbreviation=party.partyid,
            party_score=party_score,
            entered_by_user='bincom',
        )

        return JsonResponse(
            data={
                'status': 'success',
                'detail': 'Party results added successfully'
            },
            status=200
        )


polling_unit_results_view = PollingUnitResultsView.as_view()
lga_results_view = LGAResultsView.as_view()
store_party_results_view = StorePartyResultsView.as_view()


