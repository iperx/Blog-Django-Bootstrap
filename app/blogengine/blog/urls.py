from django.urls import path

from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('tags/', tags_list, name='tags_list_url'),
]