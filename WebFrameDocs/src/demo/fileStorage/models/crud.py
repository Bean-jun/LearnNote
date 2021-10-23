from sqlalchemy.orm import Session


from models import model, schemas


def get_item(db: Session, facker_name: str):
    return db.query(model.FileItem).filter_by(facker_name=facker_name).first()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = model.FileItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item: model.FileItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
