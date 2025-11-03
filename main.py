from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from datetime import datetime
import models
import schemas
from database import engine, get_db, Base
from utils import calculate_balance_denominations, denominations_to_json, generate_bill_number

import uuid
from sqlalchemy.exc import IntegrityError

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Billing System API", version="1.0.0")

# Add CORS middleware
# This is necessary to allow the frontend (running on a different port)
# to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allows all. For production, restrict this to your frontend's domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== PRODUCTS ====================

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if product already exists
    existing = db.query(models.Product).filter(
        models.Product.product_id == product.product_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID already exists"
        )
    
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=list[schemas.ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(models.Product).all()
    return products

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get product by product_id"""
    product = db.query(models.Product).filter(
        models.Product.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: str, product_update: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Update a product"""
    product = db.query(models.Product).filter(
        models.Product.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    for key, value in product_update.dict().items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(models.Product).filter(
        models.Product.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# ==================== DENOMINATIONS ====================

@app.post("/denominations", response_model=schemas.DenominationResponse)
def create_denomination(denom: schemas.DenominationCreate, db: Session = Depends(get_db)):
    """Create a new denomination"""
    existing = db.query(models.Denomination).filter(
        models.Denomination.value == denom.value
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Denomination already exists"
        )
    
    db_denom = models.Denomination(**denom.dict())
    db.add(db_denom)
    db.commit()
    db.refresh(db_denom)
    return db_denom

@app.get("/denominations", response_model=list[schemas.DenominationResponse])
def get_all_denominations(db: Session = Depends(get_db)):
    """Get all denominations"""
    denominations = db.query(models.Denomination).all()
    return denominations

# ==================== BILLS ====================

@app.post("/bills", response_model=schemas.BillResponse)
def create_bill(bill_data: schemas.BillCreate, db: Session = Depends(get_db)):
    """Create a new bill"""
    
    # Validate and fetch products
    bill_items_data = []
    subtotal = 0
    total_tax = 0
    
    for item in bill_data.items:
        product = db.query(models.Product).filter(
            models.Product.product_id == item.product_id
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )
        
        if product.available_stocks < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {item.product_id}"
            )
        
        item_subtotal = product.price_per_unit * item.quantity
        item_tax = item_subtotal * (product.tax_percentage / 100)
        item_total = item_subtotal + item_tax
        
        bill_items_data.append({
            "product": product,
            "quantity": item.quantity,
            "unit_price": product.price_per_unit,
            "tax_percentage": product.tax_percentage,
            "item_subtotal": item_subtotal,
            "item_tax": item_tax,
            "item_total": item_total
        })
        
        subtotal += item_subtotal
        total_tax += item_tax
    
    total_amount = subtotal + total_tax
    
    # Validate paid amount
    if bill_data.paid_amount < total_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paid amount is less than total amount"
        )
    
    balance_amount = bill_data.paid_amount - total_amount
    
    # Calculate balance denominations
    denominations = db.query(models.Denomination).all()
    denom_values = [d.value for d in denominations]
    balance_denoms = calculate_balance_denominations(balance_amount, denom_values)
    balance_denoms_json = denominations_to_json(balance_denoms)
    
    # Create bill
    db_bill = models.Bill(
        bill_number=f"TEMP-{uuid.uuid4()}",  # Temporary unique bill number
        customer_email=bill_data.customer_email,
        subtotal=subtotal,
        total_tax=total_tax,
        total_amount=total_amount,
        paid_amount=bill_data.paid_amount,
        balance_amount=balance_amount,
        balance_denominations=balance_denoms_json
    )
    
    try:
        db.add(db_bill)
        db.flush() # Flushes to get the ID for the bill number

        # Update bill number to its final value
        db_bill.bill_number = generate_bill_number(db_bill.id)
        
        # Create bill items and update stock
        for item_data in bill_items_data:
            db_bill_item = models.BillItem(
                bill_id=db_bill.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                tax_percentage=item_data["tax_percentage"],
                item_subtotal=item_data["item_subtotal"],
                item_tax=item_data["item_tax"],
                item_total=item_data["item_total"]
            )
            db.add(db_bill_item)
            
            # Update product stock
            item_data["product"].available_stocks -= item_data["quantity"]
        
        db.commit()
        db.refresh(db_bill)
        return db_bill

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database integrity error: {e.orig}"
        )

@app.get("/bills/{bill_id}", response_model=schemas.BillDetailResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get bill by ID"""
    bill = db.query(models.Bill).options(joinedload(models.Bill.bill_items).joinedload(models.BillItem.product)).filter(models.Bill.id == bill_id).first()
    
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    return bill

@app.get("/bills", response_model=list[schemas.BillResponse])
def get_all_bills(db: Session = Depends(get_db)):
    """Get all bills"""
    bills = db.query(models.Bill).order_by(desc(models.Bill.created_at)).all()
    return bills

@app.get("/customers/{customer_email}/purchases", response_model=schemas.CustomerPurchaseHistory)
def get_customer_purchases(customer_email: str, db: Session = Depends(get_db)):
    """Get all purchases by a customer"""
    bills = db.query(models.Bill).filter(
        models.Bill.customer_email == customer_email
    ).order_by(desc(models.Bill.created_at)).all()
    
    if not bills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No purchases found for this customer"
        )
    
    return {
        "customer_email": customer_email,
        "total_purchases": len(bills),
        "bills": bills
    }

# ==================== HEALTH CHECK ====================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Billing System API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
