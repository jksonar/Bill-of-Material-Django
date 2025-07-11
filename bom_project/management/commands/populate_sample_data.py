
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from masters.models import Fabric, Accessory, Color, Supplier
from styles.models import Style, StyleFabricConsumption, StyleAccessoryConsumption, Currency, Size
from orders.models import Order, OrderItem, StyleVariant

class Command(BaseCommand):
    help = 'Populates the database with a more extensive set of sample data for the BOM application.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate the database with extensive sample data...')

        # Clean up existing data to avoid duplicates
        self.cleanup_data()

        # Create sample data
        self.create_suppliers()
        self.create_currencies()
        self.create_sizes()
        self.create_colors()
        self.create_fabrics()
        self.create_accessories()
        self.create_styles()
        self.create_style_variants()
        self.create_consumption()
        self.create_orders()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with extensive sample data.'))

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
        Supplier.objects.all().delete()

    def create_suppliers(self):
        self.stdout.write('Creating suppliers...')
        suppliers = [
            {'name': 'Supreme Textiles', 'email': 'contact@supremetextiles.com'},
            {'name': 'Global Fabrics', 'email': 'sales@globalfabrics.com'},
            {'name': 'Future Fabrics', 'email': 'info@futurefabrics.io'},
            {'name': 'Eco-Threads', 'email': 'hello@eco-threads.com'},
            {'name': 'Luxury Looms', 'email': 'support@luxurylooms.com'},
            {'name': 'Elegant Trims', 'email': 'orders@eleganttrims.com'},
            {'name': 'ZipMaster', 'email': 'contact@zipmaster.com'},
            {'name': 'Hide & Co.', 'email': 'sales@hideandco.com'},
            {'name': 'LabelMakers Inc.', 'email': 'info@labelmakers.com'},
        ]
        for s in suppliers:
            Supplier.objects.get_or_create(name=s['name'], defaults=s)

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
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        for s in sizes:
            Size.objects.get_or_create(name=s)

    def create_colors(self):
        self.stdout.write('Creating colors...')
        colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Navy', 'Heather Grey']
        for c in colors:
            Color.objects.get_or_create(name=c)

    def create_fabrics(self):
        self.stdout.write('Creating fabrics...')
        fabrics = [
            {'name': 'Premium Cotton Jersey', 'code': 'F001', 'supplier': 'Supreme Textiles', 'unit_price': 12.50, 'construction': 'Knit'},
            {'name': 'Heavyweight Denim', 'code': 'F002', 'supplier': 'Global Fabrics', 'unit_price': 18.00, 'construction': 'Woven'},
            {'name': 'Tech Polyester', 'code': 'F003', 'supplier': 'Future Fabrics', 'unit_price': 9.50, 'construction': 'Knit'},
            {'name': 'Organic Linen', 'code': 'F004', 'supplier': 'Eco-Threads', 'unit_price': 22.00, 'construction': 'Woven'},
            {'name': 'Silk Charmeuse', 'code': 'F005', 'supplier': 'Luxury Looms', 'unit_price': 35.00, 'construction': 'Woven'},
        ]
        for f in fabrics:
            supplier = Supplier.objects.get(name=f.pop('supplier'))
            Fabric.objects.get_or_create(code=f['code'], defaults={'supplier': supplier, **f})

    def create_accessories(self):
        self.stdout.write('Creating accessories...')
        accessories = [
            {'name': 'Mother of Pearl Button', 'code': 'A001', 'supplier': 'Elegant Trims', 'price': 0.25, 'finish': 'Glossy'},
            {'name': 'YKK Zipper', 'code': 'A002', 'supplier': 'ZipMaster', 'price': 0.75, 'finish': 'Matte'},
            {'name': 'Giza Cotton Thread', 'code': 'A003', 'supplier': 'Supreme Textiles', 'price': 1.50, 'finish': 'N/A'},
            {'name': 'Leather Patch', 'code': 'A004', 'supplier': 'Hide & Co.', 'price': 2.00, 'finish': 'Embossed'},
            {'name': 'Woven Label', 'code': 'A005', 'supplier': 'LabelMakers Inc.', 'price': 0.15, 'finish': 'Satin'},
        ]
        for a in accessories:
            supplier = Supplier.objects.get(name=a.pop('supplier'))
            Accessory.objects.get_or_create(code=a['code'], defaults={'supplier': supplier, **a})

    def create_styles(self):
        self.stdout.write('Creating styles...')
        styles = [
            {'name': 'Heritage T-Shirt', 'code': 'S001', 'category': 'Tops'},
            {'name': 'Selvedge Jeans', 'code': 'S002', 'category': 'Bottoms'},
            {'name': 'Performance Polo', 'code': 'S003', 'category': 'Tops'},
            {'name': 'Linen Button-Down', 'code': 'S004', 'category': 'Shirts'},
            {'name': 'Silk Blouse', 'code': 'S005', 'category': 'Tops'},
        ]
        for s in styles:
            Style.objects.get_or_create(code=s['code'], defaults=s)

    def create_style_variants(self):
        self.stdout.write('Creating style variants...')
        styles = Style.objects.all()
        sizes = Size.objects.all()
        colors = Color.objects.all()
        for style in styles:
            for size in random.sample(list(sizes), k=random.randint(2, 4)):
                for color in random.sample(list(colors), k=random.randint(2, 4)):
                    StyleVariant.objects.get_or_create(style=style, size=size, color=color)

    def create_consumption(self):
        self.stdout.write('Creating consumption data...')
        # T-Shirt
        tshirt = Style.objects.get(code='S001')
        StyleFabricConsumption.objects.get_or_create(style=tshirt, fabric=Fabric.objects.get(code='F001'), defaults={'quantity': 1.5, 'unit': 'meters'})
        StyleAccessoryConsumption.objects.get_or_create(style=tshirt, accessory=Accessory.objects.get(code='A003'), defaults={'quantity': 100, 'unit': 'meters'})
        StyleAccessoryConsumption.objects.get_or_create(style=tshirt, accessory=Accessory.objects.get(code='A005'), defaults={'quantity': 1, 'unit': 'pieces'})

        # Jeans
        jeans = Style.objects.get(code='S002')
        StyleFabricConsumption.objects.get_or_create(style=jeans, fabric=Fabric.objects.get(code='F002'), defaults={'quantity': 2.0, 'unit': 'meters'})
        StyleAccessoryConsumption.objects.get_or_create(style=jeans, accessory=Accessory.objects.get(code='A001'), defaults={'quantity': 5, 'unit': 'pieces'})
        StyleAccessoryConsumption.objects.get_or_create(style=jeans, accessory=Accessory.objects.get(code='A002'), defaults={'quantity': 1, 'unit': 'pieces'})
        StyleAccessoryConsumption.objects.get_or_create(style=jeans, accessory=Accessory.objects.get(code='A004'), defaults={'quantity': 1, 'unit': 'pieces'})

        # Polo Shirt
        polo = Style.objects.get(code='S003')
        StyleFabricConsumption.objects.get_or_create(style=polo, fabric=Fabric.objects.get(code='F003'), defaults={'quantity': 1.8, 'unit': 'meters'})
        StyleAccessoryConsumption.objects.get_or_create(style=polo, accessory=Accessory.objects.get(code='A001'), defaults={'quantity': 3, 'unit': 'pieces'})

    def create_orders(self):
        self.stdout.write('Creating orders...')
        styles = Style.objects.all()
        customers = ['Alpha Retail', 'Bravo Wholesale', 'Charlie Corp', 'Delta Direct']
        statuses = ['Pending', 'Confirmed', 'In Production', 'Shipped', 'Cancelled']

        for i in range(1, 16):
            style = random.choice(styles)
            order = Order.objects.create(
                order_no=f'ORD{i:03}',
                customer=random.choice(customers),
                style=style,
                delivery_date=timezone.now().date() + timezone.timedelta(days=random.randint(15, 60)),
                status=random.choice(statuses)
            )
            variants = StyleVariant.objects.filter(style=style)
            if variants.exists():
                for _ in range(random.randint(1, 3)):
                    variant = random.choice(variants)
                    OrderItem.objects.create(order=order, style_variant=variant, quantity=random.randint(50, 200))
