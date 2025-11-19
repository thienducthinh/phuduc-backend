from src.core.database import Base, engine


async def init_db():
    """Initialize database tables - call this from FastAPI startup event"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Get all table names that were created
    table_names = [table.name for table in Base.metadata.sorted_tables]
    print(f"Tables created (or already exist): {', '.join(table_names)}")
