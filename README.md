# Billing System API

A simple FastAPI-based billing system with SQLite database for managing products, bills, and denominations.

## Features

- **Product Management**: Create, read, update, and delete products
- **Bill Generation**: Create bills with multiple items, automatic tax calculation
- **Denomination Management**: Manage shop denominations and calculate balance denominations
- **Customer Purchase History**: View all purchases by a customer
- **Stock Management**: Automatic stock deduction when bills are created

## Project Structure

```
billing_system/
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Database configuration
├── utils.py             # Utility functions
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

2. Access API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Products
- `POST /products` - Create a new product
- `GET /products` - Get all products
- `GET /products/{product_id}` - Get product by ID
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product

### Denominations
- `POST /denominations` - Create a new denomination
- `GET /denominations` - Get all denominations
- `POST /denominations/init` - Initialize default denominations (2000, 500, 200, 100, 50, 20, 10, 5, 2, 1)

### Bills
- `POST /bills` - Create a new bill
- `GET /bills` - Get all bills
- `GET /bills/{bill_id}` - Get bill by ID
- `GET /customers/{customer_email}/purchases` - Get all purchases by customer

### Health
- `GET /health` - Health check

## Database Schema

### Products Table
- `id` (Integer, Primary Key)
- `product_id` (String, Unique)
- `name` (String)
- `available_stocks` (Integer)
- `price_per_unit` (Float)
- `tax_percentage` (Float)
- `created_at` (DateTime)

### Bills Table
- `id` (Integer, Primary Key)
- `bill_number` (String, Unique)
- `customer_email` (String)
- `subtotal` (Float)
- `total_tax` (Float)
- `total_amount` (Float)
- `paid_amount` (Float)
- `balance_amount` (Float)
- `balance_denominations` (Text - JSON)
- `created_at` (DateTime)

### BillItems Table
- `id` (Integer, Primary Key)
- `bill_id` (Foreign Key)
- `product_id` (Foreign Key)
- `quantity` (Integer)
- `unit_price` (Float)
- `tax_percentage` (Float)
- `item_subtotal` (Float)
- `item_tax` (Float)
- `item_total` (Float)

### Denominations Table
- `id` (Integer, Primary Key)
- `value` (Float, Unique)
- `created_at` (DateTime)

## Usage Examples

### 1. Initialize Default Denominations
```bash
curl -X POST http://localhost:8000/denominations/init
```

### 2. Create a Product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD001",
    "name": "Laptop",
    "available_stocks": 10,
    "price_per_unit": 50000.0,
    "tax_percentage": 18.0
  }'
```

### 3. Create a Bill
```bash
curl -X POST http://localhost:8000/bills \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "customer@example.com",
    "items": [
      {
        "product_id": "PROD001",
        "quantity": 2
      }
    ],
    "paid_amount": 120000.0
  }'
```

### 4. Get Customer Purchase History
```bash
curl http://localhost:8000/customers/customer@example.com/purchases
```

## Assumptions

1. **Email Sending**: Email functionality is not implemented in this version. To add it, integrate with an email service like SendGrid or use SMTP.

2. **Authentication**: No authentication is implemented. For production, add JWT or OAuth2.

3. **Denominations**: Default denominations are Indian currency values (2000, 500, 200, 100, 50, 20, 10, 5, 2, 1). Modify as needed.

4. **Balance Calculation**: Uses greedy algorithm to calculate minimum denominations needed for balance.

5. **Database**: SQLite is used for simplicity. For production, use PostgreSQL or MySQL.

## Notes

- The database file `billing.db` is created automatically in the project directory
- All timestamps are in UTC
- Bill numbers are auto-generated in format: BILL-000001
- Stock is automatically deducted when a bill is created
- Balance denominations are calculated using a greedy algorithm

## Future Enhancements

1. Add email notification for bill generation
2. Add authentication and authorization
3. Add payment gateway integration
4. Add bill PDF generation
5. Add advanced reporting and analytics
6. Add inventory management features
7. Add discount and coupon functionality
