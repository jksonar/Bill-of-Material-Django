Here is your **updated PRD** for the **Apparel Industry BOM System**, now with a detailed **task list** required to complete the project. Tasks are broken down by feature/module for better tracking and assignment.

---

# ✅ Updated Product Requirements Document (PRD)

## 🎯 Project: Apparel Industry BOM (Bill of Materials) System

---

## 1. 🧭 Overview

Web-based BOM system tailored to the apparel industry to manage **styles**, **components**, **costing**, **suppliers**, **purchases**, and **reports**.

---

## 2. 🧩 Key Definitions

| Term          | Definition                                                            |
| ------------- | --------------------------------------------------------------------- |
| **BOM**       | A structured list of raw materials and components used in production. |
| **Style**     | A specific product design (e.g., T-shirt, Bikini Top).                |
| **Component** | Fabric, trims, packaging materials, etc.                              |
| **PO**        | Purchase Order                                                        |

---

## 3. 🏗️ Functional Modules & Features

### 🔹 3.1 BOM Management

* Create BOM per style (Fabric + Accessories)
* Support color/size variants
* Edit/update with version control
* Clone BOMs

### 🔹 3.2 Component Management

* **Fabric Master**: name, width, composition, supplier, pricing, stock
* **Trims Master**: similar details for accessories
* Color-wise tracking

### 🔹 3.3 Stylewise Consumption & Costing

* Input consumption & wastage per size/color
* Cost breakdown by material, overhead, production
* Retail and discount support

### 🔹 3.4 Order Entry

* Input style orders with size, quantity, destination, and customer

### 🔹 3.5 Purchase Management

* Create POs from BOMs
* Receive materials against POs
* Track balance & shortfalls

### 🔹 3.6 Reports & Export

* Generate BOM, PO, and receipt reports
* Export to PDF/Excel

---

## 4. 👥 User Roles

| Role             | Permissions        |
| ---------------- | ------------------ |
| **Admin**        | Full access        |
| **Merchandiser** | BOM & style mgmt   |
| **Procurement**  | PO & supplier mgmt |
| **Viewer**       | Report access only |

---

## 5. 🛠️ Tech Stack

* **Backend:** Django 5.x
* **Database:** PostgreSQL (or SQLite for development)
* **Admin Interface:** Django Admin / Django Jet / Django Grappelli
* **Authentication:** Django’s built-in auth (with optional RBAC)
* **Reporting:** Django templates + HTMX/Django Tables2 (optional)
* **API Support:** Django REST Framework (if frontend is decoupled)

---

## 6. ✅ Task List / Feature Breakdown

### 🔸 Phase 1: Project Setup

* [ ] Setup Git repository
* [ ] Initialize Django project
* [ ] Setup database schema (PostgreSQL production/ sqlite development)
* [ ] Configure environment (.env, profiles)

---

### 🔸 Phase 2: Master Modules

#### Fabric Master

* [ ] UI: Fabric form with auto-code
* [ ] Backend: Fabric CRUD API
* [ ] DB: Fabric table with color-wise entries

#### Accessories / Trims Master

* [ ] UI: Trims form with image & cost
* [ ] Backend: Trims CRUD
* [ ] DB: Trims table

---

### 🔸 Phase 3: Style & BOM

#### Style Management

* [ ] Style entry (name, category, description)
* [ ] Style-size-color matrix UI
* [ ] Link to BOM

#### BOM Management

* [ ] BOM creation form
* [ ] Add multiple fabrics/accessories
* [ ] Support size/color variation
* [ ] Implement BOM version history
* [ ] View BOM by style

---

### 🔸 Phase 4: Stylewise Consumption

* [ ] Consumption input per size/color
* [ ] Cost auto-calculation
* [ ] Add landed cost, production cost, overhead
* [ ] Calculate total cost with discount

---

### 🔸 Phase 5: Order Entry

* [ ] Order creation form (style, color, size)
* [ ] Validate against BOM
* [ ] Track order value & status

---

### 🔸 Phase 6: Purchase Management

#### Purchase Orders

* [ ] PO generation from BOMs
* [ ] Supplier selection
* [ ] Track quantity, price, delivery date

#### Purchase Receipts

* [ ] Receive material against PO
* [ ] Enter received quantity, price
* [ ] Link with inspection records

---

### 🔸 Phase 7: Reports & Exports

* [ ] BOM report by style
* [ ] Costing report per style/version
* [ ] PO and receipt report by date or supplier
* [ ] Export BOM, PO, and receipts to PDF
* [ ] Export to Excel using Apache POI

---

### 🔸 Phase 8: Security & Roles

* [ ] Setup user roles (Admin, Merchandiser, Procurement, Viewer)
* [ ] Role-based access control
* [ ] Login/logout flow

---

### 🔸 Phase 9: Finalization

* [ ] Testing & validation
* [ ] UAT deployment
* [ ] Production deployment
* [ ] Backup & documentation

---
