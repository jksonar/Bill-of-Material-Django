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

* [x] Model: Fabric (name, code, type, GSM, width, supplier, etc.)
* [x] CRUD operations via Django Admin or views
* [x] Search & filter functionality

---

### 2. **Accessories / Trims Master**

#### Description:

Maintain the list of accessories/trims.

#### Tasks:

* [x] Model: Accessories (name, code, type, supplier, usage notes)
* [x] CRUD operations
* [x] Filter by category/type

---

### 3. **Style-wise Fabric / Accessories Consumption**

#### Description:

Track how much fabric and accessories each style consumes.

#### Tasks:

* [x] Model: Style (code, name, category, image)
* [x] Model: StyleFabricConsumption (style, fabric, quantity, unit)
* [x] Model: StyleAccessoryConsumption (style, accessory, quantity, unit)
* [x] Views to link fabric/accessories to style
* [ ] Import/export functionality (optional)

---

### 4. **Style-wise Costing**

#### Description:

Calculate the total cost per style using consumption and rates.

#### Tasks:

* [x] Auto-calculate cost: quantity x unit price
* [x] Model: StyleCosting (linked to Style)
* [x] Display breakdown by item
* [x] Allow margin/markup configuration
* [ ] Generate costing report (PDF/HTML)

---

### 5. **Order Entry**

#### Description:

Log orders received for specific styles.

#### Tasks:

* [x] Model: Order (order\_no, customer, style, quantity, due\_date, status)
* [x] Auto-calculate required fabric & accessories
* [x] View: Order list and detail page
* [x] Status management (Pending, In Progress, Delivered)

---

### 6. **BOM (Fabric)**

#### Description:

Maintain fabric BOM entries linked to each order or style.

#### Tasks:

* [x] Model: BOMFabric (order/style, fabric, required\_qty, issued\_qty, balance)
* [x] Auto-populate based on order and consumption
* [x] Allow manual adjustment
* [x] Summary report view

---

### 7. **BOM (Accessories / Trims)**

#### Description:

Same as fabric BOM but for trims.

#### Tasks:

* [x] Model: BOMAccessory (order/style, accessory, required\_qty, issued\_qty, balance)
* [x] Entry view and inline edit
* [x] BOM report with filters

---

### 8. **Purchase Order (Fabric)**

#### Description:

Create purchase orders for required fabrics.

#### Tasks:

* [x] Model: FabricPO (po\_no, supplier, date, delivery\_date, total\_qty, status)
* [x] Model: FabricPOItem (fabric, quantity, rate)
* [x] Generate printable PO
* [x] Filter by status (Open, Received, Cancelled)

---

### 9. **Purchase Receipts (Fabric)**

#### Description:

Track goods received against POs.

#### Tasks:

* [x] Model: FabricReceipt (po\_ref, receipt\_date, GRN no)
* [x] Model: FabricReceiptItem (fabric, quantity received, damage\_qty)
* [x] Update inventory balance
* [x] Report view

---

### 📊 Reports

#### 7.1 **BOM Report**

* [x] Report view with filters: by style, by fabric, by order
* [x] Export to PDF/CSV
* [x] Summary and detailed formats

#### 8.1 **Purchase Order Report (Fabric)**

* [x] Status-wise report
* [x] Pending vs. fulfilled quantity
* [x] Date range filter

#### 9.1 **Purchase Receipt Report (Fabric)**

* [x] Track quantity received vs. ordered
* [x] Highlight delays or short receipts
* [x] Summary by supplier/fabric

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

* [x] Use Django auth for login/logout
* [x] Role-based access via Django Groups
* [ ] Optional: Django Guardian for object-level permissions

---

## ✅ Deliverables

* Django Project with reusable apps:

  * `masters`: for fabric and accessory masters
  * `styles`: for style and consumption
  * `orders`: for order entry and BOMs
  - `purchase`: for PO and receipts
  * [x] `reports`: custom reports
* [x] Admin Panel customization
* [ ] Sample dataset for testing

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

* [ ] Email/SMS alerts for low stock or delivery deadlines
* [ ] Barcode/QR code support for fabric rolls
* [ ] Multi-location warehouse inventory
* [ ] Dashboard with KPIs (total cost, delayed POs, etc.)
* [ ] Frontend with React/Next.js or HTMX if needed

---
