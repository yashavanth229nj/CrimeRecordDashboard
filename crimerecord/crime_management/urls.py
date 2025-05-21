from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Police Stations
    path('police-stations/', views.police_stations, name='police_stations'),
    path('police-stations/add/', views.add_police_station, name='add_police_station'),
    path('police-stations/edit/<int:pk>/', views.edit_police_station, name='edit_police_station'),
    path('police-stations/delete/<int:pk>/', views.delete_police_station, name='delete_police_station'),
    
    # Officers
    path('officers/', views.officers, name='officers'),
    path('officers/add/', views.add_officer, name='add_officer'),
    path('officers/edit/<int:pk>/', views.edit_officer, name='edit_officer'),
    path('officers/delete/<int:pk>/', views.delete_officer, name='delete_officer'),
    
    # Crime Types
    path('crime-types/', views.crime_types, name='crime_types'),
    path('crime-types/add/', views.add_crime_type, name='add_crime_type'),
    path('crime-types/edit/<int:pk>/', views.edit_crime_type, name='edit_crime_type'),
    path('crime-types/delete/<int:pk>/', views.delete_crime_type, name='delete_crime_type'),
    
    # Crimes
    path('crimes/', views.crimes, name='crimes'),
    path('crimes/add/', views.add_crime, name='add_crime'),
    path('crimes/edit/<int:pk>/', views.edit_crime, name='edit_crime'),
    path('crimes/delete/<int:pk>/', views.delete_crime, name='delete_crime'),
    
    # FIR Details
    path('fir-details/', views.fir_details, name='fir_details'),
    path('fir-details/add/', views.add_fir, name='add_fir'),
    path('fir-details/edit/<int:pk>/', views.edit_fir, name='edit_fir'),
    path('fir-details/delete/<int:pk>/', views.delete_fir, name='delete_fir'),
    
    # Criminals
    path('criminals/', views.criminals, name='criminals'),
    path('criminals/add/', views.add_criminal, name='add_criminal'),
    path('criminals/edit/<int:pk>/', views.edit_criminal, name='edit_criminal'),
    path('criminals/delete/<int:pk>/', views.delete_criminal, name='delete_criminal'),
    
    # Users
    path('users/', views.users, name='users'),
    path('users/add/', views.add_user, name='add_user'),
    
    # API for chart data
    path('api/crime-stats/', views.crime_stats_api, name='crime_stats_api'),
    path('api/criminal-stats/', views.criminal_stats_api, name='criminal_stats_api'),
    path('api/monthly-crime-stats/', views.monthly_crime_stats_api, name='monthly_crime_stats_api'),
]
