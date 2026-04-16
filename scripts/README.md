# Utility Scripts

This folder contains helper scripts for setting up and maintaining the PC Build Planner application.

## Scripts

### `create_sample_parts.py`
Loads sample PC components into the database.

**Usage:**
```bash
python scripts/create_sample_parts.py
```

**What it does:**
- Creates 17 sample PC components
- Includes CPUs, GPUs, RAM, SSDs, PSUs, Cases, Motherboards, and Coolers
- Uses Django ORM for safe database insertion

### `set_admin_password.py`
Sets the password for the admin user account.

**Usage:**
```bash
python scripts/set_admin_password.py
```

**What it does:**
- Sets admin user password to 'admin123'
- Uses Django's password hashing for security

## Running Scripts

All scripts should be run from the project root directory:

```bash
cd path/to/Python_Final_Project
python scripts/script_name.py
```

The scripts automatically configure the Django environment and database connection.
