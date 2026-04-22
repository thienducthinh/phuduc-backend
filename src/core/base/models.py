from src.core.database import Base, engine

# Import all models to register them with Base.metadata
# Order matters: tables with no FK dependencies first, then dependent tables
from src.modules.customer import models as customer_models
from src.modules.item import models as item_models
from src.modules.inventory import models as inventory_models
from src.modules.purchasing import models as purchasing_models
from src.modules.sales import models as sales_models


async def init_db():
    """Initialize database tables - call this from FastAPI startup event"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Get all table names that were created
    table_names = [table.name for table in Base.metadata.sorted_tables]
    print(f"Tables created (or already exist): {', '.join(table_names)}")
