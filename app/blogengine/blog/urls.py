from django.urls import path

from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/<str:slug>/', PostDetails.as_view(), name='post_details_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/<str:slug>/', TagDetails.as_view(), name='tag_details_url'),
]