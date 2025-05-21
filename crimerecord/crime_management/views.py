from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import (
    PoliceStation, Officer, CrimeType, Crime, FIRDetail, 
    Criminal, CriminalCrime, User, Profile, Admin, ProfileCriminal
)
from .forms import (
    PoliceStationForm, OfficerForm, CrimeTypeForm, CrimeForm, 
    FIRDetailForm, CriminalForm, UserForm, LoginForm
)

def login_view(request):
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
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Get counts for dashboard
    total_crimes = Crime.objects.count()
    total_criminals = Criminal.objects.count()
    total_stations = PoliceStation.objects.count()
    total_officers = Officer.objects.count()
    
    # Get recent FIRs
    recent_firs = FIRDetail.objects.all().order_by('-date', '-time')[:5]
    
    # Get crime types for chart
    crime_types = CrimeType.objects.annotate(crime_count=Count('crime')).order_by('-crime_count')[:5]
    
    context = {
        'total_crimes': total_crimes,
        'total_criminals': total_criminals,
        'total_stations': total_stations,
        'total_officers': total_officers,
        'recent_firs': recent_firs,
        'crime_types': crime_types,
    }
    return render(request, 'dashboard.html', context)

# Police Station Views
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
            messages.success(request, 'Police Station added successfully')
            return redirect('police_stations')
    else:
        form = PoliceStationForm()
    return render(request, 'form_templates/station_form.html', {'form': form, 'title': 'Add Police Station'})

@login_required
def edit_police_station(request, pk):
    station = get_object_or_404(PoliceStation, pk=pk)
    if request.method == 'POST':
        form = PoliceStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            messages.success(request, 'Police Station updated successfully')
            return redirect('police_stations')
    else:
        form = PoliceStationForm(instance=station)
    return render(request, 'form_templates/station_form.html', {'form': form, 'title': 'Edit Police Station'})

@login_required
def delete_police_station(request, pk):
    station = get_object_or_404(PoliceStation, pk=pk)
    station.delete()
    messages.success(request, 'Police Station deleted successfully')
    return redirect('police_stations')

# Officer Views
@login_required
def officers(request):
    officers_list = Officer.objects.all()
    return render(request, 'officers.html', {'officers': officers_list})

@login_required
def add_officer(request):
    if request.method == 'POST':
        form = OfficerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Officer added successfully')
            return redirect('officers')
    else:
        form = OfficerForm()
    return render(request, 'form_templates/officer_form.html', {'form': form, 'title': 'Add Officer'})

