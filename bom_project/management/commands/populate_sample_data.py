
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from masters.models import Fabric, Accessory, Color
from styles.models import Style, StyleFabricConsumption, StyleAccessoryConsumption, Currency, Size
from orders.models import Order, OrderItem, StyleVariant

class Command(BaseCommand):
    help = 'Populates the database with sample data for the BOM application.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate the database with sample data...')

        # Clean up existing data to avoid duplicates
        self.cleanup_data()

        # Create sample data
        self.create_currencies()
        self.create_sizes()
        self.create_colors()
        self.create_fabrics()
        self.create_accessories()
        self.create_styles()
        self.create_style_variants()
        self.create_consumption()
        self.create_orders()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data.'))

    def cleanup_data(self):
        self.stdout.write('Cleaning up old data...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        StyleFabricConsumption.objects.all().delete()
        StyleAccessoryConsumption.objects.all().delete()
        StyleVariant.objects.all().delete()
        Style.objects.all().delete()
        Accessory.objects.all().delete()
        Fabric.objects.all().delete()
        Color.objects.all().delete()
        Size.objects.all().delete()
        Currency.objects.all().delete()

    def create_currencies(self):
        self.stdout.write('Creating currencies...')
        currencies = [
            {'name': 'US Dollar', 'code': 'USD'},
            {'name': 'Euro', 'code': 'EUR'},
            {'name': 'Indian Rupee', 'code': 'INR'},
        ]
        for c in currencies:
            Currency.objects.get_or_create(**c)

    def create_sizes(self):
        self.stdout.write('Creating sizes...')
        sizes = ['Small', 'Medium', 'Large', 'X-Large']
        for s in sizes:
            Size.objects.get_or_create(name=s)

    def create_colors(self):
        self.stdout.write('Creating colors...')
        colors = ['Red', 'Blue', 'Green', 'Black', 'White']
        for c in colors:
            Color.objects.get_or_create(name=c)

    def create_fabrics(self):
        self.stdout.write('Creating fabrics...')
        fabrics = [
            {'name': 'Cotton Jersey', 'code': 'F001', 'supplier': 'ABC Textiles', 'unit_price': 10.50},
            {'name': 'Denim', 'code': 'F002', 'supplier': 'Global Fabrics', 'unit_price': 15.00},
            {'name': 'Polyester', 'code': 'F003', 'supplier': 'ABC Textiles', 'unit_price': 8.00},
        ]
        for f in fabrics:
            Fabric.objects.get_or_create(name=f['name'], defaults=f)

    def create_accessories(self):
        self.stdout.write('Creating accessories...')
        accessories = [
            {'name': 'Button', 'code': 'A001', 'supplier': 'XYZ Trims', 'price': 0.10},
            {'name': 'Zipper', 'code': 'A002', 'supplier': 'XYZ Trims', 'price': 0.50},
            {'name': 'Thread', 'code': 'A003', 'supplier': 'ABC Textiles', 'price': 1.00},
        ]
        for a in accessories:
            Accessory.objects.get_or_create(name=a['name'], defaults=a)

    def create_styles(self):
        self.stdout.write('Creating styles...')
        styles = [
            {'name': 'Classic T-Shirt', 'code': 'S001', 'category': 'Tops'},
            {'name': 'Jeans', 'code': 'S002', 'category': 'Bottoms'},
            {'name': 'Polo Shirt', 'code': 'S003', 'category': 'Tops'},
        ]
        for s in styles:
            Style.objects.get_or_create(code=s['code'], defaults=s)

    def create_style_variants(self):
        self.stdout.write('Creating style variants...')
        styles = Style.objects.all()
        sizes = Size.objects.all()
        colors = Color.objects.all()
        for style in styles:
            for size in random.sample(list(sizes), k=2):
                for color in random.sample(list(colors), k=2):
                    StyleVariant.objects.get_or_create(style=style, size=size, color=color)

    def create_consumption(self):
        self.stdout.write('Creating consumption data...')
        tshirt = Style.objects.get(code='S001')
        jeans = Style.objects.get(code='S002')

        StyleFabricConsumption.objects.get_or_create(
            style=tshirt, fabric=Fabric.objects.get(code='F001'),
            defaults={'quantity': 1.5, 'unit': 'meters'}
        )
        StyleAccessoryConsumption.objects.get_or_create(
            style=tshirt, accessory=Accessory.objects.get(code='A003'),
            defaults={'quantity': 100, 'unit': 'meters'}
        )

        StyleFabricConsumption.objects.get_or_create(
            style=jeans, fabric=Fabric.objects.get(code='F002'),
            defaults={'quantity': 2.0, 'unit': 'meters'}
        )
        StyleAccessoryConsumption.objects.get_or_create(
            style=jeans, accessory=Accessory.objects.get(code='A001'),
            defaults={'quantity': 5, 'unit': 'pieces'}
        )
        StyleAccessoryConsumption.objects.get_or_create(
            style=jeans, accessory=Accessory.objects.get(code='A002'),
            defaults={'quantity': 1, 'unit': 'pieces'}
        )

    def create_orders(self):
        self.stdout.write('Creating orders...')
        style = Style.objects.first()
        order = Order.objects.create(
            order_no='ORD001',
            customer='Sample Customer',
            style=style,
            delivery_date=timezone.now().date(),
            status='Pending'
        )
        variant = StyleVariant.objects.filter(style=style).first()
        if variant:
            OrderItem.objects.create(order=order, style_variant=variant, quantity=100)
