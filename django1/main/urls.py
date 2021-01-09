from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),

    path('create_result', views.ResultView.create, name='create_result'),
    path('results', views.ResultView.list, name='all_results'),
    path('result/(?P<pk>[0-9]+)/$', views.ResultView.get, name='result'),

    path('patients', views.PatientView.list, name='patients'),
    path('new_patient', views.PatientView.create, name='new_patient'),
    path('delete_patient/(?P<pk>[0-9]+)/$', views.PatientView.delete, name='delete_patient'),
    path('update_patient', views.PatientView.update, name='update_patient'),
]