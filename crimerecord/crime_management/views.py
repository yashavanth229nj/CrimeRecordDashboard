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
from .forms import (
    LoginForm, PoliceStationForm, OfficerForm, CrimeTypeForm,
    CrimeForm, FIRDetailForm, CriminalForm
)

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
            # Use relativedelta to correctly handle month transitions
            from dateutil.relativedelta import relativedelta
            next_month = month_date + relativedelta(months=1)
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

@login_required
def add_police_station(request):
    if request.method == 'POST':
        form = PoliceStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('police_stations')
    else:
        form = PoliceStationForm()
    
    return render(request, 'form_templates/station_form.html', {
        'form': form,
        'title': 'Add Police Station'
    })

@login_required
def edit_police_station(request, station_id):
    station = get_object_or_404(PoliceStation, station_id=station_id)
    
    if request.method == 'POST':
        form = PoliceStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('police_stations')
    else:
        form = PoliceStationForm(instance=station)
    
    return render(request, 'form_templates/station_form.html', {
        'form': form,
        'title': 'Edit Police Station'
    })

@login_required
def delete_police_station(request, station_id):
    station = get_object_or_404(PoliceStation, station_id=station_id)
    station.delete()
    return redirect('police_stations')

# Officers management
@login_required
def officers(request):
    all_officers = Officer.objects.all()
    return render(request, 'officers.html', {'officers': all_officers})

@login_required
def add_officer(request):
    if request.method == 'POST':
        form = OfficerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('officers')
    else:
        form = OfficerForm()
    
    return render(request, 'form_templates/officer_form.html', {
        'form': form,
        'title': 'Add Officer'
    })

@login_required
def edit_officer(request, officer_id):
    officer = get_object_or_404(Officer, officer_id=officer_id)
    
    if request.method == 'POST':
        form = OfficerForm(request.POST, instance=officer)
        if form.is_valid():
            form.save()
            return redirect('officers')
    else:
        form = OfficerForm(instance=officer)
    
    return render(request, 'form_templates/officer_form.html', {
        'form': form,
        'title': 'Edit Officer'
    })

@login_required
def delete_officer(request, officer_id):
    officer = get_object_or_404(Officer, officer_id=officer_id)
    officer.delete()
    return redirect('officers')

# Crime Types management
@login_required
def crime_types(request):
    all_crime_types = CrimeType.objects.all()
    return render(request, 'crime_types.html', {'crime_types': all_crime_types})

@login_required
def add_crime_type(request):
    if request.method == 'POST':
        form = CrimeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crime_types')
    else:
        form = CrimeTypeForm()
    
    return render(request, 'form_templates/crime_type_form.html', {
        'form': form,
        'title': 'Add Crime Type'
    })

@login_required
def edit_crime_type(request, crime_type_id):
    crime_type = get_object_or_404(CrimeType, crime_type_id=crime_type_id)
    
    if request.method == 'POST':
        form = CrimeTypeForm(request.POST, instance=crime_type)
        if form.is_valid():
            form.save()
            return redirect('crime_types')
    else:
        form = CrimeTypeForm(instance=crime_type)
    
    return render(request, 'form_templates/crime_type_form.html', {
        'form': form,
        'title': 'Edit Crime Type'
    })

@login_required
def delete_crime_type(request, crime_type_id):
    crime_type = get_object_or_404(CrimeType, crime_type_id=crime_type_id)
    crime_type.delete()
    return redirect('crime_types')

# Crimes management
@login_required
def crimes(request):
    all_crimes = Crime.objects.all()
    return render(request, 'crimes.html', {'crimes': all_crimes})

@login_required
def add_crime(request):
    if request.method == 'POST':
        form = CrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crimes')
    else:
        form = CrimeForm()
    
    return render(request, 'form_templates/crime_form.html', {
        'form': form,
        'title': 'Add Crime'
    })

