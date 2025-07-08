I've prepared a detailed **Product Requirement Document (PRD)** for building a Django-based backend system. The PRD includes a full breakdown of modules, their purposes, and the associated tasks needed to implement each feature.

---

## 📘 Product Requirements Document (PRD)

### 🧾 Project Title

**BOM Management System**

---

### 🎯 Objective

To build a Django-based web application for managing Bill of Materials (BOM), including fabric and accessory/trims tracking, style-wise consumption and costing, order entry, purchase orders and receipts, and detailed reporting.

---

### 🏗️ Tech Stack

* **Backend:** Django 5.x
* **Database:** PostgreSQL (or SQLite for development)
* **Admin Interface:** Django Admin / Django Jet / Django Grappelli
* **Authentication:** Django’s built-in auth (with optional RBAC)
* **Reporting:** Django templates + HTMX/Django Tables2 (optional)
* **API Support:** Django REST Framework (if frontend is decoupled)

---

## 📂 Core Modules & Features

---

### 1. **Fabric Master**

#### Description:

Maintain the list of fabrics used in styles.

#### Tasks:

* [ ] Model: Fabric (name, code, type, GSM, width, supplier, etc.)
* [ ] CRUD operations via Django Admin or views
* [ ] Search & filter functionality

---

### 2. **Accessories / Trims Master**

#### Description:

Maintain the list of accessories/trims.

#### Tasks:

* [ ] Model: Accessories (name, code, type, supplier, usage notes)
* [ ] CRUD operations
* [ ] Filter by category/type

---

### 3. **Style-wise Fabric / Accessories Consumption**

#### Description:

Track how much fabric and accessories each style consumes.

#### Tasks:

* [ ] Model: Style (code, name, category, image)
* [ ] Model: StyleFabricConsumption (style, fabric, quantity, unit)
* [ ] Model: StyleAccessoryConsumption (style, accessory, quantity, unit)
* [ ] Views to link fabric/accessories to style
* [ ] Import/export functionality (optional)

---

### 4. **Style-wise Costing**

#### Description:

Calculate the total cost per style using consumption and rates.

#### Tasks:

* [ ] Auto-calculate cost: quantity x unit price
* [ ] Model: StyleCosting (linked to Style)
* [ ] Display breakdown by item
* [ ] Allow margin/markup configuration
* [ ] Generate costing report (PDF/HTML)

---

### 5. **Order Entry**

#### Description:

Log orders received for specific styles.

#### Tasks:

* [ ] Model: Order (order\_no, customer, style, quantity, due\_date, status)
* [ ] Auto-calculate required fabric & accessories
* [ ] View: Order list and detail page
* [ ] Status management (Pending, In Progress, Delivered)

---

### 6. **BOM (Fabric)**

#### Description:

Maintain fabric BOM entries linked to each order or style.

#### Tasks:

* [ ] Model: BOMFabric (order/style, fabric, required\_qty, issued\_qty, balance)
* [ ] Auto-populate based on order and consumption
* [ ] Allow manual adjustment
* [ ] Summary report view

---

### 7. **BOM (Accessories / Trims)**

#### Description:

Same as fabric BOM but for trims.

#### Tasks:

* [ ] Model: BOMAccessory (order/style, accessory, required\_qty, issued\_qty, balance)
* [ ] Entry view and inline edit
* [ ] BOM report with filters

---

### 8. **Purchase Order (Fabric)**

#### Description:

Create purchase orders for required fabrics.

#### Tasks:

* [ ] Model: FabricPO (po\_no, supplier, date, delivery\_date, total\_qty, status)
* [ ] Model: FabricPOItem (fabric, quantity, rate)
* [ ] Generate printable PO
* [ ] Filter by status (Open, Received, Cancelled)

---

### 9. **Purchase Receipts (Fabric)**

#### Description:

Track goods received against POs.

#### Tasks:

* [ ] Model: FabricReceipt (po\_ref, receipt\_date, GRN no)
* [ ] Model: FabricReceiptItem (fabric, quantity received, damage\_qty)
* [ ] Update inventory balance
* [ ] Report view

---

### 📊 Reports

#### 7.1 **BOM Report**

* [ ] Report view with filters: by style, by fabric, by order
* [ ] Export to PDF/CSV
* [ ] Summary and detailed formats

#### 8.1 **Purchase Order Report (Fabric)**

* [ ] Status-wise report
* [ ] Pending vs. fulfilled quantity
* [ ] Date range filter

#### 9.1 **Purchase Receipt Report (Fabric)**

* [ ] Track quantity received vs. ordered
* [ ] Highlight delays or short receipts
* [ ] Summary by supplier/fabric

---

## 👥 User Roles

| Role         | Permissions                                  |
| ------------ | -------------------------------------------- |
| Admin        | Full access                                  |
| Manager      | Can view, create, update orders and BOMs     |
| Store Keeper | Can update receipts, issue materials         |
| Viewer       | Read-only access to reports and BOM listings |

---

## 🔐 Authentication & Authorization

* Use Django auth for login/logout
* Role-based access via Django Groups
* Optional: Django Guardian for object-level permissions

---

## ✅ Deliverables

* Django Project with reusable apps:

  * `masters`: for fabric and accessory masters
  * `styles`: for style and consumption
  * `orders`: for order entry and BOMs
  * `purchase`: for PO and receipts
  * `reports`: custom reports
* Admin Panel customization
* Sample dataset for testing

---

## 🧱 Folder Structure (Example)

```
bom_project/
├── masters/
│   ├── models.py  # Fabric, Accessories
├── styles/
│   ├── models.py  # Style, Consumption, Costing
├── orders/
│   ├── models.py  # Orders, BOM
├── purchase/
│   ├── models.py  # POs, Receipts
├── reports/
│   ├── views.py   # Reporting logic
├── templates/
├── static/
├── manage.py
```

---

## 🛠️ Future Enhancements

* Email/SMS alerts for low stock or delivery deadlines
* Barcode/QR code support for fabric rolls
* Multi-location warehouse inventory
* Dashboard with KPIs (total cost, delayed POs, etc.)
* Frontend with React/Next.js or HTMX if needed

---
