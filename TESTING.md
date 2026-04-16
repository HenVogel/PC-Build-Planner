# PC Build Planner - Testing Guide

This document provides comprehensive testing scenarios to verify all project requirements.

## Pre-Testing Checklist

✓ Server running on http://localhost:8000  
✓ Admin credentials ready (admin / admin123)  
✓ 17 sample parts loaded in database  
✓ Database migrations applied  

---

## Test Scenarios

### 1. Authentication & Authorization

#### Test 1.1: Login Required
- [ ] Attempt to access `/builds/` without logging in
- **Expected**: Redirected to login page
- [ ] Log in with admin / admin123
- **Expected**: Redirected to build list

#### Test 1.2: Owner-Only Editing
- [ ] Log in as admin
- [ ] Create Build #1 (name: "Gaming PC")
- [ ] Create another user (use Django admin)
- [ ] Log out and log in as new user
- [ ] Try to access `/builds/<id>/edit/` where id is admin's build
- **Expected**: Access denied (403 or similar)

---

### 2. Build Management (ListView, CreateView, UpdateView)

#### Test 2.1: Create Build (CreateView)
- [ ] Click "Create Build" button
- [ ] Fill in:
  - Build Name: "High-End Gaming Build"
  - Total Budget: $3500
  - Notes: "For 4K gaming at 120fps"
- [ ] Click "Create Build"
- **Expected**: Build created, redirected to build detail page, success message shown

#### Test 2.2: Build List (ListView)
- [ ] Navigate to `/builds/`
- **Expected**: Display all user's builds in card format with:
  - Build name
  - Total budget ($3500)
  - Used cost (initially $0)
  - Remaining budget (initially $3500)
  - Creation date
  - "View Details" button

#### Test 2.3: Build Detail View
- [ ] Click "View Details" on a build
- **Expected**: See:
  - Build name and notes
  - Budget breakdown (Total, Used, Remaining, % Used)
  - Empty components table with "+ Add Part" button
  - Edit Build and Delete Build buttons

#### Test 2.4: Update Build (UpdateView)
- [ ] Click "Edit Build"
- [ ] Change:
  - Name to "Ultimate Gaming Build 2024"
  - Budget to $4000
  - Notes to "Updated for better performance"
- [ ] Click "Update Build"
- **Expected**: Changes saved, redirected to detail page, success message

---

### 3. Part Management (CreateView with Links)

#### Test 3.1: Add Part to Build
- [ ] On build detail page, click "+ Add Part"
- [ ] Select: "NVIDIA RTX 4090" (CPU category could be changed, this is GPU)
- [ ] Set Quantity: 1
- [ ] Click "Add Part to Build"
- **Expected**: 
  - Part added to build
  - Table now shows: RTX 4090 | GPU | 1 | $1999.99 | $1999.99
  - Total Cost updated to $1999.99
  - Remaining Budget updated to $2000.01

#### Test 3.2: Add Multiple Parts
- [ ] Click "+ Add Part" again
- [ ] Select: "Intel Core i9-13900K"
- [ ] Quantity: 1
- [ ] Click "Add"
- **Expected**: 
  - Second part added
  - Total Cost now $2599.98
  - Remaining Budget $900.02
  - Both parts visible in table

#### Test 3.3: Add Part with Quantity > 1
- [ ] Click "+ Add Part"
- [ ] Select: "Samsung 990 Pro 1TB NVMe"
- [ ] Quantity: 2
- [ ] Click "Add"
- **Expected**: 
  - Shows Quantity column with "2"
  - Total Price = $119.99 × 2 = $239.98

---

### 4. Part Swap/Update (UpdateView)

#### Test 4.1: Swap Part
- [ ] In build detail, find "RTX 4090" part
- [ ] Click "Swap" button
- [ ] Select different GPU: "NVIDIA RTX 4070" ($699.99)
- [ ] Click "Update Part"
- **Expected**: 
  - Part replaced in table
  - Total Cost recalculated
  - Remaining Budget updated
  - Confirmation message shown

#### Test 4.2: Update Quantity
- [ ] Find "Samsung 990 Pro" (currently qty 2)
- [ ] Click "Swap" button
- [ ] Change Quantity to 3
- [ ] Click "Update Part"
- **Expected**: 
  - Quantity updated to 3
  - Total Price = $119.99 × 3 = $359.97
  - Budget recalculated

---

### 5. Part Removal (DeleteView)

#### Test 5.1: Remove Part from Build
- [ ] Find any part in the build
- [ ] Click "Remove" button
- [ ] Confirm deletion
- **Expected**: 
  - Part removed from table
  - Total Cost decreased
  - Remaining Budget increased
  - Confirmation message shown

#### Test 5.2: Remove All Parts
- [ ] Remove all remaining parts one by one
- **Expected**: 
  - Build becomes empty
  - Total Cost = $0
  - Remaining Budget = Total Budget
  - Message: "No parts added yet"

---

### 6. Budget Tracking

