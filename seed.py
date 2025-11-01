"""
Seed script to populate initial data
"""
from database import SessionLocal, engine, Base
import models

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add default denominations
default_denoms = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

for value in default_denoms:
    existing = db.query(models.Denomination).filter(
        models.Denomination.value == value
    ).first()
    
    if not existing:
        denom = models.Denomination(value=value)
        db.add(denom)
        print(f"Added denomination: {value}")

# Add sample products
sample_products = [
    {
        "product_id": "PROD001",
        "name": "Laptop",
        "available_stocks": 10,
        "price_per_unit": 50000.0,
        "tax_percentage": 18.0
    },
    {
        "product_id": "PROD002",
        "name": "Mouse",
        "available_stocks": 50,
        "price_per_unit": 500.0,
        "tax_percentage": 12.0
    },
    {
        "product_id": "PROD003",
        "name": "Keyboard",
        "available_stocks": 30,
        "price_per_unit": 2000.0,
        "tax_percentage": 12.0
    },
    {
        "product_id": "PROD004",
        "name": "Monitor",
        "available_stocks": 15,
        "price_per_unit": 15000.0,
        "tax_percentage": 18.0
    },
    {
        "product_id": "PROD005",
        "name": "USB Cable",
        "available_stocks": 100,
        "price_per_unit": 200.0,
        "tax_percentage": 5.0
    }
]

for prod_data in sample_products:
    existing = db.query(models.Product).filter(
        models.Product.product_id == prod_data["product_id"]
    ).first()
    
    if not existing:
        product = models.Product(**prod_data)
        db.add(product)
        print(f"Added product: {prod_data['name']}")

db.commit()
db.close()

print("\nDatabase seeded successfully!")

