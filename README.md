# Apparel Industry BOM (Bill of Materials) System

A comprehensive web-based BOM system tailored for the apparel industry to manage styles, components, costing, suppliers, purchases, and reports.

## 🚀 Features

### Core Modules

#### 1. **Master Data Management**
- **Supplier Management**: Complete supplier database with contact details, payment terms, and lead times
- **Fabric Master**: Comprehensive fabric management with auto-generated codes, supplier linking, and color-wise tracking
- **Accessories/Trims Master**: Detailed accessory management with categories, units, and supplier information
- **Color Management**: Centralized color database with hex codes

#### 2. **Style & BOM Management**
- **Style Creation**: Style entry with categories, descriptions, and associated styles
- **Size/Color Matrix**: Support for multiple size and color variants
- **BOM Creation**: Create detailed BOMs with fabric and accessory consumption
- **Version Control**: Track BOM versions with change history
- **Wastage Calculation**: Built-in wastage percentage for accurate costing

#### 3. **Advanced Costing System**
- **Multi-level Costing**: Material, production, overhead, and shipping costs
- **Currency Support**: Multi-currency with exchange rates
- **Margin & Discount**: Configurable markup and discount calculations
- **Size/Color Specific**: Costing per size and color variant
- **Auto-calculation**: Real-time cost updates based on consumption

#### 4. **Order Management**
- **Order Entry**: Complete order management with customer details
- **BOM Generation**: Automatic BOM calculation from orders
- **Quantity Tracking**: Track ordered vs. required quantities
- **Status Management**: Order lifecycle tracking

#### 5. **Purchase Management**
- **Fabric Purchase Orders**: Complete PO management for fabrics
- **Accessory Purchase Orders**: Separate PO system for accessories
- **Supplier Integration**: Link POs to supplier database
- **Receipt Management**: Track material receipts with inspection notes
- **Status Tracking**: Monitor PO status from draft to completion

#### 6. **Reports & Analytics**
- **BOM Reports**: Detailed BOM reports by style and version
- **Costing Reports**: Comprehensive cost analysis
- **Purchase Reports**: PO and receipt tracking
- **Export Options**: PDF and Excel export capabilities
- **Template System**: Customizable report templates

#### 7. **User Management & Security**
- **Role-Based Access**: Admin, Merchandiser, Procurement, and Viewer roles
- **Permission System**: Granular permissions per module
- **Audit Logging**: Track all system changes
- **Session Management**: Monitor user sessions

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (development) / PostgreSQL (production)
- **UI Framework**: Bootstrap 5 with Crispy Forms
- **Tables**: Django Tables2 with filtering
- **Reports**: ReportLab (PDF) + OpenPyXL (Excel)
- **Authentication**: Django's built-in auth + Django Guardian
- **Real-time**: Django HTMX for dynamic interactions

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_BOM
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## 📋 User Roles & Permissions

### Admin
- Full system access
- User management
- System configuration
- All CRUD operations

### Merchandiser
- Style and BOM management
- Costing and consumption
- Order entry
- View suppliers and materials

### Procurement
- Purchase order management
- Supplier management
- Material receipts
- Inventory tracking

### Viewer
- Read-only access to all modules
- Report generation
- Data export

## 🗂️ Project Structure

```
django_BOM/
├── bom_project/          # Main project settings
├── masters/              # Master data (Suppliers, Fabrics, Accessories)
├── styles/               # Style and BOM management
├── orders/               # Order management
├── purchase/             # Purchase orders and receipts
├── reports/              # Report generation
├── dashboard/            # Main dashboard
├── user_management/      # User roles and permissions
├── static/               # Static files
├── media/                # User uploads
├── reports_output/       # Generated reports
└── requirements.txt      # Dependencies
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=your-domain.com
```

### Database Configuration
For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bom_production',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Key Features Implemented

### ✅ Enhanced Models
- **Supplier Model**: Complete supplier management
- **Enhanced Fabric/Accessory**: Better categorization and tracking
- **Size/Color Variants**: Support for style variations
- **Advanced Costing**: Multi-level cost calculation
- **Purchase Management**: Comprehensive PO system

### ✅ User Management
- **Role-based Access Control**: Four distinct user roles
- **Permission System**: Granular permissions
- **Audit Logging**: Track all changes
- **Session Management**: Monitor user activity

### ✅ Reporting System
- **Template Engine**: Customizable report templates
- **Multiple Formats**: PDF, Excel, CSV export
- **Report Generation**: Async report processing
- **BOM Reports**: Detailed material requirements

### ✅ Enhanced UI/UX
- **Bootstrap 5**: Modern, responsive design
- **Crispy Forms**: Beautiful form rendering
- **Django Tables**: Sortable, filterable tables
- **HTMX Integration**: Dynamic interactions

## 🚀 Next Steps

### Phase 1: Core Enhancements
- [ ] Implement advanced search and filtering
- [ ] Add bulk operations for data management
- [ ] Create dashboard analytics
- [ ] Implement notification system

### Phase 2: Advanced Features
- [ ] API development with DRF
- [ ] Mobile-responsive improvements
- [ ] Advanced reporting with charts
- [ ] Integration with external systems

### Phase 3: Production Readiness
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Backup and recovery
- [ ] Monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for the Apparel Industry**
