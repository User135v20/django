from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
