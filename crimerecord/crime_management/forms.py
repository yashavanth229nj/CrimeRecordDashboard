from django import forms
from .models import (
    PoliceStation, Officer, CrimeType, Crime, 
    FIRDetail, Criminal, User, Admin
)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PoliceStationForm(forms.ModelForm):
    class Meta:
        model = PoliceStation
        fields = ['name', 'contact_person', 'status', 'area_id', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'area_id': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = ['name', 'off_rank', 'contact', 'station']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'off_rank': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'station': forms.Select(attrs={'class': 'form-control'}),
        }

class CrimeTypeForm(forms.ModelForm):
    class Meta:
        model = CrimeType
        fields = ['crime_type_name', 'description']
        widgets = {
            'crime_type_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ['crime_type']
        widgets = {
            'crime_type': forms.Select(attrs={'class': 'form-control'}),
        }

class FIRDetailForm(forms.ModelForm):
    class Meta:
        model = FIRDetail
        fields = ['description', 'date', 'time', 'crime', 'user', 'officer']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'crime': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'officer': forms.Select(attrs={'class': 'form-control'}),
        }

class CriminalForm(forms.ModelForm):
    class Meta:
        model = Criminal
        fields = ['name', 'gender', 'date_of_birth', 'address', 'nationality']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['admin']
        widgets = {
            'admin': forms.Select(attrs={'class': 'form-control'}),
        }
