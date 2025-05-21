from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Management routes
    path('police-stations/', views.police_stations, name='police_stations'),
    path('officers/', views.officers, name='officers'),
    path('crime-types/', views.crime_types, name='crime_types'),
    path('crimes/', views.crimes, name='crimes'),
    path('fir-details/', views.fir_details, name='fir_details'),
    path('criminals/', views.criminals, name='criminals'),
    path('settings/', views.settings, name='settings'),
]