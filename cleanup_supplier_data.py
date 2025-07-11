import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bom_project.settings')
django.setup()

print("Schema for masters_fabric:")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(masters_fabric);")
    for row in cursor.fetchall():
        print(row)

print("\nSchema for masters_accessory:")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(masters_accessory);")
    for row in cursor.fetchall():
        print(row)

