# PC Build Planner

PC Build Planner is a Django web app for creating and managing custom PC builds with budget tracking, wattage guidance, and per-user ownership controls.

## Features

- Build dashboard with pagination
- Create, edit, and delete builds
- Add, update, and remove build parts
- Budget calculations (total, remaining, percent used)
- Wattage calculations with PSU recommendation
- Public/private builds via `is_public`
- Favorites for builds and parts
- Custom auth pages: login, signup, profile
- Django admin for full data management

## Tech Stack

- Python
- Django 6.0.4
- django-crispy-forms + crispy-bootstrap5
- SQLite (default)
- Pillow (image uploads)

## Quick Start

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Create an admin user

```bash
python manage.py createsuperuser
```

Optional: if you created an `admin` user and want the dev password:

```bash
python scripts/set_admin_password.py
```

This sets the `admin` account password to `superpassword`.

### 5. Load sample parts

```bash
python scripts/create_sample_parts.py
```

### 6. Run the server

```bash
python manage.py runserver
```

Open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## Core Models

### Part

Represents hardware components.

Key fields:

- `name`, `manufacturer`
- `part_type` (CPU, GPU, RAM, SSD, HDD, PSU, CASE, MOTHERBOARD, COOLER, OTHER)
- `wattage`, `price`, `status`
- `description`, `image`
- `favorited_by`

### PCBuild

Represents a user build.

Key fields:

- `name`, `slug`
- `total_budget`, `notes`, `description`
- `image`, `is_public`
- `creator`, `favorited_by`

Utility methods include:

- `get_total_cost()`
- `get_remaining_budget()`
- `get_total_wattage()`
- `get_recommended_psu()`
- `get_budget_percentage()`

### BuildItem

Join model between `PCBuild` and `Part`.

Key fields:

- `pc_build`, `part`
- `quantity`
- `added_at`

Constraint:

- Unique pair of `pc_build` and `part`

## Main Routes

### Project

- `/` home page
- `/admin/` Django admin

### Authentication

- `/builds/auth/login/`
- `/builds/auth/logout/`
- `/builds/auth/signup/`
- `/builds/auth/profile/`

### Builds

- `/builds/` list your builds
- `/builds/create/` create build
- `/builds/<slug>/` build detail (preferred)
- `/builds/<pk>/` legacy detail route
- `/builds/<slug>/edit/`
- `/builds/<slug>/delete/`
- `/builds/<slug>/add-part/`
- `/builds/item/<item_pk>/edit/`
- `/builds/item/<item_pk>/delete/`

### API Endpoints

- `/builds/api/parts/`
- `/builds/api/toggle-favorite-build/<slug>/`
- `/builds/api/toggle-favorite-part/<pk>/`

## Authorization Rules

- Most build management requires login.
- Only the creator can edit/delete a build or its items.
- Build detail pages are viewable by the owner or when `is_public` is true.

## Project Layout

```text
pc_builder/               Django project settings and root URLs
builds/                   Main app (models, views, forms, urls, admin)
builds/templates/builds/  Build-specific templates
builds/migrations/        Database migrations
builds/templatetags/      Custom template filters
templates/                Global templates (home, base, auth, errors)
static/                   CSS and images
media/                    Uploaded images
scripts/                  Utility scripts for setup and sample data
```

## Useful Commands

```bash
python manage.py check
python manage.py test
python manage.py makemigrations
python manage.py migrate
```

## Notes

- Current settings are development-oriented (`DEBUG=True` in settings).
- Sample data script is idempotent (`update_or_create`), so it is safe to rerun.

## Additional Docs

- `QUICK_START.md` for a user walkthrough
- `TESTING.md` for manual test scenarios
- `PROJECT_SUMMARY.md` for project scope and status
