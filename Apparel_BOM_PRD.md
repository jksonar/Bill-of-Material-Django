# Product Requirements Document (PRD) – Apparel BOM System

## 🌟 Project Name: Apparel Industry Bill of Materials (BOM) System

---

## 1. 📅 Overview
A web-based system to manage the Bill of Materials lifecycle specific to the apparel industry. This includes style-specific component management (fabric, trims), cost analysis, purchase handling, and versioned BOM reports.

---

## 2. 🔢 Key Modules & Screens (Based on Screenshots)

### 2.1 FABRIC MASTER
- Auto-generated Fabric Code (e.g., F-000001)
- Fields:
  - Description, Construction, Composition
  - Supplier, Stock-in-hand, Width, Weight, Lead Time
  - Color-wise stock and PO details
  - Image upload support
- Color matrix: multiple entries with quantity, PO, and stock

### 2.2 ACCESSORIES / TRIMS MASTER
- Auto-generated Code (e.g., A-000002)
- Fields:
  - Description, Finish, Supplier
  - Price, Weight, Unit, Lead Time
  - Stock, Color-wise tracking, Image

### 2.3 STYLEWISE FABRIC / ACCESSORIES CONSUMPTION
- Map style to components with color/size
- Fields:
  - Style Name, Item Description, Associated Items
  - Measurement (grams/meters), Costing info
  - Discount %, Retail Price

### 2.4 STYLEWISE COSTING
- Input cost components:
  - Material Cost
  - Production Cost
  - Overheads, Discounts
  - Retail/Landed Cost (multiple price entries)

### 2.5 ORDER ENTRY
- Fields:
  - Order No, Customer PO No, Delivery Date, Destination
  - Customer Name, Season, Shipment Mode
  - Size-Color-Qty grid
- Calculates total quantity and price

### 2.6 BILL OF MATERIAL (FABRIC)
- BOM based on style
- Links style to fabric usage:
  - Order quantity
  - Consumption, wastage, PO required quantity

### 2.7 BILL OF MATERIAL (ACCESSORIES/TRIMS)
- BOM for trims/accessories:
  - Per item usage, waste, PO requirement

### 2.8 BOM REPORT
- Printable/exportable report of BOM for style
- Summarizes fabric, trims with size/color/qty/wastage

### 2.9 PURCHASE ORDER (FABRIC)
- Auto-generated PO No
- Fields:
  - Supplier, Material, Color, Qty, Unit Price
  - Delivery Date, Payment Terms

### 2.10 PURCHASE ORDER REPORT
- Printable version of PO
- Includes shipping info, remarks

### 2.11 PURCHASE RECEIPTS (FABRIC)
- Fields:
  - Receipt No, Type, Date, Supplier, Reference
  - Quantity, Price, Inspector

### 2.12 PURCHASE RECEIPT REPORT
- Printable version of receipt with color, width, price, amount

---

## 3. 🔑 Roles & Permissions
| Role | Permissions |
|------|-------------|
| Admin | Full Access |
| Merchandiser | BOM, Style, Costing Management |
| Procurement | PO, Receipts, Supplier Management |
| Viewer | Read-only access to reports & listings |

---

## 4. ✅ Tasks Breakdown by Module

### 4.1 Fabric Master
- [ ] Design Fabric form UI with auto-code generation
- [ ] Implement Fabric CRUD APIs
- [ ] Enable color-wise matrix for fabric entries
- [ ] Integrate image upload feature
- [ ] Link fabric to supplier and stock tracking

### 4.2 Accessories / Trims Master
- [ ] Create trim entry screen with auto-generated code
- [ ] Implement trims CRUD APIs and service layer
- [ ] Build color-wise quantity management
- [ ] Image preview and unit/cost support

### 4.3 Stylewise Consumption
- [ ] Define size-color variants for styles
- [ ] Link components to styles with consumption units
- [ ] Input discount %, retail price, and costing basis
- [ ] Enable association of related items (e.g., bottom to top)

### 4.4 Stylewise Costing
- [ ] Cost sheet view with material, production, OH
- [ ] Enable multiple landed cost/retail price entries
- [ ] Calculation logic for cost summaries and discounts
- [ ] Add support for alternate currencies

### 4.5 BOM (Fabric and Accessories)
- [ ] Design BOM input UI for style linking
- [ ] Separate tabs for fabric and accessories
- [ ] Enable per-item wastage and consumption input
- [ ] Implement version history tracking
- [ ] Build diff/rollback view

### 4.6 BOM Report
- [ ] Generate style-specific BOM printable reports
- [ ] Include size-color matrix breakdown
- [ ] Export to PDF and Excel

### 4.7 Order Entry
- [ ] Create order form with PO fields and customer info
- [ ] Add multi-size, color, and quantity grid
- [ ] Integrate with BOM and costing for validation

### 4.8 Purchase Order
- [ ] Auto-generate PO numbers
- [ ] Select supplier, material, price, qty, delivery
- [ ] Implement editable payment terms
- [ ] Link POs to BOMs and style requirements

### 4.9 Purchase Order Report
- [ ] Create printable PO format
- [ ] Include shipping and terms details
- [ ] Add validation and remarks section

### 4.10 Purchase Receipt
- [ ] Input receipt against PO
- [ ] Record quantity, unit cost, inspector
- [ ] Mark PO as partially/fully received

### 4.11 Purchase Receipt Report
- [ ] Printable receipt with full transaction log
- [ ] Export and store with PO history

### 4.12 Admin & Roles
- [ ] Setup user roles and permissions
- [ ] Secure CRUD operations based on roles
- [ ] Add user login and session management

---

## 5. 🌐 Technology Stack
| Layer | Tool |
|-------|------|
| Frontend | Vaadin / React.js |
| Backend | Spring Boot (Java) |
| Database | PostgreSQL / MySQL |
| Reporting | JasperReports / Apache POI / iText |
| Export | PDF/Excel support |
| Auth | Spring Security / JWT |

---
