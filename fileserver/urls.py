from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:resource_id>', views.get_resource, name='resource'),
]
