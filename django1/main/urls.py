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

    path('users', views.UserView.list, name='users'),
    path('new_user', views.UserView.create, name='new_user'),
    path('delete_user/(?P<pk>[0-9]+)/$', views.UserView.delete, name='delete_user'),
    path('update_user', views.UserView.update, name='update_user'),

    path('add_image', views.ImageView.add, name='add_image'),
    path('all_images', views.ImageView.list, name='all_images'),
    path('delete_image/(?P<pk>[0-9]+)/$', views.ImageView.delete, name='delete_image'),
    path('download', views.ImageView.download, name='download'),
]




urlpatterns += static(MEDIA_URL, document_root=MEDIA_DIR)