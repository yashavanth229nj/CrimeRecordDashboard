from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, timedelta
import json
import random
from dateutil.relativedelta import relativedelta

from .models import (
    Admin, User as CustomUser, Profile, PoliceStation, Officer, 
    CrimeType, Crime, FIRDetail, Criminal, CriminalCrime, ProfileCriminal
)
from .forms import (
    LoginForm, PoliceStationForm, OfficerForm, CrimeTypeForm,
    CrimeForm, FIRDetailForm, CriminalForm, UserForm
)

# Create dummy data for visualizations
def create_dummy_data():
    # Create dummy police stations if none exist
    if PoliceStation.objects.count() == 0:
        stations = [
            {"name": "Central Police Station", "contact_person": "Capt. Anderson", "status": "Active", "area_id": "A-101", "address": "123 Main Street, Downtown"},
            {"name": "Westside Precinct", "contact_person": "Lt. Martinez", "status": "Active", "area_id": "B-202", "address": "456 West Avenue, Westside"},
            {"name": "North District Station", "contact_person": "Sgt. Thompson", "status": "Active", "area_id": "C-303", "address": "789 North Road, Northside"},
            {"name": "South Police Headquarters", "contact_person": "Capt. Johnson", "status": "Active", "area_id": "D-404", "address": "101 South Blvd, Southside"},
            {"name": "Eastside Police Post", "contact_person": "Lt. Williams", "status": "Active", "area_id": "E-505", "address": "202 East Street, Eastside"},
        ]
        
        for station_data in stations:
            PoliceStation.objects.create(**station_data)
    
    # Create crime types if none exist
    if CrimeType.objects.count() == 0:
        crime_types = [
            {"crime_type_name": "Theft", "description": "Unlawful taking of property without owner's consent."},
            {"crime_type_name": "Assault", "description": "Physical attack or threat of attack on an individual."},
            {"crime_type_name": "Robbery", "description": "Taking property by force or threat of force."},
            {"crime_type_name": "Burglary", "description": "Illegal entry into a building with intent to commit a crime."},
            {"crime_type_name": "Fraud", "description": "Deception for personal gain."},
            {"crime_type_name": "Vandalism", "description": "Willful destruction or damage to property."},
            {"crime_type_name": "Drug Offenses", "description": "Possession, distribution, or manufacturing of illegal drugs."},
            {"crime_type_name": "Cyber Crime", "description": "Criminal activities conducted via the internet or computers."}
        ]
        
        for crime_type_data in crime_types:
            CrimeType.objects.create(**crime_type_data)
    
    # Create admin user if none exists
    if Admin.objects.count() == 0:
        admin = Admin.objects.create()
        
        # Create custom user linked to admin
        if CustomUser.objects.count() == 0:
            user = CustomUser.objects.create(admin=admin)
            
            # Create profile linked to user
            if Profile.objects.count() == 0:
                Profile.objects.create(user=user)
    
    # Create officers if none exist
    if Officer.objects.count() == 0:
        officers = [
            {"name": "John Smith", "off_rank": "Inspector", "contact": "555-1234", "station": PoliceStation.objects.get(id=1)},
            {"name": "Maria Rodriguez", "off_rank": "Sergeant", "contact": "555-2345", "station": PoliceStation.objects.get(id=2)},
            {"name": "Robert Johnson", "off_rank": "Constable", "contact": "555-3456", "station": PoliceStation.objects.get(id=3)},
            {"name": "Sarah Williams", "off_rank": "Lieutenant", "contact": "555-4567", "station": PoliceStation.objects.get(id=4)},
            {"name": "Michael Brown", "off_rank": "Captain", "contact": "555-5678", "station": PoliceStation.objects.get(id=5)},
            {"name": "Jennifer Davis", "off_rank": "Inspector", "contact": "555-6789", "station": PoliceStation.objects.get(id=1)},
            {"name": "David Wilson", "off_rank": "Sergeant", "contact": "555-7890", "station": PoliceStation.objects.get(id=2)},
            {"name": "Lisa Taylor", "off_rank": "Constable", "contact": "555-8901", "station": PoliceStation.objects.get(id=3)}
        ]
        
        for officer_data in officers:
            Officer.objects.create(**officer_data)
    
    # Create crimes linked to crime types if none exist
    if Crime.objects.count() == 0:
        for crime_type in CrimeType.objects.all():
            # Create multiple crimes for each crime type
            for i in range(random.randint(2, 5)):
                Crime.objects.create(crime_type=crime_type)
    
    # Create criminals if none exist
    if Criminal.objects.count() == 0:
        criminals = [
            {"name": "Jake Roberts", "gender": "Male", "date_of_birth": "1985-07-12", "address": "123 Criminal Lane, Downtown", "nationality": "American"},
            {"name": "Emily Wilson", "gender": "Female", "date_of_birth": "1990-03-24", "address": "456 Outlaw Street, Westside", "nationality": "Canadian"},
            {"name": "Carlos Mendez", "gender": "Male", "date_of_birth": "1978-11-05", "address": "789 Felony Road, Southside", "nationality": "Mexican"},
            {"name": "Anna Johnson", "gender": "Female", "date_of_birth": "1982-09-17", "address": "101 Misdemeanor Ave, Eastside", "nationality": "American"},
            {"name": "Trevor Phillips", "gender": "Male", "date_of_birth": "1972-05-30", "address": "202 Wanted Street, Northside", "nationality": "British"},
            {"name": "Sophia Chen", "gender": "Female", "date_of_birth": "1993-12-08", "address": "303 Fugitive Blvd, Downtown", "nationality": "Chinese"},
            {"name": "Mohamed Al-Fayed", "gender": "Male", "date_of_birth": "1987-02-14", "address": "404 Lawless Lane, Westside", "nationality": "Egyptian"},
            {"name": "Isabella Romano", "gender": "Female", "date_of_birth": "1991-08-22", "address": "505 Outlaw Circle, Southside", "nationality": "Italian"},
            {"name": "Raj Patel", "gender": "Male", "date_of_birth": "1983-04-11", "address": "606 Criminal Court, Eastside", "nationality": "Indian"},
            {"name": "Nina Petrova", "gender": "Female", "date_of_birth": "1989-10-29", "address": "707 Bandit Road, Northside", "nationality": "Russian"},
            {"name": "Alex Undefined", "gender": "Other", "date_of_birth": "1995-06-15", "address": "808 Mystery Street, Downtown", "nationality": "Australian"},
            {"name": "Unknown Person", "gender": "Other", "date_of_birth": "1980-01-01", "address": "909 Unknown Place, Unknown", "nationality": "Unknown"}
        ]
        
        for criminal_data in criminals:
            Criminal.objects.create(**criminal_data)
    
    # Create criminal-crime associations if none exist
    if CriminalCrime.objects.count() == 0:
        criminals = Criminal.objects.all()
        crimes = Crime.objects.all()
        
        # Assign 1-3 crimes to each criminal
        for criminal in criminals:
            selected_crimes = random.sample(list(crimes), random.randint(1, 3))
            for crime in selected_crimes:
                CriminalCrime.objects.create(criminal=criminal, crime=crime)
    
    # Create FIR details if none exist
    if FIRDetail.objects.count() == 0:
        crimes = Crime.objects.all()
        officers = Officer.objects.all()
        user = CustomUser.objects.first()  # Use the first user for all FIRs
        
        # Generate FIRs for the past 6 months
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=180)
        
        # Create 20 FIRs with randomly distributed dates
        for i in range(20):
            days_offset = random.randint(0, 180)
            fir_date = end_date - timedelta(days=days_offset)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            fir_time = f"{hour:02d}:{minute:02d}"
            
            FIRDetail.objects.create(
                description=f"FIR report #{i+1} for investigation of incident.",
                date=fir_date,
                time=fir_time,
                crime=random.choice(crimes),
                user=user,
                officer=random.choice(officers)
            )

