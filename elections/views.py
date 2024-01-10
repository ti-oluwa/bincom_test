from django.views import generic


class IndexView(generic.RedirectView):
    url = 'results/polling-unit/'


index_view = IndexView.as_view()
