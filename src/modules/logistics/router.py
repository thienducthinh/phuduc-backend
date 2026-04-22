from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.core.database import get_db
from .dependencies import get_carrier_or_404, get_delivery_or_404
from .models import Carrier, Delivery
from .schemas import (
    CarrierCreate, CarrierUpdate, CarrierResponse,
    DeliveryCreate, DeliveryUpdate, DeliveryResponse, DeliveryStatus,
)
from .service import CarrierService, DeliveryService

router = APIRouter(prefix="/logistics", tags=["Logistics"])


# --- Carriers ---

@router.get("/carriers", response_model=list[CarrierResponse])
async def list_carriers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    return await CarrierService(db).get_all(skip=skip, limit=limit)


@router.get("/carriers/{carrier_id}", response_model=CarrierResponse)
async def get_carrier(carrier: Carrier = Depends(get_carrier_or_404)):
    return carrier


@router.post("/carriers", response_model=CarrierResponse, status_code=201)
async def create_carrier(data: CarrierCreate, db: AsyncSession = Depends(get_db)):
    return await CarrierService(db).create(data)


@router.put("/carriers/{carrier_id}", response_model=CarrierResponse)
async def update_carrier(
    data: CarrierUpdate,
    carrier: Carrier = Depends(get_carrier_or_404),
    db: AsyncSession = Depends(get_db),
):
    return await CarrierService(db).update(carrier, data)


@router.delete("/carriers/{carrier_id}", status_code=204)
async def delete_carrier(
    carrier: Carrier = Depends(get_carrier_or_404),
    db: AsyncSession = Depends(get_db),
):
    await CarrierService(db).delete(carrier)


# --- Deliveries ---

@router.get("/deliveries", response_model=list[DeliveryResponse])
async def list_deliveries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[DeliveryStatus] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = DeliveryService(db)
    if status:
        return await svc.get_by_status(status, skip=skip, limit=limit)
    return await svc.get_all(skip=skip, limit=limit)


@router.get("/deliveries/sales-order/{sales_order_id}", response_model=list[DeliveryResponse])
async def list_by_sales_order(sales_order_id: int, db: AsyncSession = Depends(get_db)):
    return await DeliveryService(db).get_by_sales_order(sales_order_id)


@router.get("/deliveries/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(delivery: Delivery = Depends(get_delivery_or_404)):
    return delivery


@router.post("/deliveries", response_model=DeliveryResponse, status_code=201)
async def create_delivery(data: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    return await DeliveryService(db).create(data)


@router.put("/deliveries/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(
    data: DeliveryUpdate,
    delivery: Delivery = Depends(get_delivery_or_404),
    db: AsyncSession = Depends(get_db),
):
    return await DeliveryService(db).update(delivery, data)


@router.delete("/deliveries/{delivery_id}", status_code=204)
async def delete_delivery(
    delivery: Delivery = Depends(get_delivery_or_404),
    db: AsyncSession = Depends(get_db),
):
    await DeliveryService(db).delete(delivery)