# Authentication views
def user_login(request):
    error_message = None
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid username or password."
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def user_register(request):
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if passwords match
        if password != confirm_password:
            error_message = "Passwords do not match."
        # Check if username already exists
        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists."
        else:
            # Create Django auth user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create Admin, CustomUser, and Profile objects
            admin = Admin.objects.create()
            custom_user = CustomUser.objects.create(admin=admin)
            Profile.objects.create(user=custom_user)
            
            # Log the user in
            login(request, user)
            return redirect('dashboard')
    
    return render(request, 'register.html', {'error_message': error_message})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard and main views
@login_required
def dashboard(request):
    # Ensure dummy data exists
    create_dummy_data()
    
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
    
    # Get data for monthly crime chart
    monthly_data = []
    monthly_labels = []
    
    # Get data for the past 6 months
    today = datetime.now()
    for i in range(5, -1, -1):
        month_date = today - relativedelta(months=i)
        month_name = month_date.strftime('%B')
        month_start = month_date.replace(day=1).date()
        
        if i > 0:
            next_month = today - relativedelta(months=i-1)
            month_end = next_month.replace(day=1).date() - timedelta(days=1)
        else:
            month_end = today.date()
        
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
    
    return render(request, 'dashboard.html', context)

# Police Stations views
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
    
    return render(request, 'add_police_station.html', {'form': form})

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
    
    return render(request, 'edit_police_station.html', {'form': form})

