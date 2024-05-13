from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.get_service, name='get_service'),
    path('add_service/', views.add_service, name='add_service'),
    path('edit_service_modal/<int:service_id>/', views.edit_service_modal, name='edit_service_modal'),
    path('delete/<int:id>/', views.delete_service, name='delete_service'),
]
