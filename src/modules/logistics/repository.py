from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Carrier, Delivery


class CarrierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, carrier_id: int) -> Carrier | None:
        result = await self.db.execute(select(Carrier).where(Carrier.carrier_id == carrier_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Carrier]:
        result = await self.db.execute(select(Carrier).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> Carrier:
        carrier = Carrier(**data)
        self.db.add(carrier)
        await self.db.commit()
        await self.db.refresh(carrier)
        return carrier

    async def update(self, carrier: Carrier, data: dict) -> Carrier:
        for field, value in data.items():
            setattr(carrier, field, value)
        await self.db.commit()
        await self.db.refresh(carrier)
        return carrier

    async def delete(self, carrier: Carrier) -> None:
        await self.db.delete(carrier)
        await self.db.commit()


class DeliveryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, delivery_id: int) -> Delivery | None:
        result = await self.db.execute(select(Delivery).where(Delivery.delivery_id == delivery_id))
        return result.scalar_one_or_none()

    async def get_by_sales_order(self, sales_order_id: int) -> list[Delivery]:
        result = await self.db.execute(
            select(Delivery).where(Delivery.sales_order_id == sales_order_id)
        )
        return list(result.scalars().all())

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list[Delivery]:
        result = await self.db.execute(
            select(Delivery).where(Delivery.status == status).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Delivery]:
        result = await self.db.execute(select(Delivery).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> Delivery:
        delivery = Delivery(**data)
        self.db.add(delivery)
        await self.db.commit()
        await self.db.refresh(delivery)
        return delivery

    async def update(self, delivery: Delivery, data: dict) -> Delivery:
        for field, value in data.items():
            setattr(delivery, field, value)
        await self.db.commit()
        await self.db.refresh(delivery)
        return delivery

    async def delete(self, delivery: Delivery) -> None:
        await self.db.delete(delivery)
        await self.db.commit()
