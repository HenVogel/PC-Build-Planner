import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_builder.settings')
django.setup()

from builds.models import Part
from decimal import Decimal

# Sample parts data with new fields
sample_parts = [
    # CPUs
    {
        'name': 'Intel Core i9-13900K',
        'part_type': 'CPU',
        'wattage': 253,
        'price': Decimal('599.99'),
        'manufacturer': 'Intel',
        'status': 'IN_STOCK',
        'description': '24-core flagship processor with Raptor Lake architecture. DDR5 and PCIe 5.0 support.'
    },
    {
        'name': 'AMD Ryzen 9 7950X',
        'part_type': 'CPU',
        'wattage': 162,
        'price': Decimal('549.99'),
        'manufacturer': 'AMD',
        'status': 'IN_STOCK',
        'description': '16-core processor with Zen 4 architecture. Excellent thermal efficiency and gaming performance.'
    },
    # GPUs
    {
        'name': 'NVIDIA RTX 4090',
        'part_type': 'GPU',
        'wattage': 450,
        'price': Decimal('1999.99'),
        'manufacturer': 'NVIDIA',
        'status': 'IN_STOCK',
        'description': 'Ada Lovelace GPU with 16384 CUDA cores. Ultimate gaming and professional compute performance.'
    },
    {
        'name': 'NVIDIA RTX 4070',
        'part_type': 'GPU',
        'wattage': 200,
        'price': Decimal('699.99'),
        'manufacturer': 'NVIDIA',
        'status': 'IN_STOCK',
        'description': 'Mid-range Ada GPU with 5888 CUDA cores. Great 1440p and 4K gaming performance.'
    },
    {
        'name': 'AMD RX 7900 XTX',
        'part_type': 'GPU',
        'wattage': 420,
        'price': Decimal('899.99'),
        'manufacturer': 'AMD',
        'status': 'IN_STOCK',
        'description': 'RDNA 3 flagship with 24GB VRAM. Competitive 4K gaming and excellent value.'
    },
    # RAM
    {
        'name': 'Corsair Vengeance 32GB DDR5',
        'part_type': 'RAM',
        'wattage': None,
        'price': Decimal('149.99'),
        'manufacturer': 'Corsair',
        'status': 'IN_STOCK',
        'description': '32GB DDR5 6000MHz kit. Fast, reliable performance with excellent RGB lighting.'
    },
    {
        'name': 'G.Skill Trident Z 64GB DDR5',
        'part_type': 'RAM',
        'wattage': None,
        'price': Decimal('299.99'),
        'manufacturer': 'G.Skill',
        'status': 'IN_STOCK',
        'description': '64GB DDR5 6000MHz kit. Maximum memory for content creation and streaming.'
    },
    # SSDs
    {
        'name': 'Samsung 990 Pro 1TB NVMe',
        'part_type': 'SSD',
        'wattage': None,
        'price': Decimal('119.99'),
        'manufacturer': 'Samsung',
        'status': 'IN_STOCK',
        'description': 'PCIe 4.0 NVMe with 7400MB/s reads. Enterprise-grade reliability in consumer form factor.'
    },
    {
        'name': 'WD Black SN850X 2TB',
        'part_type': 'SSD',
        'wattage': None,
        'price': Decimal('199.99'),
        'manufacturer': 'Western Digital',
        'status': 'IN_STOCK',
        'description': '2TB PCIe 4.0 drive with 7100MB/s reads. Great for gaming and creative professionals.'
    },
    # Power Supplies
    {
        'name': 'Corsair RM1000e 1000W',
        'part_type': 'PSU',
        'wattage': 1000,
        'price': Decimal('179.99'),
        'manufacturer': 'Corsair',
        'status': 'IN_STOCK',
        'description': '1000W Fully Modular 80+ Gold. Quiet, efficient power delivery with 12-year warranty.'
    },
    {
        'name': 'EVGA SuperNOVA 850W',
        'part_type': 'PSU',
        'wattage': 850,
        'price': Decimal('129.99'),
        'manufacturer': 'EVGA',
        'status': 'IN_STOCK',
        'description': '850W Fully Modular 80+ Gold. Excellent value with exceptional build quality.'
    },
    # Cases
    {
        'name': 'NZXT H9 Flow',
        'part_type': 'CASE',
        'wattage': None,
        'price': Decimal('129.99'),
        'manufacturer': 'NZXT',
        'status': 'IN_STOCK',
        'description': 'Mid-tower ATX case with excellent airflow design and tempered glass front.'
    },
    {
        'name': 'Lian Li Lancool 216',
        'part_type': 'CASE',
        'wattage': None,
        'price': Decimal('89.99'),
        'manufacturer': 'Lian Li',
        'status': 'IN_STOCK',
        'description': 'Budget-friendly ATX case with solid airflow and clean internal layout.'
    },
    # Motherboards
    {
        'name': 'MSI Z790 Edge WiFi',
        'part_type': 'MOTHERBOARD',
        'wattage': None,
        'price': Decimal('299.99'),
        'manufacturer': 'MSI',
        'status': 'IN_STOCK',
        'description': 'Z790 socket for 13th gen Intel. PCIe 5.0, DDR5 support, WiFi 6E included.'
    },
    {
        'name': 'ASUS ROG STRIX X870-E',
        'part_type': 'MOTHERBOARD',
        'wattage': None,
        'price': Decimal('349.99'),
        'manufacturer': 'ASUS',
        'status': 'IN_STOCK',
        'description': 'X870-E socket for Ryzen 7000 series. Premium features with DDR5 and PCIe 5.0.'
    },
    # CPU Coolers
    {
        'name': 'Noctua NH-D15',
        'part_type': 'COOLER',
        'wattage': None,
        'price': Decimal('89.99'),
        'manufacturer': 'Noctua',
        'status': 'IN_STOCK',
        'description': 'Dual-tower air cooler. Quiet, efficient, supports most Intel/AMD sockets.'
    },
    {
        'name': 'NZXT Kraken X73 360mm',
        'part_type': 'COOLER',
        'wattage': None,
        'price': Decimal('179.99'),
        'manufacturer': 'NZXT',
        'status': 'IN_STOCK',
        'description': '360mm AIO liquid cooler with smart RGB and CAM software control.'
    },
]

# Create or update parts with new fields
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
