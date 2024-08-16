from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('success/', views.registration_success, name='registration_success'),
    path('get_service/', views.get_service, name='get_service'),
    path('add_service/', views.add_service, name='add_service'),
    path('edit_service_modal/<int:service_id>/', views.edit_service_modal, name='edit_service_modal'),
    path('delete/<int:id>/', views.delete_service, name='delete_service'),
    path("verify/<str:userid>/<str:token>/", views.verify_email, name="verify_email"),
]
