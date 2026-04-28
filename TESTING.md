# Testing Guide

## Pre-Testing Checklist

- Server running on http://localhost:8000
- Admin credentials: admin / admin123
- 23 sample parts loaded
- Database migrations applied

## Test Scenarios

### 1. Authentication & Login

- Access `/builds/` without login → redirected to login page
- Log in with admin / admin123 → successful login
- View builds dashboard after login

### 2. Create Build

- Click "Create Build"
- Fill: name, budget ($3000), notes
- Submit → build created, detail page shown

### 3. Build List

- Navigate to `/builds/`
- See all user builds in card layout
- Cards show: name, budget, used, remaining, % used

### 4. Build Detail

- Click build → see detail page
- Display: name, notes, budget breakdown
- Show "+ Add Part" button
- Show "Edit Build" and "Delete Build" buttons

### 5. Add Parts to Build

- Click "+ Add Part"
- Select component from dropdown (e.g., Intel i9)
- Set quantity: 1
- Submit → part added to build
- Table shows: part name, type, qty, price, total

### 6. Add Multiple Parts

Example of parts:
- Add CPU: $
- Add GPU: $
- Add RAM: $
- Total Cost: $
- Remaining: $

### 7. Budget Tracking

- Add parts exceeding budget
- Remaining budget shows in red (negative)
- System still allows adding (flexible planning)

### 8. Swap Parts

- Click "Swap" on any part
- Select different component
- Submit → part replaced
- Budget recalculates

### 9. Update Quantity

- Click "Swap" on a part
- Change quantity field
- Submit → quantity updated
- Total price recalculates

### 10. Remove Parts

- Click "Remove" on a part
- Confirm → part deleted
- Budget updates automatically

### 11. Edit Build

- Click "Edit Build"
- Change: name, budget, notes
- Submit → changes saved

### 12. Delete Build

- Click "Delete Build"
- Confirm deletion
- Build removed from list

### 13. Authorization (Owner-Only)

- Create build as admin
- Create another user in admin panel
- Log in as new user
- Try accessing other user's build edit URL
- Access denied (403 or unauthorized message)

### 14. Admin Panel

- Visit `/admin/`
- View Parts list (23 items)
- Filter parts by type
- Search parts by name
- View/edit PCBuilds
- View/edit BuildItems

### 15. Model Data

- Admin → Parts: verify 23 sample parts loaded
- Admin → PCBuilds: verify created builds appear
- Admin → BuildItems: verify items match builds

### 16. UI Responsiveness

- View on desktop → full layout
- View on tablet → responsive
- View on mobile → stacked layout
- Navigation collapse on small screens

### 17. Form Validation

- Try submit empty create form → validation errors
- Try negative budget → validation error
- Try invalid quantity → validation error
- All required fields show error messages

### 18. Navigation

- Navbar links work: Home, My Builds, Create Build, Admin, Logout
- Logo → home page
- "Back" buttons return to previous page

### 19. Success Messages

- Create build → success message shown
- Update build → success message shown
- Delete part → success message shown
- Messages disappear after action

### 20. Performance

- Pages load within 1 second
- Budget calculations instant
- No console errors

---

## Security Testing

#### Test 14.1: CSRF Protection
- Submit form normally
- **Expected**: CSRF token handled automatically

#### Test 14.2: SQLi Prevention
- Try searching with SQL: `' OR '1'='1`
- **Expected**: ORM prevents injection

#### Test 14.3: XSS Prevention
- Add notes with: `<script>alert('xss')</script>`
- **Expected**: HTML escaped in template

---

## Summary Checklist

- All 3 models created and working
- 3+ views implemented (List, Create, Update, Delete)
- Authorization working (only creator can edit)
- Budget tracking accurate
- Parts can be added, swapped, removed
- Forms validation working
- Admin interface functional
- Sample data loaded
- UI responsive and user-friendly
- All CRUD operations functional

---

## Known Limitations (By Design)

- Single-user builds only (can enhance with permissions)
- SQLite database (fine for development, upgrade for production)
- No part compatibility checking (future feature)
- No image uploads for parts (future feature)

---
