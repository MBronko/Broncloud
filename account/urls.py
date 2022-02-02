from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # new

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
