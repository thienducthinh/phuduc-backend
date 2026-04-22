from sqlalchemy.ext.asyncio import AsyncSession

from .models import Carrier, Delivery
from .repository import CarrierRepository, DeliveryRepository
from .schemas import CarrierCreate, CarrierUpdate, DeliveryCreate, DeliveryUpdate


class CarrierService:
    def __init__(self, db: AsyncSession):
        self.repo = CarrierRepository(db)

    async def get(self, carrier_id: int) -> Carrier | None:
        return await self.repo.get_by_id(carrier_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Carrier]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def create(self, data: CarrierCreate) -> Carrier:
        return await self.repo.create(data.model_dump())

    async def update(self, carrier: Carrier, data: CarrierUpdate) -> Carrier:
        return await self.repo.update(carrier, data.model_dump(exclude_unset=True))

    async def delete(self, carrier: Carrier) -> None:
        await self.repo.delete(carrier)


class DeliveryService:
    def __init__(self, db: AsyncSession):
        self.repo = DeliveryRepository(db)

    async def get(self, delivery_id: int) -> Delivery | None:
        return await self.repo.get_by_id(delivery_id)

    async def get_by_sales_order(self, sales_order_id: int) -> list[Delivery]:
        return await self.repo.get_by_sales_order(sales_order_id)

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list[Delivery]:
        return await self.repo.get_by_status(status, skip=skip, limit=limit)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Delivery]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def create(self, data: DeliveryCreate) -> Delivery:
        return await self.repo.create(data.model_dump())

    async def update(self, delivery: Delivery, data: DeliveryUpdate) -> Delivery:
        return await self.repo.update(delivery, data.model_dump(exclude_unset=True))

    async def delete(self, delivery: Delivery) -> None:
        await self.repo.delete(delivery)
