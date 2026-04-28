# PC Build Planner

Django web app for creating and managing custom PC builds with budget tracking.

## Features

- Create, edit, delete builds
- Add, update, remove build components
- Real-time budget calculations
- Owner-only access control
- Django admin for data management

## Setup

### 1. Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
# Or set password for existing admin user:
python scripts/set_admin_password.py
```

### 5. Load Sample Parts

```bash
python scripts/parts.py
```

### 6. Run Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Models

**Part**: Hardware components (name, type, wattage, price, description)

**PCBuild**: User's build (name, budget, notes, creator)

**BuildItem**: Links parts to builds (quantity, cost tracking)

## Routes

**Build Management:**
- `/builds/` - List user's builds
- `/builds/create/` - Create build
- `/builds/<slug>/` - View build details
- `/builds/<slug>/edit/` - Edit build
- `/builds/<slug>/delete/` - Delete build
- `/builds/<slug>/add-part/` - Add part to build

**Auth:**
- `/builds/auth/login/` - Login
- `/builds/auth/signup/` - Signup
- `/builds/auth/logout/` - Logout

**Admin:**
- `/admin/` - Django admin

## Authorization

- Login required for all build operations
- Only creator can edit/delete their builds
- All operations checked via UserIsOwnerMixin

## Tech Stack

- Python 3.14+
- Django 4.2.11
- SQLite
- Bootstrap 5
- django-crispy-forms

## Useful Commands

```bash
python manage.py check           # Validate setup
python manage.py test            # Run tests
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
```

## Documentation

- `QUICK_START.md` - User walkthrough
- `TESTING.md` - Test scenarios
- `PROJECT_SUMMARY.md` - Project overview
