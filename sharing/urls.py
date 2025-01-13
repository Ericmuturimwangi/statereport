from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('upload/', views.upload_file, name='upload_file'),
     path('download/<int:pk>/', views.download_file, name='download_file'),
]