@login_required
def edit_officer(request, pk):
    officer = get_object_or_404(Officer, pk=pk)
    if request.method == 'POST':
        form = OfficerForm(request.POST, instance=officer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Officer updated successfully')
            return redirect('officers')
    else:
        form = OfficerForm(instance=officer)
    return render(request, 'form_templates/officer_form.html', {'form': form, 'title': 'Edit Officer'})

@login_required
def delete_officer(request, pk):
    officer = get_object_or_404(Officer, pk=pk)
    officer.delete()
    messages.success(request, 'Officer deleted successfully')
    return redirect('officers')

# Crime Type Views
@login_required
def crime_types(request):
    crime_types_list = CrimeType.objects.all()
    return render(request, 'crime_types.html', {'crime_types': crime_types_list})

@login_required
def add_crime_type(request):
    if request.method == 'POST':
        form = CrimeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crime Type added successfully')
            return redirect('crime_types')
    else:
        form = CrimeTypeForm()
    return render(request, 'form_templates/crime_type_form.html', {'form': form, 'title': 'Add Crime Type'})

@login_required
def edit_crime_type(request, pk):
    crime_type = get_object_or_404(CrimeType, pk=pk)
    if request.method == 'POST':
        form = CrimeTypeForm(request.POST, instance=crime_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crime Type updated successfully')
            return redirect('crime_types')
    else:
        form = CrimeTypeForm(instance=crime_type)
    return render(request, 'form_templates/crime_type_form.html', {'form': form, 'title': 'Edit Crime Type'})

@login_required
def delete_crime_type(request, pk):
    crime_type = get_object_or_404(CrimeType, pk=pk)
    crime_type.delete()
    messages.success(request, 'Crime Type deleted successfully')
    return redirect('crime_types')

# Crime Views
@login_required
def crimes(request):
    crimes_list = Crime.objects.all()
    return render(request, 'crimes.html', {'crimes': crimes_list})

@login_required
def add_crime(request):
    if request.method == 'POST':
        form = CrimeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crime added successfully')
            return redirect('crimes')
    else:
        form = CrimeForm()
    return render(request, 'form_templates/crime_form.html', {'form': form, 'title': 'Add Crime'})

@login_required
def edit_crime(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    if request.method == 'POST':
        form = CrimeForm(request.POST, instance=crime)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crime updated successfully')
            return redirect('crimes')
    else:
        form = CrimeForm(instance=crime)
    return render(request, 'form_templates/crime_form.html', {'form': form, 'title': 'Edit Crime'})

@login_required
def delete_crime(request, pk):
    crime = get_object_or_404(Crime, pk=pk)
    crime.delete()
    messages.success(request, 'Crime deleted successfully')
    return redirect('crimes')

# FIR Details Views
@login_required
def fir_details(request):
    firs = FIRDetail.objects.all().order_by('-date', '-time')
    return render(request, 'fir_details.html', {'firs': firs})

@login_required
def add_fir(request):
    if request.method == 'POST':
        form = FIRDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FIR added successfully')
            return redirect('fir_details')
    else:
        form = FIRDetailForm()
    return render(request, 'form_templates/fir_form.html', {'form': form, 'title': 'Add FIR'})

@login_required
def edit_fir(request, pk):
    fir = get_object_or_404(FIRDetail, pk=pk)
    if request.method == 'POST':
        form = FIRDetailForm(request.POST, instance=fir)
        if form.is_valid():
            form.save()
            messages.success(request, 'FIR updated successfully')
            return redirect('fir_details')
    else:
        form = FIRDetailForm(instance=fir)
    return render(request, 'form_templates/fir_form.html', {'form': form, 'title': 'Edit FIR'})

@login_required
def delete_fir(request, pk):
    fir = get_object_or_404(FIRDetail, pk=pk)
    fir.delete()
    messages.success(request, 'FIR deleted successfully')
    return redirect('fir_details')

# Criminal Views
@login_required
def criminals(request):
    criminals_list = Criminal.objects.all()
    return render(request, 'criminals.html', {'criminals': criminals_list})

@login_required
def add_criminal(request):
    if request.method == 'POST':
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Criminal added successfully')
            return redirect('criminals')
    else:
        form = CriminalForm()
    return render(request, 'form_templates/criminal_form.html', {'form': form, 'title': 'Add Criminal'})

@login_required
def edit_criminal(request, pk):
    criminal = get_object_or_404(Criminal, pk=pk)
    if request.method == 'POST':
        form = CriminalForm(request.POST, instance=criminal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Criminal updated successfully')
            return redirect('criminals')
    else:
        form = CriminalForm(instance=criminal)
    return render(request, 'form_templates/criminal_form.html', {'form': form, 'title': 'Edit Criminal'})

@login_required
def delete_criminal(request, pk):
    criminal = get_object_or_404(Criminal, pk=pk)
    criminal.delete()
    messages.success(request, 'Criminal deleted successfully')
    return redirect('criminals')

# User Views
@login_required
def users(request):
    users_list = User.objects.all()
    return render(request, 'users.html', {'users': users_list})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully')
            return redirect('users')
    else:
        form = UserForm()
    return render(request, 'form_templates/user_form.html', {'form': form, 'title': 'Add User'})

# API endpoints for charts
@login_required
def crime_stats_api(request):
    crime_types = CrimeType.objects.annotate(crime_count=Count('crime')).order_by('-crime_count')
    data = {
        'labels': [ct.crime_type_name for ct in crime_types],
        'data': [ct.crime_count for ct in crime_types]
    }
    return JsonResponse(data)

@login_required
def criminal_stats_api(request):
    gender_data = Criminal.objects.values('gender').annotate(count=Count('gender'))
    data = {
        'labels': [d['gender'] if d['gender'] else 'Unknown' for d in gender_data],
        'data': [d['count'] for d in gender_data]
    }
    return JsonResponse(data)

@login_required
def monthly_crime_stats_api(request):
    # Get all FIR details
    all_firs = FIRDetail.objects.all()
    
    # Prepare month counter
    month_counter = {i: 0 for i in range(1, 13)}
    
    # Count FIRs by month
    for fir in all_firs:
        month = fir.date.month
        month_counter[month] += 1
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = {
        'labels': months,
        'data': [month_counter[i] for i in range(1, 13)]
    }
    
    return JsonResponse(data)
