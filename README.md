# PC Build Planner & Part Compatibility

A Django-based web application for planning, managing, and optimizing PC builds with component compatibility tracking.

## Features

✓ **Build Management**: Create and manage multiple PC builds with separate budgets  
✓ **Component Library**: Browse and select from a comprehensive database of PC components  
✓ **Budget Tracking**: Monitor total budget, used budget, and remaining funds  
✓ **Part Management**: Add, swap, and remove components from builds  
✓ **Authorization**: Only build creators can edit their own builds  
✓ **Responsive Design**: Beautiful UI built with Bootstrap 5  
✓ **Django Admin**: Full admin interface for managing parts and builds  

## Project Structure

```
pc_builder/                          # Main Django project
├── settings.py                      # Django settings
├── urls.py                          # Main URL configuration
└── ...

builds/                              # Main app for PC builds
├── models.py                        # Database models
├── views.py                         # View logic
├── forms.py                         # Django forms
├── admin.py                         # Admin configuration
├── urls.py                          # App URL patterns
├── templatetags/
│   └── custom_filters.py            # Custom template filters
├── migrations/                      # Database migrations
└── templates/builds/                # App templates

templates/                           # Project-wide templates
├── base.html                        # Base template
└── home.html                        # Home page

scripts/                             # Utility scripts
├── create_sample_parts.py          # Load sample PC components
└── set_admin_password.py           # Set admin user password

manage.py                            # Django management script
db.sqlite3                           # SQLite database
.venv/                               # Python virtual environment
```

## Models

### 1. **Part**
Represents a PC component (CPU, GPU, RAM, PSU, etc.)

**Fields:**
- `name` (CharField): Component name
- `part_type` (CharField): Type of part (CPU, GPU, RAM, SSD, HDD, PSU, CASE, MOTHERBOARD, COOLER, OTHER)
- `wattage` (IntegerField): Power consumption (optional)
- `price` (DecimalField): Component cost
- `created_at` & `updated_at` (DateTimeField): Timestamps

### 2. **PCBuild**
Represents a complete PC build configuration

**Fields:**
- `name` (CharField): Build name
- `total_budget` (DecimalField): Budget limit for the build
- `notes` (TextField): Additional notes and comments
- `creator` (ForeignKey): User who created the build
- `created_at` & `updated_at` (DateTimeField): Timestamps

**Methods:**
- `get_total_cost()`: Calculate total cost of all parts
- `get_remaining_budget()`: Calculate remaining budget

### 3. **BuildItem**
Links Parts to PCBuilds (many-to-many with metadata)

**Fields:**
- `pc_build` (ForeignKey): Reference to PCBuild
- `part` (ForeignKey): Reference to Part
- `quantity` (IntegerField): Number of this part in the build
- `added_at` (DateTimeField): When part was added

**Constraints:**
- Unique combination of pc_build and part

## Views & URLs

### Build Management
- `GET /builds/` - **BuildListView**: List all user's builds
- `GET/POST /builds/create/` - **BuildCreateView**: Create new build
- `GET /builds/<id>/` - **BuildDetailView**: View build with all parts
- `GET/POST /builds/<id>/edit/` - **BuildUpdateView**: Edit build details
- `GET/POST /builds/<id>/delete/` - **BuildDeleteView**: Delete build

### Part Management
- `GET/POST /builds/<id>/add-part/` - **AddPartToBuildView**: Add parts to build
- `GET/POST /builds/item/<id>/edit/` - **UpdateBuildItemView**: Swap/update parts
- `GET/POST /builds/item/<id>/delete/` - **DeleteBuildItemView**: Remove parts
- `GET /builds/api/parts/` - **parts_api**: API for dynamic part loading

## Authorization

The application implements role-based authorization:
- **Login Required**: All build management requires authentication
- **Owner-based Access**: `UserIsOwnerMixin` ensures only the build creator can edit/delete
- **Automatic Creator Assignment**: Build creator is automatically set when creating

## Credentials

Default admin account created:
- **Username**: `admin`
- **Password**: `admin123`

## How to Use

### 1. **Access the Application**
```
http://localhost:8000
```

### 2. **Login**
- Click "Login" on the home page
- Or navigate to: `http://localhost:8000/admin/`
- Use credentials above

### 3. **Create a PC Build**
- Click "Create Build" button
- Fill in build name, total budget, and notes
- Click "Create Build"

### 4. **Add Components**
- On build detail page, click "+ Add Part"
- Select a component from the dropdown
- Set quantity
- Click "Add Part to Build"

### 5. **Manage Components**
- **Swap Part**: Click "Swap" on a component to replace it
- **Remove Part**: Click "Remove" to delete from build
- **Budget Tracking**: View remaining budget in real-time

### 6. **Edit or Delete Build**
- Click "Edit Build" to modify name, budget, or notes
- Click "Delete Build" to remove the entire build

## Admin Interface

Access admin at: `http://localhost:8000/admin/`

**Admin Features:**
- Add/edit/delete Parts
- View all builds and build items
- Filter by type, creator, date
- Search by name

## Sample Data

17 pre-loaded hardware components are included:
- CPUs: Intel Core i9-13900K, AMD Ryzen 9 7950X
- GPUs: RTX 4090, RTX 4070, AMD RX 7900 XTX
- RAM: Corsair, G.Skill DDR5 options
- Storage: Samsung 990 Pro, WD Black NVMe
- Power Supplies: 850W-1000W options
- Cases: NZXT H9 Flow, Lian Li Lancool
- Motherboards: MSI Z790, ASUS ROG options
- Coolers: Noctua NH-D15, NZXT Kraken

## Development

### Install Dependencies
```bash
pip install Django==4.2.11 python-decouple==3.8
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Populate Sample Data
```bash
python scripts/create_sample_parts.py
```

### Start Development Server
```bash
python manage.py runserver
```

## Key Technologies

- **Framework**: Django 4.2.11
- **Database**: SQLite (default, easily switchable)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Python**: 3.14+

## Custom Template Filters

- `mul`: Multiply two values (e.g., `price|mul:quantity`)
- `currency`: Format as currency (e.g., `value|currency`)

## Security Features

✓ CSRF protection on all forms  
✓ SQL injection prevention via ORM  
✓ Login required for protected views  
✓ Authorization checks for ownership  
✓ Secure password hashing  

## Future Enhancement Ideas

- Advanced search and filtering
- Part compatibility checker
- Price history and trend tracking
- Wishlist/comparison features
- Export builds to PDF
- Share builds with users
- Reviews and ratings system
- API for mobile apps

## Support

For issues or questions, check:
1. Django documentation: https://docs.djangoproject.com/
2. Admin panel for direct data management
3. Terminal output for debug information

---

**Created**: April 2026  
**Last Updated**: April 13, 2026
