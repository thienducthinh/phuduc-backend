from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from .schemas import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerListResponse
from .service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=CustomerListResponse)
async def list_customers(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """List all customers with pagination"""
    customers = await CustomerService.get_customers(db, skip=skip, limit=limit)
    total = await CustomerService.get_customers_count(db)
    page = skip // limit + 1
    return {
        "customers": customers,
        "total": total,
        "page": page,
        "page_size": limit,
    }


@router.get("/search/", response_model=list[CustomerResponse])
async def search_customers(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """Search customers by name, email, or phone"""
    return await CustomerService.search_customers(db, q, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single customer by ID"""
    customer = await CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """Create a new customer"""
    return await CustomerService.create_customer(db, customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a customer"""
    customer = await CustomerService.update_customer(db, customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a customer"""
    success = await CustomerService.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
