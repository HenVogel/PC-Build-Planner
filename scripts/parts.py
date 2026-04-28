import os
import sys
import django

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_builder.settings')
django.setup()

from builds.models import Part
from decimal import Decimal

# Sample parts data with new fields
sample_parts = [
    # CPUs
    {
        'name': 'Intel Core i9-12900K',
        'part_type': 'CPU',
        'wattage': 125,
        'price': Decimal('352.70'),
        'manufacturer': 'Intel',
        'status': 'IN_STOCK',
        'description': '16-core/24-thread processor. High performance for gaming and workstations.'
    },
    {
        'name': 'Intel Core i9-12900KF',
        'part_type': 'CPU',
        'wattage': 125,
        'price': Decimal('329.00'),
        'manufacturer': 'Intel',
        'status': 'IN_STOCK',
        'description': '16-core/24-thread processor without integrated graphics. Great value option.'
    },
    {
        'name': 'AMD Ryzen 9 9950X3D',
        'part_type': 'CPU',
        'wattage': 170,
        'price': Decimal('657.00'),
        'manufacturer': 'AMD',
        'status': 'IN_STOCK',
        'description': '16-core/32-thread processor with 3D V-Cache. Excellent for gaming and content creation.'
    },
    {
        'name': 'AMD Ryzen 9 9950X',
        'part_type': 'CPU',
        'wattage': 170,
        'price': Decimal('499.00'),
        'manufacturer': 'AMD',
        'status': 'IN_STOCK',
        'description': '16-core/32-thread processor. Strong all-around performance for productivity and gaming.'
    },
    # GPUs
    {
        'name': 'NVIDIA RTX 4090',
        'part_type': 'GPU',
        'wattage': 450,
        'price': Decimal('1,999.99'),
        'manufacturer': 'NVIDIA',
        'status': 'IN_STOCK',
        'description': 'Flagship GPU with 16384 CUDA cores. Ultimate gaming and professional performance.'
    },
    {
        'name': 'NVIDIA RTX 4070',
        'part_type': 'GPU',
        'wattage': 200,
        'price': Decimal('699.99'),
        'manufacturer': 'NVIDIA',
        'status': 'IN_STOCK',
        'description': 'Mid-range GPU with 5888 CUDA cores. Great for 1440p and 4K gaming.'
    },
    {
        'name': 'AMD RX 7900 XTX',
        'part_type': 'GPU',
        'wattage': 420,
        'price': Decimal('899.99'),
        'manufacturer': 'AMD',
        'status': 'IN_STOCK',
        'description': 'RDNA 3 flagship with 24GB VRAM. Competitive 4K gaming performance.'
    },
    # RAM
    {
        'name': 'Corsair Dominator Titanium RGB 32GB (2x16GB)',
        'part_type': 'RAM',
        'wattage': 5,
        'price': Decimal('215.00'),
        'manufacturer': 'Corsair',
        'status': 'IN_STOCK',
        'description': 'DDR5-7000 high-performance memory. Premium RGB lighting for gaming builds.'
    },
    {
        'name': 'G.Skill Trident Z5 RGB 64GB (2x32GB)',
        'part_type': 'RAM',
        'wattage': 7,
        'price': Decimal('340.00'),
        'manufacturer': 'G.Skill',
        'status': 'IN_STOCK',
        'description': 'DDR5-6400 memory kit. Maximum capacity for streaming and content creation.'
    },
    # SSDs
    {
        'name': 'Samsung 9100 Pro 2TB',
        'part_type': 'SSD',
        'wattage': 8,
        'price': Decimal('478.00'),
        'manufacturer': 'Samsung',
        'status': 'IN_STOCK',
        'description': 'PCIe Gen 5 NVMe drive. Fastest storage speeds with peak performance.'
    },
    {
        'name': 'WD Black SN8100 1TB',
        'part_type': 'SSD',
        'wattage': 7,
        'price': Decimal('285.00'),
        'manufacturer': 'Western Digital',
        'status': 'IN_STOCK',
        'description': 'PCIe Gen 5 NVMe drive. High-speed performance for gaming and creative work.'
    },
    {
        'name': 'Crucial T710 2TB',
        'part_type': 'SSD',
        'wattage': 11,
        'price': Decimal('323.00'),
        'manufacturer': 'Crucial',
        'status': 'IN_STOCK',
        'description': 'PCIe Gen 5 NVMe drive with excellent speeds. Great capacity for large projects.'
    },
    # Power Supplies
    {
        'name': 'Corsair RM1000x Shift',
        'part_type': 'PSU',
        'wattage': 1000,
        'price': Decimal('199.99'),
        'manufacturer': 'Corsair',
        'status': 'IN_STOCK',
        'description': 'ATX 3.1 1000W modular PSU. Latest standard with excellent efficiency.'
    },
    {
        'name': 'Seasonic Focus GX-850',
        'part_type': 'PSU',
        'wattage': 850,
        'price': Decimal('149.99'),
        'manufacturer': 'Seasonic',
        'status': 'IN_STOCK',
        'description': '80+ Gold 850W modular PSU. Reliable power with good efficiency.'
    },
    {
        'name': 'MSI MAG A750GL PCIE5',
        'part_type': 'PSU',
        'wattage': 750,
        'price': Decimal('109.99'),
        'manufacturer': 'MSI',
        'status': 'IN_STOCK',
        'description': 'ATX 3.0 750W modular PSU. Supports PCIe 5.0 graphics cards.'
    },
    # Cases
    {
        'name': 'Corsair FRAME 4000D',
        'part_type': 'CASE',
        'wattage': None,
        'price': Decimal('129.99'),
        'manufacturer': 'Corsair',
        'status': 'IN_STOCK',
        'description': 'Mid-tower case with excellent airflow. Clean design with tempered glass.'
    },
    {
        'name': 'Cooler Master COSMOS Alpha',
        'part_type': 'CASE',
        'wattage': None,
        'price': Decimal('549.00'),
        'manufacturer': 'Cooler Master',
        'status': 'IN_STOCK',
        'description': 'Full-tower case with premium build quality. Perfect for high-end builds.'
    },
    {
        'name': 'Lian Li O11 Dynamic EVO XL',
        'part_type': 'CASE',
        'wattage': None,
        'price': Decimal('234.99'),
        'manufacturer': 'Lian Li',
        'status': 'IN_STOCK',
        'description': 'Dual-chamber case for excellent cable management. Popular among enthusiasts.'
    },
    # Motherboards
    {
        'name': 'ASUS ROG Strix X870E-E Gaming WiFi',
        'part_type': 'MOTHERBOARD',
        'wattage': 60,
        'price': Decimal('499.00'),
        'manufacturer': 'ASUS',
        'status': 'IN_STOCK',
        'description': 'AM5 socket flagship motherboard. Premium features with DDR5 and PCIe 5.0.'
    },
    {
        'name': 'MSI MAG Z790 Tomahawk WiFi',
        'part_type': 'MOTHERBOARD',
        'wattage': 55,
        'price': Decimal('259.99'),
        'manufacturer': 'MSI',
        'status': 'IN_STOCK',
        'description': 'LGA 1700 motherboard for 13th gen Intel. Excellent balance of features and value.'
    },
    # CPU Coolers
    {
        'name': 'Noctua NH-D15 G2',
        'part_type': 'COOLER',
        'wattage': 2,
        'price': Decimal('180.00'),
        'manufacturer': 'Noctua',
        'status': 'IN_STOCK',
        'description': 'Dual-tower air cooler. Quiet and efficient for high-end processors.'
    },
    {
        'name': 'Thermalright Peerless Assassin 120 SE',
        'part_type': 'COOLER',
        'wattage': 2,
        'price': Decimal('36.00'),
        'manufacturer': 'Thermalright',
        'status': 'IN_STOCK',
        'description': 'Budget air cooler with excellent performance. Great value option.'
    },
    {
        'name': 'Arctic Liquid Freezer III Pro 360',
        'part_type': 'COOLER',
        'wattage': 12,
        'price': Decimal('115.00'),
        'manufacturer': 'Arctic',
        'status': 'IN_STOCK',
        'description': '360mm AIO liquid cooler. Excellent cooling performance for flagship CPUs.'
    },
]

# Create or update parts with new fields
part_names = [part_data['name'] for part_data in sample_parts]

# Delete parts not in the current list
Part.objects.exclude(name__in=part_names).delete()

# Create or update parts in the list
for part_data in sample_parts:
    part, created = Part.objects.update_or_create(
        name=part_data['name'],
        defaults={
            'part_type': part_data['part_type'],
            'wattage': part_data['wattage'],
            'price': part_data['price'],
            'manufacturer': part_data['manufacturer'],
            'status': part_data['status'],
            'description': part_data['description'],
        }
    )
    if created:
        print(f"✓ Created: {part.name}")
    else:
        print(f"↻ Updated: {part.name}")

print(f"\nTotal parts in database: {Part.objects.count()}")
