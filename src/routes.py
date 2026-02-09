# Routes have been reorganized into their respective domain modules:
# - PO routes -> src.modules.purchasing.router
# - SO routes -> src.modules.sales.router
# - Item routes -> src.modules.inventory.router

from fastapi import APIRouter
from src.modules.purchasing.router import router as purchasing_router
from src.modules.customer.router import router as customer_router

# Main router that includes all module routers
router = APIRouter()
router.include_router(purchasing_router)
router.include_router(customer_router)

# Add more module routers as they are created:
# from src.modules.sales.router import router as sales_router
# from src.modules.inventory.router import router as inventory_router
# router.include_router(sales_router)
# router.include_router(inventory_router)
