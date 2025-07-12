# Apparel BOM Management System

## Overview

This project is a web-based Bill of Materials (BOM) management system designed specifically for the apparel industry. It provides a comprehensive solution for managing the entire lifecycle of a product, from initial design and costing to purchase order management and reporting.

## Key Features

*   **Master Data Management:** Maintain centralized records for fabrics, accessories, and suppliers.
*   **Style Management:** Define product styles, including their components, consumption, and costing.
*   **Order Management:** Create and track customer orders with detailed size and color specifications.
*   **BOM Generation:** Automatically generate versioned BOMs based on style and order requirements.
*   **Purchasing:** Manage the procurement process with purchase orders and receipts.
*   **Reporting:** Generate a variety of reports, including BOM summaries, costing analysis, and purchase order tracking.
*   **User Management:** Secure the system with role-based access control for administrators, merchandisers, and procurement staff.

## Technology Stack

*   **Backend:** Django
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap, HTMX
*   **Database:** SQLite (for development), PostgreSQL (recommended for production)
*   **Libraries:**
    *   `django-guardian` for object-level permissions
    *   `django-htmx` for dynamic and interactive pages
    *   `Pillow` for image processing
    *   `reportlab` and `openpyxl` for PDF and Excel reporting
    *   `django-tables2` and `django-filter` for sortable and filterable tables
    *   `django-crispy-forms` and `crispy-bootstrap5` for beautifully rendered forms

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/django-bom.git
    cd django-bom
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7.  **Access the application** at `http://localhost:8000` in your web browser.

## Usage

*   **Admin:** Access the admin interface at `http://localhost:8000/admin/` to manage users, groups, and permissions.
*   **Application:** Use the main application to manage masters, styles, orders, and purchases.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.