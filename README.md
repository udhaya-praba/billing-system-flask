# Billing System

A simple FastAPI-based billing system with a vanilla JavaScript frontend and SQLite database for managing products, bills, and denominations.

## Features

- **Product Management**: Create, read, update, and delete products.
- **Bill Generation**: Create bills with multiple items and automatic tax calculation.
- **Denomination Management**: Manage shop denominations and calculate balance denominations.
- **Customer Purchase History**: View all purchases by a customer.
- **Stock Management**: Automatic stock deduction when bills are created.

## Project Structure

```
billing-system-flask-main/
├── frontend/
│   ├── index.html          # Main page for creating bills
│   ├── products.html       # Page for managing products
│   ├── bills.html          # Page for viewing all bills
│   └── bill-detail.html    # Page for viewing a single bill's details
├── main.py                 # FastAPI application and routes
├── models.py               # SQLAlchemy database models
├── schemas.py              # Pydantic request/response schemas
├── database.py             # Database configuration
├── utils.py                # Utility functions
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Backend Setup

### Installation

1.  Install Python 3.8 or higher.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Backend

1.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  Access API documentation:
    *   Swagger UI: `http://127.0.0.1:8000/docs`
    *   ReDoc: `http://127.0.0.1:8000/redoc`

## Frontend Setup

### Running the Frontend

No special setup is required. Simply open the `.html` files from the `frontend` directory in your web browser.

For example, on Windows, you can double-click the `index.html` file, or open it from your browser using the `File > Open` menu and navigating to `d:\PRABAKARAN\mallow_assement\billing-system-flask-main\frontend\index.html`.

### Frontend Pages

*   **`index.html` (Billing Terminal)**
    *   This is the main page for creating a new bill.
    *   You can add products to the cart, specify quantities, and see the total amount dynamically update.
    *   It allows entering the customer's email and the amount paid.
    *   The "Sum Denominations" button calculates the total paid amount based on the number of notes entered.
    *   On successful bill generation, a confirmation is shown, and you can navigate to the bill's detail page.

*   **`products.html` (Product Management)**
    *   Displays all available products in a card format.
    *   Allows you to **add** a new product using the "Add New Product" button, which opens a modal form.
    *   Provides **edit** and **delete** functionality for each product.

*   **`bills.html` (All Bills)**
    *   Lists all bills that have been generated.
    *   Each bill card shows a summary (bill number, customer, total amount, etc.).
    *   Clicking on a bill card takes you to the detailed view for that bill.

*   **`bill-detail.html` (Bill Details)**
    *   Shows a comprehensive view of a single bill, including all items, quantities, prices, taxes, and payment details.
    *   It also displays the exact denominations that were returned as change.

## API Endpoints

The frontend interacts with the following backend API endpoints.

### Products

*   `GET /products`: Fetches all products to display on the `products.html` page and to populate the product selection dropdowns in `index.html`.
*   `POST /products`: Creates a new product from the modal form in `products.html`.
*   `PUT /products/{product_id}`: Updates an existing product.
*   `DELETE /products/{product_id}`: Deletes a product.

### Bills

*   `POST /bills`: Creates a new bill from the `index.html` page.
*   `GET /bills`: Fetches all bills to display on the `bills.html` page.
*   `GET /bills/{bill_id}`: Fetches the details of a single bill for the `bill-detail.html` page.

## Database Schema

### Products Table

-   `id` (Integer, Primary Key)
-   `product_id` (String, Unique)
-   `name` (String)
-   `available_stocks` (Integer)
-   `price_per_unit` (Float)
-   `tax_percentage` (Float)
-   `created_at` (DateTime)

### Bills Table

-   `id` (Integer, Primary Key)
-   `bill_number` (String, Unique)
-   `customer_email` (String)
-   `subtotal` (Float)
-   `total_tax` (Float)
-   `total_amount` (Float)
-   `paid_amount` (Float)
-   `balance_amount` (Float)
-   `balance_denominations` (Text - JSON)
-   `created_at` (DateTime)

### BillItems Table

-   `id` (Integer, Primary Key)
-   `bill_id` (Foreign Key)
-   `product_id` (Foreign Key)
-   `quantity` (Integer)
-   `unit_price` (Float)
-   `tax_percentage` (Float)
-   `item_subtotal` (Float)
-   `item_tax` (Float)
-   `item_total` (Float)

### Denominations Table

-   `id` (Integer, Primary Key)
-   `value` (Float, Unique)
-   `created_at` (DateTime)
