from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('download/', views.download_logs),
]