from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('url', views.shorten_url, name='url'),
    path('delete/<str:resource_id>', views.delete_resource, name='delete'),
    path('<str:resource_id>', views.get_resource, name='resource'),
]
