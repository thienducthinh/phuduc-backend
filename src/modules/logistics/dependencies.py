from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from .models import Carrier, Delivery
from .repository import CarrierRepository, DeliveryRepository


async def get_carrier_or_404(carrier_id: int, db: AsyncSession = Depends(get_db)) -> Carrier:
    carrier = await CarrierRepository(db).get_by_id(carrier_id)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier


async def get_delivery_or_404(delivery_id: int, db: AsyncSession = Depends(get_db)) -> Delivery:
    delivery = await DeliveryRepository(db).get_by_id(delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery
