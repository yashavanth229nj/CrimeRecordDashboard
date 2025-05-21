from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    Admin, User as CustomUser, Profile, PoliceStation, Officer, 
    CrimeType, Crime, FIRDetail, Criminal, CriminalCrime
)
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Simple validation
        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'register.html', {'error_message': error_message})
        
        # Create user (in a real app, add more validation)
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create our app's user model
        admin = Admin.objects.create(name=f"{first_name} {last_name}")
        custom_user = CustomUser.objects.create(admin=admin, username=username)
        Profile.objects.create(user=custom_user, full_name=f"{first_name} {last_name}")
        
        # Log in the user
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('dashboard')
    
    return render(request, 'register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def welcome(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'welcome.html')

@login_required
def dashboard(request):
    # Get counts for dashboard statistics
    total_crimes = Crime.objects.count()
    total_criminals = Criminal.objects.count()
    total_stations = PoliceStation.objects.count()
    total_officers = Officer.objects.count()
    
    # Get recent FIR details
    recent_fir = FIRDetail.objects.all().order_by('-date', '-time')[:10]
    
    # Get data for crime type distribution chart
    crime_type_data = []
    crime_type_labels = []
    
    crime_counts = Crime.objects.values('crime_type__crime_type_name').annotate(count=Count('crime_id'))
    
    for item in crime_counts:
        crime_type_labels.append(item['crime_type__crime_type_name'])
        crime_type_data.append(item['count'])
    
    # Get data for criminal gender distribution chart
    male_count = Criminal.objects.filter(gender='Male').count()
    female_count = Criminal.objects.filter(gender='Female').count()
    other_count = Criminal.objects.filter(gender='Other').count()
    gender_data = [male_count, female_count, other_count]
    
    # Get data for monthly crime chart (past 6 months)
    monthly_data = []
    monthly_labels = []
    
    # Get data for the past 6 months
    today = timezone.now().date()
    
    for i in range(5, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=i*30)
        month_name = month_date.strftime('%B')
        month_start = month_date.replace(day=1)
        
        # Calculate month end (last day of month)
        if month_date.month == 12:
            month_end = month_date.replace(day=31)
        else:
            next_month = month_date.replace(month=month_date.month+1)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        
        # Count FIRs for this month
        month_count = FIRDetail.objects.filter(date__gte=month_start, date__lte=month_end).count()
        
        monthly_labels.append(month_name)
        monthly_data.append(month_count)
    
    context = {
        'total_crimes': total_crimes,
        'total_criminals': total_criminals,
        'total_stations': total_stations,
        'total_officers': total_officers,
        'recent_fir': recent_fir,
        'crime_type_data': crime_type_data,
        'crime_type_labels': json.dumps(crime_type_labels),
        'gender_data': gender_data,
        'monthly_data': monthly_data,
        'monthly_labels': json.dumps(monthly_labels)
    }
    
    return render(request, 'dashboard_charts.html', context)

# Police Stations management
@login_required
def police_stations(request):
    stations = PoliceStation.objects.all()
    return render(request, 'police_stations.html', {'stations': stations})

# Officers management
@login_required
def officers(request):
    all_officers = Officer.objects.all()
    return render(request, 'officers.html', {'officers': all_officers})

# Crime Types management
@login_required
def crime_types(request):
    all_crime_types = CrimeType.objects.all()
    return render(request, 'crime_types.html', {'crime_types': all_crime_types})

# Crimes management
@login_required
def crimes(request):
    all_crimes = Crime.objects.all()
    return render(request, 'crimes.html', {'crimes': all_crimes})

# FIR Details management
@login_required
def fir_details(request):
    all_fir_details = FIRDetail.objects.all().order_by('-date', '-time')
    return render(request, 'fir_details.html', {'fir_details': all_fir_details})

# Criminals management
@login_required
def criminals(request):
    all_criminals = Criminal.objects.all()
    return render(request, 'criminals.html', {'criminals': all_criminals})

# Settings page
@login_required
def settings(request):
    return render(request, 'settings.html')