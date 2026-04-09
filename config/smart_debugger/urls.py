from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
        path('download/', download_logs, name='download_logs'),

]