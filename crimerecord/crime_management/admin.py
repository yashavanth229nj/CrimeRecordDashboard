from django.contrib import admin
from .models import (
    Admin, User, Profile, PoliceStation, Officer, 
    CrimeType, Crime, FIRDetail, Criminal, 
    CriminalCrime, ProfileCriminal
)

# Register models with admin site
admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Profile)

@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'status', 'area_id', 'address')
    search_fields = ('name', 'contact_person', 'area_id')

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('name', 'off_rank', 'contact', 'station')
    list_filter = ('station', 'off_rank')
    search_fields = ('name', 'contact')

@admin.register(CrimeType)
class CrimeTypeAdmin(admin.ModelAdmin):
    list_display = ('crime_type_name', 'description')
    search_fields = ('crime_type_name',)

@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ('crime_id', 'crime_type')
    list_filter = ('crime_type',)

@admin.register(FIRDetail)
class FIRDetailAdmin(admin.ModelAdmin):
    list_display = ('fir_id', 'date', 'time', 'crime', 'user', 'officer')
    list_filter = ('date', 'officer')
    search_fields = ('description',)

@admin.register(Criminal)
class CriminalAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'date_of_birth', 'address', 'nationality')
    list_filter = ('gender', 'nationality')
    search_fields = ('name', 'address')

@admin.register(CriminalCrime)
class CriminalCrimeAdmin(admin.ModelAdmin):
    list_display = ('criminal', 'crime')
    list_filter = ('crime',)

@admin.register(ProfileCriminal)
class ProfileCriminalAdmin(admin.ModelAdmin):
    list_display = ('profile', 'criminal')
    list_filter = ('criminal',)
