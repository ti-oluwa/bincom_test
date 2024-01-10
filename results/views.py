from re import L
from typing import Any
from django.views import generic
import json
from django.http import JsonResponse

from divisions.models import States, LGA, Ward, PollingUnit
from .models import AnnouncedPuResults



class PollingUnitResultsView(generic.TemplateView):
    template_name = 'results/polling_unit_results.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['states'] = States.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST request"""
        data: dict = json.loads(request.body.decode())
        polling_unit_uniqueid = data.get('polling-unit')

        if not polling_unit_uniqueid:
            return JsonResponse(
                data={
                    'status': 'error',
                    'detail': 'Polling unit uniqueid is required'
                },
                status=400
            )
        
        polling_unit_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=polling_unit_uniqueid)
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
    results = divisions.values(f'{nxt_name}_name', 'pk')
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



polling_unit_results_view = PollingUnitResultsView.as_view()


