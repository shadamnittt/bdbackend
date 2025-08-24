# from sqlalchemy.orm import Session
# from app.models.client import Client
# from app.schemas.client_schema import ClientCreate, ClientUpdate
# from datetime import datetime

# def create_client(db: Session, client: ClientCreate, user_id: int):
#     db_client = Client(
#         full_name=client.full_name,
#         phone_number=client.phone_number,
#         status=client.status,
#         comment=client.comment,
#         date_created=datetime.utcnow(),
#         user_id=user_id
#     )
#     db.add(db_client)
#     db.commit()
#     db.refresh(db_client)
#     return db_client

# def get_clients(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Client).offset(skip).limit(limit).all()

# def update_client(db: Session, client_id: int, client: ClientUpdate):
#     db_client = db.query(Client).filter(Client.id == client_id).first()
#     if not db_client:
#         return None
#     for key, value in client.dict(exclude_unset=True).items():
#         setattr(db_client, key, value)
#     db.commit()
#     db.refresh(db_client)
#     return db_client

# def delete_client(db: Session, client_id: int):
#     db_client = db.query(Client).filter(Client.id == client_id).first()
#     if not db_client:
#         return None
#     db.delete(db_client)
#     db.commit()
#     return db_client

from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientUpdate
from datetime import datetime

def create_client(db: Session, client: ClientCreate, user_id: int):
    db_client = Client(
        full_name=client.full_name,
        phone_number=client.phone_number,
        status=client.status,
        comment=client.comment,
        date_created=datetime.utcnow(),
        user_id=user_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# 🔹 Исправленный get_clients с фильтром по врачу
def get_clients(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    query = db.query(Client)
    if user_id is not None:
        query = query.filter(Client.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def update_client(db: Session, client_id: int, client: ClientUpdate):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None
    for key, value in client.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None
    db.delete(db_client)
    db.commit()
    return db_client
