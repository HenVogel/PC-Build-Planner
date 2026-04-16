# Quick Start Guide

## Getting Started in 2 Minutes

### 1. Access the Application
Open your browser and go to:
```
http://localhost:8000
```

### 2. Log In
- Click the **"Login"** button in the top right
- Use these credentials:
  - **Username**: `admin`
  - **Password**: `admin123`

### 3. View Your Builds
After logging in, you'll see "My Builds" page. It's empty initially!

### 4. Create Your First Build
1. Click the **"+ Create Build"** button (top right or home page)
2. Fill in:
   - **Build Name**: e.g., "Gaming PC 2026"
   - **Total Budget**: e.g., $3000
   - **Notes** (optional): e.g., "For 4K gaming"
3. Click **"Create Build"**
4. You'll be taken to the build details page

### 5. Add PC Components
1. Click **"+ Add Part"** button
2. From the dropdown, select a component, e.g., "Intel Core i9-13900K"
3. Set **Quantity** (usually 1)
4. Click **"Add Part to Build"**

The component appears in your build with:
- Component name
- Type (CPU, GPU, RAM, etc.)
- Quantity
- Price per unit
- Total price for this component

### 6. Monitor Your Budget
The budget info shows:
- **Total Budget**: How much you allocated
- **Used**: Total cost of all parts you've added
- **Remaining**: Budget left (goes red if over budget)
- **% Used**: Visual representation of budget usage

### 7. Swap Parts (Better Deal Found?)
1. Find a part you want to replace
2. Click the **"Swap"** button on that row
3. Select a different part from the dropdown
4. Click **"Update Part"**

The total cost and remaining budget update automatically!

### 8. Remove Parts
- Click **"Remove"** on any part to take it out of the build
- The budget recalculates instantly

### 9. Manage Your Builds
From the "My Builds" page:
- **View Details**: Click to see all parts in a build
- **Edit Build**: Click to change the build name, budget, or notes
- **Delete Build**: Click to remove the entire build

---

## Available PC Components (Sample Data)

Your system comes pre-loaded with 17 high-end PC parts:

**Processors (CPUs):**
- Intel Core i9-13900K ($599.99)
- AMD Ryzen 9 7950X ($549.99)

**Graphics Cards (GPUs):**
- NVIDIA RTX 4090 ($1999.99)
- NVIDIA RTX 4070 ($699.99)
- AMD RX 7900 XTX ($899.99)

**Memory (RAM):**
- Corsair Vengeance 32GB DDR5 ($149.99)
- G.Skill Trident Z 64GB DDR5 ($299.99)

**Storage (SSDs):**
- Samsung 990 Pro 1TB ($119.99)
- WD Black SN850X 2TB ($199.99)

**Power Supplies (PSUs):**
- Corsair RM1000e 1000W ($179.99)
- EVGA SuperNOVA 850W ($129.99)

**Cases:**
- NZXT H9 Flow ($129.99)
- Lian Li Lancool 216 ($89.99)

**Motherboards:**
- MSI Z790 Edge WiFi ($299.99)
- ASUS ROG STRIX X870-E ($349.99)

**CPU Coolers:**
- Noctua NH-D15 ($89.99)
- NZXT Kraken X73 360mm ($179.99)

---

## Tips & Tricks

💡 **Multi-Part Builds**: Add multiple components of the same type (e.g., 2 SSDs, 3 case fans)

💡 **Budget Planning**: Start with expensive parts (GPU, CPU) then fill in the rest

💡 **Price Comparison**: Try multiple GPU options to see which fits your budget

💡 **Keep Notes**: Use the Notes field to explain your build strategy

💡 **Full Flexibility**: Budget exceeded? The system allows it - great for planning!

---

## Admin Panel (Advanced)

If you want to manage parts or view all data:
1. Go to: `http://localhost:8000/admin/`
2. Log in with the same admin credentials
3. You can:
   - Add new PC components
   - View/edit all builds and parts
   - Manage users
   - Track database statistics

---

## Common Tasks

### Scenario: Building a Gaming PC with $2000 Budget

1. **Create Build**: "Gaming Beast 2024" with $2000 budget
2. **Add GPU**: RTX 4070 ($699.99)
3. **Add CPU**: Intel Core i9 ($599.99)
4. **Add RAM**: Corsair 32GB ($149.99)
5. **Add Storage**: Samsung 990 Pro 1TB ($119.99)
6. **Add PSU**: EVGA 850W ($129.99)
7. **Add Case**: NZXT H9 Flow ($129.99)
8. **Total**: $1929.94 ✓ **Remaining**: $70.06

### Scenario: Optimizing Your Budget

1. View your build (shows you're over budget by $500)
2. Click "Swap" on the most expensive part
3. Choose a cheaper alternative
4. Check updated budget
5. Repeat if needed!

---

## Troubleshooting

**Q: Can't see my builds?**  
A: Make sure you're logged in. Click "Login" at the top right.

**Q: Parts dropdown empty?**  
A: Parts should auto-load. Try refreshing the page.

**Q: Budget calculation wrong?**  
A: Refresh the page. Budget recalculates when you add/remove/swap parts.

**Q: Forgot password?**  
A: Contact your administrator or reset in Django admin.

**Q: Want to add new parts?**  
A: Go to Admin panel (link in top menu) and add them there.

---

## Next Steps

1. ✓ Log in
2. ✓ Create a build
3. ✓ Add components
4. ✓ Optimize your budget
5. 📖 Check **README.md** for technical details
6. 🧪 See **TESTING.md** for comprehensive testing guide

---

**Happy Building! 🖥️🚀**
