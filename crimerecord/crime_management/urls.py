from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Main pages
    path('', views.dashboard, name='dashboard'),
    path('welcome/', views.welcome, name='welcome'),
    
    # Police Stations
    path('police-stations/', views.police_stations, name='police_stations'),
    path('police-stations/add/', views.add_police_station, name='add_police_station'),
    path('police-stations/edit/<int:station_id>/', views.edit_police_station, name='edit_police_station'),
    path('police-stations/delete/<int:station_id>/', views.delete_police_station, name='delete_police_station'),
    
    # Officers
    path('officers/', views.officers, name='officers'),
    path('officers/add/', views.add_officer, name='add_officer'),
    path('officers/edit/<int:officer_id>/', views.edit_officer, name='edit_officer'),
    path('officers/delete/<int:officer_id>/', views.delete_officer, name='delete_officer'),
    
    # Crime Types
    path('crime-types/', views.crime_types, name='crime_types'),
    path('crime-types/add/', views.add_crime_type, name='add_crime_type'),
    path('crime-types/edit/<int:crime_type_id>/', views.edit_crime_type, name='edit_crime_type'),
    path('crime-types/delete/<int:crime_type_id>/', views.delete_crime_type, name='delete_crime_type'),
    
    # Crimes
    path('crimes/', views.crimes, name='crimes'),
    path('crimes/add/', views.add_crime, name='add_crime'),
    path('crimes/edit/<int:crime_id>/', views.edit_crime, name='edit_crime'),
    path('crimes/delete/<int:crime_id>/', views.delete_crime, name='delete_crime'),
    
    # FIR Details
    path('fir-details/', views.fir_details, name='fir_details'),
    path('fir-details/add/', views.add_fir_detail, name='add_fir_detail'),
    path('fir-details/edit/<int:fir_id>/', views.edit_fir_detail, name='edit_fir_detail'),
    path('fir-details/delete/<int:fir_id>/', views.delete_fir_detail, name='delete_fir_detail'),
    path('fir-details/view/<int:fir_id>/', views.fir_detail, name='fir_detail'),
    
    # Criminals
    path('criminals/', views.criminals, name='criminals'),
    path('criminals/add/', views.add_criminal, name='add_criminal'),
    path('criminals/edit/<int:criminal_id>/', views.edit_criminal, name='edit_criminal'),
    path('criminals/delete/<int:criminal_id>/', views.delete_criminal, name='delete_criminal'),
    path('criminals/view/<int:criminal_id>/', views.criminal_detail, name='criminal_detail'),
    
    # Settings
    path('settings/', views.settings, name='settings'),
]