@login_required
def edit_crime(request, crime_id):
    crime = get_object_or_404(Crime, crime_id=crime_id)
    
    if request.method == 'POST':
        form = CrimeForm(request.POST, instance=crime)
        if form.is_valid():
            form.save()
            return redirect('crimes')
    else:
        form = CrimeForm(instance=crime)
    
    return render(request, 'form_templates/crime_form.html', {
        'form': form,
        'title': 'Edit Crime'
    })

@login_required
def delete_crime(request, crime_id):
    crime = get_object_or_404(Crime, crime_id=crime_id)
    crime.delete()
    return redirect('crimes')

# FIR Details management
@login_required
def fir_details(request):
    all_fir_details = FIRDetail.objects.all().order_by('-date', '-time')
    return render(request, 'fir_details.html', {'firs': all_fir_details})

@login_required
def add_fir(request):
    if request.method == 'POST':
        form = FIRDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fir_details')
    else:
        form = FIRDetailForm()
    
    return render(request, 'form_templates/fir_form.html', {
        'form': form,
        'title': 'Add FIR Report'
    })

@login_required
def edit_fir(request, fir_id):
    fir = get_object_or_404(FIRDetail, fir_id=fir_id)
    
    if request.method == 'POST':
        form = FIRDetailForm(request.POST, instance=fir)
        if form.is_valid():
            form.save()
            return redirect('fir_details')
    else:
        form = FIRDetailForm(instance=fir)
    
    return render(request, 'form_templates/fir_form.html', {
        'form': form,
        'title': 'Edit FIR Report'
    })

@login_required
def delete_fir(request, fir_id):
    fir = get_object_or_404(FIRDetail, fir_id=fir_id)
    fir.delete()
    return redirect('fir_details')

# Criminals management
@login_required
def criminals(request):
    all_criminals = Criminal.objects.all()
    return render(request, 'criminals.html', {'criminals': all_criminals})

@login_required
def add_criminal(request):
    if request.method == 'POST':
        # Assume we have a CriminalForm in forms.py
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criminals')
    else:
        form = CriminalForm()
    
    return render(request, 'form_templates/criminal_form.html', {
        'form': form,
        'title': 'Add Criminal'
    })

@login_required
def edit_criminal(request, criminal_id):
    criminal = get_object_or_404(Criminal, criminal_id=criminal_id)
    
    if request.method == 'POST':
        form = CriminalForm(request.POST, instance=criminal)
        if form.is_valid():
            form.save()
            return redirect('criminals')
    else:
        form = CriminalForm(instance=criminal)
    
    return render(request, 'form_templates/criminal_form.html', {
        'form': form,
        'title': 'Edit Criminal'
    })

@login_required
def delete_criminal(request, criminal_id):
    criminal = get_object_or_404(Criminal, criminal_id=criminal_id)
    criminal.delete()
    return redirect('criminals')

# Settings page
@login_required
def settings(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        
        if form_type == 'profile':
            # Handle profile form
            full_name = request.POST.get('full_name', '')
            email = request.POST.get('email', '')
            
            if full_name:
                names = full_name.split(' ', 1)
                request.user.first_name = names[0]
                if len(names) > 1:
                    request.user.last_name = names[1]
                else:
                    request.user.last_name = ''
            
            if email:
                request.user.email = email
            
            request.user.save()
            
            # Handle profile image upload if included
            if 'profile_image' in request.FILES:
                # You would need to add logic to handle the file upload
                pass
                
            return redirect('settings')
            
        elif form_type == 'password':
            # Handle password change form
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            if current_password and new_password and confirm_password:
                if request.user.check_password(current_password):
                    if new_password == confirm_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        # Re-authenticate the user after password change
                        from django.contrib.auth import update_session_auth_hash
                        update_session_auth_hash(request, request.user)
                        return redirect('settings')
            
        elif form_type == 'system':
            # Handle system settings
            # In a real app, you might save these to a Settings model
            # or to user preferences
            
            return redirect('settings')
    
    return render(request, 'settings.html')