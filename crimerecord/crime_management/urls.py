from django.urls import path
from . import views

urlpatterns = [
    # Welcome page
    path('', views.welcome, name='welcome'),
]
