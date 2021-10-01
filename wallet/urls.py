from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'uploadImage', views.uploadImage, name='uploadImage'),
    url(r'getFiles', views.getFiles, name='getFiles'),
]
