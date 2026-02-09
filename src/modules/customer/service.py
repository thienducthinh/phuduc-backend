from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Customer
from .schemas import CustomerCreate, CustomerUpdate


class CustomerService:
    @staticmethod
    async def get_customer(db: AsyncSession, customer_id: int) -> Customer:
        """Get a single customer by ID"""
        result = await db.execute(
            select(Customer).filter(Customer.customer_id == customer_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Customer]:
        """Get all customers with pagination"""
        result = await db.execute(
            select(Customer).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_customers_count(db: AsyncSession) -> int:
        """Get total count of customers"""
        result = await db.execute(select(func.count(Customer.customer_id)))
        return result.scalar()

    @staticmethod
    async def create_customer(db: AsyncSession, customer: CustomerCreate) -> Customer:
        """Create a new customer"""
        db_customer = Customer(
            customer_name=customer.customer_name,
            customer_address=customer.customer_address,
            customer_phone=customer.customer_phone,
            customer_email=customer.customer_email,
            price_type=customer.price_type,
        )
        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        return db_customer

    @staticmethod
    async def update_customer(db: AsyncSession, customer_id: int, customer_update: CustomerUpdate) -> Customer:
        """Update an existing customer"""
        result = await db.execute(
            select(Customer).filter(Customer.customer_id == customer_id)
        )
        db_customer = result.scalar_one_or_none()

        if not db_customer:
            return None

        update_data = customer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)

        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        return db_customer

    @staticmethod
    async def delete_customer(db: AsyncSession, customer_id: int) -> bool:
        """Delete a customer"""
        result = await db.execute(
            select(Customer).filter(Customer.customer_id == customer_id)
        )
        db_customer = result.scalar_one_or_none()

        if not db_customer:
            return False

        await db.delete(db_customer)
        await db.commit()
        return True

    @staticmethod
    async def search_customers(db: AsyncSession, query: str, skip: int = 0, limit: int = 10) -> list[Customer]:
        """Search customers by name, email, or phone"""
        result = await db.execute(
            select(Customer)
            .filter(
                (Customer.customer_name.ilike(f"%{query}%")) |
                (Customer.customer_email.ilike(f"%{query}%")) |
                (Customer.customer_phone.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
