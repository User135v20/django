from django.conf.urls.static import static
from django.urls import path

from . import views
from .settings import MEDIA_URL, MEDIA_DIR

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),

    path('create_result', views.ResultView.create, name='create_result'),
    path('results', views.ResultView.list, name='all_results'),
    path('result/(?P<pk>[0-9]+)/$', views.ResultView.get, name='result'),
    path('delete_result/(?P<pk>[0-9]+)/$', views.ResultView.delete, name='delete_result'),
    path('update_result', views.ResultView.update, name='update_result'),

    path('patients', views.PatientView.list, name='patients'),
    path('new_patient', views.PatientView.create, name='new_patient'),
    path('delete_patient/(?P<pk>[0-9]+)/$', views.PatientView.delete, name='delete_patient'),
    path('update_patient', views.PatientView.update, name='update_patient'),

    path('add_image', views.ImageView.add, name='add_image'),
    path('all_images', views.ImageView.list, name='all_images'),
    path('delete_image/(?P<pk>[0-9]+)/$', views.ImageView.delete, name='delete_image'),
]




urlpatterns += static(MEDIA_URL, document_root=MEDIA_DIR)