#### Test 6.1: Budget Alert
- [ ] Create a new build with Budget: $500
- [ ] Add parts totaling > $500
- **Expected**: 
  - Warning alert appears: "Budget exceeded by $X"
  - Remaining Budget shows negative in red
  - Still allows adding more (for flexibility)

#### Test 6.2: Budget Calculation
- [ ] Create build with Budget: $2000
- [ ] Add:
  - CPU: $599.99
  - GPU: $699.99
  - RAM: $149.99
- **Expected**: 
  - Total Cost: $1449.97
  - Remaining: $550.03
  - Progress: 72.5%

---

### 7. Build Deletion (DeleteView)

#### Test 7.1: Delete Build
- [ ] Navigate to build detail
- [ ] Click "Delete Build"
- [ ] Confirm deletion
- **Expected**: 
  - Build and all parts removed
  - Redirected to build list
  - Build no longer appears in list
  - Confirmation message shown

---

### 8. Models & Database

#### Test 8.1: Part Model
- [ ] Admin panel → Parts
- [ ] Verify 17 sample parts exist
- **Expected**: 
  - All parts show: name, type, wattage (if applicable), price
  - Filtering by part_type works
  - Search by name works

#### Test 8.2: PCBuild Model
- [ ] Admin panel → PC Builds
- [ ] Verify builds created in tests appear
- **Expected**: 
  - Shows: name, creator, budget, created_at
  - Filtering by creator works
  - Ordering by creation date

#### Test 8.3: BuildItem Model
- [ ] Admin panel → Build Items
- [ ] Verify items added appear
- **Expected**: 
  - Shows: build name, part name, quantity
  - Filtering works
  - Unique constraint (same part can't be added twice to same build)

---

### 9. Authorization Edge Cases

#### Test 9.1: Direct URL Access
- [ ] Create Build A as User 1
- [ ] Log in as User 2
- [ ] Try direct URL: `/builds/<Build A id>/edit/`
- **Expected**: 403 Forbidden or redirected

#### Test 9.2: Try Claiming Others' Builds
- [ ] Log in as admin
- [ ] Verify only admin's builds show in `/builds/`
- **Expected**: Other users' builds hidden

---

### 10. UI/UX Testing

#### Test 10.1: Responsive Design
- [ ] View on desktop, tablet, mobile
- **Expected**: 
  - Bootstrap layout responsive
  - Navigation collapse on small screens
  - Tables scroll on mobile

#### Test 10.2: Form Validation
- [ ] Try submitting empty form
- **Expected**: Error messages for required fields

#### Test 10.3: Success Messages
- [ ] Perform operations: create, update, delete
- **Expected**: 
  - Success messages appear
  - Messages auto-dismiss or have close button
  - Correct operation confirmed

---

### 11. Navigation Testing

#### Test 11.1: Navigation Menu
- [ ] Verify navbar links:
  - [ ] "My Builds" → `/builds/`
  - [ ] "Create Build" → `/builds/create/`
  - [ ] "Admin" → admin panel
  - [ ] "Logout" → logout and redirect
  - [ ] Logo → home page

#### Test 11.2: Breadcrumbs/Return Links
- [ ] Check "Back to Builds" button on detail
- **Expected**: Returns to `/builds/`
- [ ] Check "Cancel" button on forms
- **Expected**: Returns to previous page

---

### 12. Admin Interface

#### Test 12.1: Admin CRUD Operations
- [ ] Add new part via admin
- [ ] Edit existing part
- [ ] Delete a part
- **Expected**: Changes reflected in application

#### Test 12.2: Admin Filters
- [ ] Filter parts by type
- [ ] Filter builds by creator
- **Expected**: Correct filtering applied

---

## Performance Testing

#### Test 13.1: Page Load Times
- [ ] Check all pages load within reasonable time
- **Expected**: < 1 second on localhost

#### Test 13.2: Database Queries
- [ ] Enable Django Debug Toolbar (optional)
- [ ] Monitor query count
- **Expected**: No N+1 queries

---

## Security Testing

#### Test 14.1: CSRF Protection
- [ ] Submit form normally
- **Expected**: CSRF token handled automatically

#### Test 14.2: SQLi Prevention
- [ ] Try searching with SQL: `' OR '1'='1`
- **Expected**: ORM prevents injection

#### Test 14.3: XSS Prevention
- [ ] Add notes with: `<script>alert('xss')</script>`
- **Expected**: HTML escaped in template

---

## Summary Checklist

- [ ] All 3 models created and working
- [ ] 3+ views implemented (List, Create, Update, Delete)
- [ ] Authorization working (only creator can edit)
- [ ] Budget tracking accurate
- [ ] Parts can be added, swapped, removed
- [ ] Forms validation working
- [ ] Admin interface functional
- [ ] Sample data loaded
- [ ] UI responsive and user-friendly
- [ ] All CRUD operations functional

---

## Known Limitations (By Design)

- Single-user builds only (can enhance with permissions)
- SQLite database (fine for development, upgrade for production)
- No part compatibility checking (future feature)
- No image uploads for parts (future feature)

---

**Test Date**: ________________  
**Tester**: ________________  
**Status**: ☐ PASS ☐ FAIL

