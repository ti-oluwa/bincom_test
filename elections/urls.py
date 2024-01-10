from django.urls import path, include

from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('results/', include('results.urls', namespace='results')),
]
