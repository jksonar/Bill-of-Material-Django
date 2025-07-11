# Apparel Industry BOM (Bill of Materials) System

This project is a web-based Bill of Materials (BOM) system tailored to the apparel industry. It helps manage styles, components, costing, suppliers, purchases, and reports.

## Overview

The system provides a centralized platform for managing the entire lifecycle of apparel production, from design and material sourcing to order management and reporting. It aims to streamline workflows, improve accuracy, and provide real-time visibility into the production process.

## Key Features

*   **BOM Management:** Create, edit, and clone BOMs per style, with support for color and size variants.
*   **Component Management:** Maintain a master list of fabrics and accessories, including details like suppliers, pricing, and stock levels.
*   **Stylewise Consumption & Costing:** Input material consumption and wastage per size and color, and automatically calculate the cost of production.
*   **Order Entry:** Record customer orders with details like style, size, quantity, and destination.
*   **Purchase Management:** Generate purchase orders (POs) from BOMs, track material receipts, and manage supplier information.
*   **Reports & Export:** Generate various reports, including BOMs, POs, and receipts, and export them to PDF or Excel.

## User Roles

The system supports the following user roles:

*   **Admin:** Full access to all features and settings.
*   **Merchandiser:** Manages BOMs and styles.
*   **Procurement:** Manages POs and suppliers.
*   **Viewer:** Can only view reports.

## Tech Stack

*   **Backend:** Django 5.x
*   **Database:** PostgreSQL (production) / SQLite (development)
*   **Admin Interface:** Django Admin
*   **Authentication:** Django's built-in authentication system
*   **Reporting:** Django templates

## Getting Started

To get started with the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/jksonar/Bill-of-Material-Django.git
cd your-project
pip install -r requirements.txt
```

Then, apply the database migrations and run the development server:

```bash
python manage.py migrate
python manage.py runserver
```

You can now access the application at `http://localhost:8000`.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.
