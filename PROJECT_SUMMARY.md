# PC Build Planner

Django web application for creating and managing PC builds with budget tracking.

## Models

**Part** - PC components (name, type, wattage, price, timestamps)
**PCBuild** - User builds (name, budget, notes, creator, auto-calculated totals)
**BuildItem** - Part-to-build relationship with quantity and cost tracking

## Features

- Create/Read/Update/Delete operations for builds and parts
- Dashboard listing all user builds with budget summaries
- Add, swap, and remove components from builds
- Real-time budget calculations and color-coded status
- Owner-only authorization for build management
- Form validation and Bootstrap 5 responsive UI
- Admin interface for part management
- 23 pre-loaded PC components (CPUs, GPUs, RAM, SSDs, PSUs, Cases, Motherboards, Coolers)

## Technology

Backend: Django 4.2.11, Python 3.14+, SQLite, Django ORM
Frontend: Bootstrap 5.3, HTML5, CSS3
Security: CSRF protection, SQL injection prevention, XSS protection, authorization checks

## Quick Start

1. Activate virtual environment: `.venv\Scripts\activate`
2. Load sample data: `python scripts/parts.py`
3. Run server: `python manage.py runserver`
4. Visit: `http://localhost:8000` (Login: admin/admin123)

## Key Features

- Budget color-coding (green/red status)
- Responsive card design for all devices
- Real-time budget calculations
- Owner-based authorization with multi-user support
- Admin interface for data management
- Custom template filters for price calculations