@login_required
def delete_police_station(request, station_id):
    station = get_object_or_404(PoliceStation, station_id=station_id)
    station.delete()
    return redirect('police_stations')

# Officers views
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
    
    return render(request, 'add_officer.html', {'form': form})

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
    
    return render(request, 'edit_officer.html', {'form': form})

@login_required
def delete_officer(request, officer_id):
    officer = get_object_or_404(Officer, officer_id=officer_id)
    officer.delete()
    return redirect('officers')

# Crime Types views
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
    
    return render(request, 'add_crime_type.html', {'form': form})

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
    
    return render(request, 'edit_crime_type.html', {'form': form})

@login_required
def delete_crime_type(request, crime_type_id):
    crime_type = get_object_or_404(CrimeType, crime_type_id=crime_type_id)
    crime_type.delete()
    return redirect('crime_types')

# Crimes views
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
    
    return render(request, 'add_crime.html', {'form': form})

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
    
    return render(request, 'edit_crime.html', {'form': form})

@login_required
def delete_crime(request, crime_id):
    crime = get_object_or_404(Crime, crime_id=crime_id)
    crime.delete()
    return redirect('crimes')

# FIR Details views
@login_required
def fir_details(request):
    all_fir_details = FIRDetail.objects.all().order_by('-date', '-time')
    return render(request, 'fir_details.html', {'fir_details': all_fir_details})

@login_required
def add_fir_detail(request):
    if request.method == 'POST':
        form = FIRDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fir_details')
    else:
        form = FIRDetailForm()
    
    return render(request, 'add_fir_detail.html', {'form': form})

@login_required
def edit_fir_detail(request, fir_id):
    fir_detail = get_object_or_404(FIRDetail, fir_id=fir_id)
    
    if request.method == 'POST':
        form = FIRDetailForm(request.POST, instance=fir_detail)
        if form.is_valid():
            form.save()
            return redirect('fir_details')
    else:
        form = FIRDetailForm(instance=fir_detail)
    
    return render(request, 'edit_fir_detail.html', {'form': form})

@login_required
def delete_fir_detail(request, fir_id):
    fir_detail = get_object_or_404(FIRDetail, fir_id=fir_id)
    fir_detail.delete()
    return redirect('fir_details')

@login_required
def fir_detail(request, fir_id):
    fir = get_object_or_404(FIRDetail, fir_id=fir_id)
    return render(request, 'fir_detail.html', {'fir': fir})

# Criminals views
@login_required
def criminals(request):
    all_criminals = Criminal.objects.all()
    return render(request, 'criminals.html', {'criminals': all_criminals})

@login_required
def add_criminal(request):
    if request.method == 'POST':
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criminals')
    else:
        form = CriminalForm()
    
    return render(request, 'add_criminal.html', {'form': form})

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
    
    return render(request, 'edit_criminal.html', {'form': form})

@login_required
def delete_criminal(request, criminal_id):
    criminal = get_object_or_404(Criminal, criminal_id=criminal_id)
    criminal.delete()
    return redirect('criminals')

@login_required
def criminal_detail(request, criminal_id):
    criminal = get_object_or_404(Criminal, criminal_id=criminal_id)
    crimes = Crime.objects.filter(criminalcrime__criminal=criminal)
    return render(request, 'criminal_detail.html', {'criminal': criminal, 'crimes': crimes})

# Settings view
@login_required
def settings(request):
    return render(request, 'settings.html')

# Welcome page
def welcome(request):
    return render(request, 'welcome.html')