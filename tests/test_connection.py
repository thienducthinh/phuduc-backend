"""
Test database connection to Azure SQL Server
"""
import asyncio
from src.core.database import engine

async def test_connection():
    try:
        print("Testing database connection...")
        async with engine.connect() as conn:
            print("✓ Successfully connected to database!")
            result = await conn.execute("SELECT @@VERSION as version")
            version = await result.fetchone()
            print(f"Database version: {version[0][:100]}...")
        await engine.dispose()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        await engine.dispose()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
