from fastapi import Depends
from src.modules.auth.dependencies import get_auth_user

# Example: Inventory might not require admin, just authenticated user
get_inventory_user = get_auth_user