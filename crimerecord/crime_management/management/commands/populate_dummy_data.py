from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from crime_management.models import (
    Admin, User, Profile, PoliceStation, Officer, 
    CrimeType, Crime, FIRDetail, Criminal, CriminalCrime
)

class Command(BaseCommand):
    help = 'Populate database with dummy data for visualizations'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data for visualizations...')
        
        # Create Admin
        admin_count = Admin.objects.count()
        if admin_count == 0:
            admin = Admin.objects.create(name="System Admin")
            self.stdout.write(self.style.SUCCESS(f'Created Admin: {admin}'))
        else:
            admin = Admin.objects.first()
            
        # Create User
        user_count = User.objects.count()
        if user_count == 0:
            user = User.objects.create(admin=admin, username="admin_user")
            self.stdout.write(self.style.SUCCESS(f'Created User: {user}'))
        else:
            user = User.objects.first()
            
        # Create Profile
        profile_count = Profile.objects.count()
        if profile_count == 0:
            profile = Profile.objects.create(user=user, full_name="Admin User")
            self.stdout.write(self.style.SUCCESS(f'Created Profile: {profile}'))
        
        # Create Police Stations
        station_count = PoliceStation.objects.count()
        if station_count == 0:
            stations = [
                {"name": "Central Police Station", "contact_person": "Capt. Anderson", "status": "Active", "area_id": "A-101", "address": "123 Main Street, Downtown"},
                {"name": "Westside Precinct", "contact_person": "Lt. Martinez", "status": "Active", "area_id": "B-202", "address": "456 West Avenue, Westside"},
                {"name": "North District Station", "contact_person": "Sgt. Thompson", "status": "Active", "area_id": "C-303", "address": "789 North Road, Northside"},
                {"name": "South Police Headquarters", "contact_person": "Capt. Johnson", "status": "Active", "area_id": "D-404", "address": "101 South Blvd, Southside"},
                {"name": "Eastside Police Post", "contact_person": "Lt. Williams", "status": "Active", "area_id": "E-505", "address": "202 East Street, Eastside"},
            ]
            
            for station_data in stations:
                station = PoliceStation.objects.create(**station_data)
                self.stdout.write(self.style.SUCCESS(f'Created Police Station: {station}'))
        
        # Create Crime Types
        crime_type_count = CrimeType.objects.count()
        if crime_type_count == 0:
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
                crime_type = CrimeType.objects.create(**crime_type_data)
                self.stdout.write(self.style.SUCCESS(f'Created Crime Type: {crime_type}'))
        
        # Create Officers
        officer_count = Officer.objects.count()
        if officer_count == 0:
            stations = list(PoliceStation.objects.all())
            officers = [
                {"name": "John Smith", "off_rank": "Inspector", "contact": "555-1234", "station": stations[0]},
                {"name": "Maria Rodriguez", "off_rank": "Sergeant", "contact": "555-2345", "station": stations[1]},
                {"name": "Robert Johnson", "off_rank": "Constable", "contact": "555-3456", "station": stations[2]},
                {"name": "Sarah Williams", "off_rank": "Lieutenant", "contact": "555-4567", "station": stations[3]},
                {"name": "Michael Brown", "off_rank": "Captain", "contact": "555-5678", "station": stations[4]},
                {"name": "Jennifer Davis", "off_rank": "Inspector", "contact": "555-6789", "station": stations[0]},
                {"name": "David Wilson", "off_rank": "Sergeant", "contact": "555-7890", "station": stations[1]},
                {"name": "Lisa Taylor", "off_rank": "Constable", "contact": "555-8901", "station": stations[2]}
            ]
            
            for officer_data in officers:
                officer = Officer.objects.create(**officer_data)
                self.stdout.write(self.style.SUCCESS(f'Created Officer: {officer}'))
        
        # Create Crimes linked to crime types
        crime_count = Crime.objects.count()
        if crime_count == 0:
            crime_types = list(CrimeType.objects.all())
            
            for crime_type in crime_types:
                # Create multiple crimes for each crime type
                for i in range(random.randint(2, 5)):
                    crime = Crime.objects.create(crime_type=crime_type)
                    self.stdout.write(self.style.SUCCESS(f'Created Crime: {crime}'))
        
        # Create Criminals
        criminal_count = Criminal.objects.count()
        if criminal_count == 0:
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
                {"name": "Alex Kim", "gender": "Other", "date_of_birth": "1995-06-15", "address": "808 Mystery Street, Downtown", "nationality": "Australian"},
                {"name": "Unknown Person", "gender": "Other", "date_of_birth": "1980-01-01", "address": "909 Unknown Place, Unknown", "nationality": "Unknown"}
            ]
            
            for criminal_data in criminals:
                # Convert date strings to date objects
                if criminal_data['date_of_birth']:
                    criminal_data['date_of_birth'] = datetime.strptime(criminal_data['date_of_birth'], '%Y-%m-%d').date()
                
                criminal = Criminal.objects.create(**criminal_data)
                self.stdout.write(self.style.SUCCESS(f'Created Criminal: {criminal}'))
        
        # Create criminal-crime associations
        criminal_crime_count = CriminalCrime.objects.count()
        if criminal_crime_count == 0:
            criminals = list(Criminal.objects.all())
            crimes = list(Crime.objects.all())
            
            # Assign 1-3 crimes to each criminal
            for criminal in criminals:
                selected_crimes = random.sample(crimes, k=min(random.randint(1, 3), len(crimes)))
                for crime in selected_crimes:
                    criminal_crime = CriminalCrime.objects.create(criminal=criminal, crime=crime)
                    self.stdout.write(self.style.SUCCESS(f'Created Criminal-Crime association: {criminal_crime}'))
        
        # Create FIR details if none exist
        fir_count = FIRDetail.objects.count()
        if fir_count == 0:
            crimes = list(Crime.objects.all())
            officers = list(Officer.objects.all())
            
            # Generate FIRs for the past 6 months
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=180)
            
            # Create 20 FIRs with randomly distributed dates
            for i in range(20):
                days_offset = random.randint(0, 180)
                fir_date = end_date - timedelta(days=days_offset)
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                fir_time = timezone.now().replace(hour=hour, minute=minute).time()
                
                fir = FIRDetail.objects.create(
                    description=f"FIR report #{i+1} for investigation of incident.",
                    date=fir_date,
                    time=fir_time,
                    crime=random.choice(crimes),
                    user=user,
                    officer=random.choice(officers)
                )
                self.stdout.write(self.style.SUCCESS(f'Created FIR detail: {fir}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))