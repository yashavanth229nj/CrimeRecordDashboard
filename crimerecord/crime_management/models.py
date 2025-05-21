from django.db import models

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"Admin {self.admin_id}"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User {self.user_id}"

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Profile {self.profile_id}"

class PoliceStation(models.Model):
    station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    area_id = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Officer(models.Model):
    officer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    off_rank = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class CrimeType(models.Model):
    crime_type_id = models.AutoField(primary_key=True)
    crime_type_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.crime_type_name

class Crime(models.Model):
    crime_id = models.AutoField(primary_key=True)
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Crime {self.crime_id} - {self.crime_type}"

class FIRDetail(models.Model):
    fir_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"FIR {self.fir_id} - {self.date}"

class Criminal(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    criminal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name

class CriminalCrime(models.Model):
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('criminal', 'crime'),)
    
    def __str__(self):
        return f"{self.criminal} - {self.crime}"

class ProfileCriminal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('profile', 'criminal'),)
    
    def __str__(self):
        return f"{self.profile} - {self.criminal}"
