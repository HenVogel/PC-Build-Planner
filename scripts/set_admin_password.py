import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_builder.settings')
django.setup()

from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('superpassword')
user.save()
print("Admin password set to 'admin123'")
