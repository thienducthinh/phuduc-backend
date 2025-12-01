"""
Script to create database tables in local MySQL Workbench
Run this script to initialize your local MySQL database with all tables from the models
"""
import asyncio
import sys
from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import create_async_engine

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# MySQL connection string for local database
# Update these values according to your local MySQL setup
MYSQL_USER = "root"
MYSQL_PASSWORD = "Thinhnguyen2491@"  # Change this to your MySQL password
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "OcoMainDB"

# URL-encode password to handle special characters like @
encoded_password = quote_plus(MYSQL_PASSWORD)

# Create async MySQL connection URL for local MySQL
LOCAL_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create engine
engine = create_async_engine(
    LOCAL_DATABASE_URL,
    echo=True,  # Set to False to disable SQL logging
    pool_pre_ping=True,
)

# Import Base and all models from the actual project
from src.core.database import Base

# Import all models to register them with Base.metadata
# This ensures all tables are created
from src.modules.inventory import models as inventory_models
from src.modules.purchasing import models as purchasing_models
from src.modules.sales import models as sales_models

# All model classes are now imported and registered with Base.metadata
# No need to redefine them here


async def drop_all_tables():
    """Drop all tables in the database"""
    from sqlalchemy import text

    print("⚠️  Dropping all existing tables...")

    async with engine.begin() as conn:
        # Get all tables
        result = await conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()

        if tables:
            # Disable foreign key checks to allow dropping tables with FK constraints
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            for (table_name,) in tables:
                print(f"  Dropping table: {table_name}")
                await conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

            # Re-enable foreign key checks
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            print(f"✓ Dropped {len(tables)} tables")
        else:
            print("✓ No tables to drop")


async def create_database():
    """Create the database if it doesn't exist"""
    from sqlalchemy import text

    # Connect without database to create it
    db_url_without_db = f"mysql+aiomysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}"
    temp_engine = create_async_engine(db_url_without_db, echo=True)

    async with temp_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} DEFAULT CHARACTER SET = 'utf8mb4'"))
        await conn.commit()
        print(f"✓ Database '{MYSQL_DATABASE}' created or already exists")

    await temp_engine.dispose()


async def create_tables(drop_existing=False):
    """Create all tables in the database"""
    from sqlalchemy import text

    # First create database if needed
    await create_database()

    # Drop existing tables if requested
    if drop_existing:
        await drop_all_tables()

    # Now create tables
    print("\nCreating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Get all table names
    table_names = [table.name for table in Base.metadata.sorted_tables]
    print(f"\n✓ Successfully created {len(table_names)} tables:")
    for idx, table_name in enumerate(table_names, 1):
        print(f"  {idx}. {table_name}")

    await engine.dispose()


async def main():
    """Main function to run the script"""
    print("="*60)
    print("Creating Local MySQL Database Tables")
    print("="*60)
    print(f"Database: {MYSQL_DATABASE}")
    print(f"Host: {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"User: {MYSQL_USER}")
    print("="*60)
    print()

    # Ask user if they want to drop existing tables
    drop = input("Do you want to drop existing tables? (yes/no) [no]: ").strip().lower()
    drop_existing = drop in ['yes', 'y']

    try:
        await create_tables(drop_existing=drop_existing)
        print("\n✅ Database setup completed successfully!")
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Install required packages:
    # pip install aiomysql pymysql

    print("\nIMPORTANT: Before running this script:")
    print("1. Update MYSQL_PASSWORD in the script with your MySQL password")
    print("2. Make sure MySQL server is running")
    print("3. Install required packages: pip install aiomysql pymysql")
    print()

    asyncio.run(main())
