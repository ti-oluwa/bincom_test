from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [
    path('polling-unit/', views.polling_unit_results_view, name='polling_unit_results'),
    path('fetch-next-division/', views.fetch_next_division_by_previous_division_view, name='fetch_next_division'),
    path('lga/', views.lga_results_view, name='lga_results'),
    path('new/', views.store_party_results_view, name='store_party_results')
]
