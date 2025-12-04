from sqlalchemy.orm import Session
from .models import Item
from .schemas import ItemCreate, ItemUpdate


class ItemService:
    @staticmethod
    def get_item(db: Session, item_id: int) -> Item:
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 10) -> list[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    @staticmethod
    def get_items_count(db: Session) -> int:
        return db.query(Item).count()

    @staticmethod
    def create_item(db: Session, item: ItemCreate) -> Item:
        db_item = Item(
            name=item.name,
            description=item.description,
            is_active=item.is_active,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Item:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return None

        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete_item(db: Session, item_id: int) -> bool:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True

    @staticmethod
    def search_items(db: Session, query: str, skip: int = 0, limit: int = 10) -> list[Item]:
        return (
            db.query(Item)
            .filter(Item.name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
