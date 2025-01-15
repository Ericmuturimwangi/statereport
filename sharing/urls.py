from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
     path('upload/', views.upload_file, name='upload_file'),
     path('download/<int:pk>/', views.download_file, name='download_file'),
     path('register/sender', views.register_sender, name='register_sender'),
     path('register/receiver', views.register_receiver, name='register_receiver'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    ]
