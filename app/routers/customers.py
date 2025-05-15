from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.auth import get_db, get_current_active_user, get_admin_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=schemas.Customer)
def create_customer(
    customer: schemas.CustomerCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_customer = crud.get_customer(db, customer.id)
    if db_customer:
        raise HTTPException(status_code=400, detail="Customer already exists")
    return crud.create_customer(db, customer)

@router.get("/", response_model=list[schemas.Customer])
def read_customers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_customers(db)

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(
    customer_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int, 
    customer: schemas.CustomerCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)  # Only admins can update customers
):
    updated_customer = crud.update_customer(db, customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)  # Only admins can delete customers
):
    result = crud.delete_customer(db, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": f"Customer {customer_id} deleted"}