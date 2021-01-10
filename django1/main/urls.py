from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('Patient_database', views.PatientView.list, name='Patient_database')

]