# Crime Record Management System

A Django-based web application for managing crime records, connecting to an existing MySQL database.

## Features

- Admin dashboard with crime statistics visualization
- Management of Police Stations, Officers, Crime Types, and Criminals
- FIR (First Information Report) recording and management
- User profiles and criminal records
- Responsive design with professional UI for law enforcement users

## Tech Stack

- **Backend**: Python 3.x, Django 4.x, MySQL
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript, Chart.js
- **Database**: MySQL (existing schema)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd CrimeRecordDashboard
```

2. Create and activate a virtual environment:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

4. Database Setup:
   - Create a MySQL database named 'crimerecord':
   ```powershell
   mysql -u root -p
   ```
   - In the MySQL console, run:
   ```sql
   CREATE DATABASE IF NOT EXISTS crimerecord CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   exit
   ```
   - Configure database settings in `crimerecord/crimerecord/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'crimerecord',
           'USER': 'root',
           'PASSWORD': 'your_password',  # Replace with your MySQL password
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       }
   }
   ```

5. Run database migrations:
```powershell
cd crimerecord
python manage.py migrate
```

6. Populate the database with sample data:
```powershell
python manage.py populate_dummy_data
```

7. Create a superuser for admin access:
```powershell
python manage.py createsuperuser
```

8. Run the development server:
```powershell
python manage.py runserver
```

9. Access the application:
   - Main website: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## User Guide

### Login
- Use the credentials created during superuser setup
- Or register a new account

### Dashboard
- View crime statistics and visualizations
- Access quick links to all management sections

### Management Sections
- **Police Stations**: Add, edit, or delete police station records
- **Officers**: Manage officer information and assignments
- **Crime Types**: Categorize different types of crimes
- **Crimes**: Record crime incidents
- **FIR Details**: Manage First Information Reports
- **Criminals**: Track criminal records and crime associations

### Settings
- Update your user profile
- Change password
- Configure system preferences

## Database Structure
The application uses the following main models:
- Admin
- User
- Profile
- PoliceStation
- Officer
- CrimeType
- Crime
- FIRDetail
- Criminal
- CriminalCrime (junction between criminals and crimes)

## Connecting with MySQL Workbench
To manage the database directly using MySQL Workbench:
1. Open MySQL Workbench
2. Create a new connection with:
   - Connection Name: CrimeRecordDashboard
   - Hostname: localhost
   - Port: 3306
   - Username: root
   - Password: Your MySQL password
   - Default Schema: crimerecord

## Troubleshooting
- If you encounter a "no module named mysqlclient" error, ensure it's installed correctly:
  ```powershell
  pip install mysqlclient
  ```
- Database connection issues:
  - Verify MySQL service is running
  - Confirm database credentials in settings.py are correct
  - Ensure the crimerecord database exists
