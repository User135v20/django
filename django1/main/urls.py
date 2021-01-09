from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('results', views.results, name='all_results'),
    path('new_patient', views.new_patient, name='new_patient'),
]