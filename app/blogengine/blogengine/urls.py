from django.contrib import admin
from django.urls import path
from django.urls import include
from django.shortcuts import redirect

from .views import redirect_blog


urlpatterns = [
    path('', redirect_blog),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
]
