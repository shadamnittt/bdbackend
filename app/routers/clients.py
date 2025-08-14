from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.client_schema import ClientCreate, ClientOut, ClientUpdate
from app.crud.client_crud import (
    create_client,
    get_clients,
    update_client,
    delete_client
)
from app.database import get_db

router = APIRouter(
    prefix="/clients",
    tags=["Клиенты"]
)

@router.post("/", response_model=ClientOut)
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    user_id = 1  # Для теста: жестко заданный user_id
    return create_client(db, client, user_id)

@router.get("/", response_model=List[ClientOut])
def list_clients(
    db: Session = Depends(get_db),
    full_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_created: Optional[str] = Query(None),
):
    # В get_clients пока не реализована фильтрация, можно добавить потом
    return get_clients(db)

@router.put("/{client_id}", response_model=ClientOut)
def edit_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    updated_client = update_client(db, client_id, client)
    if not updated_client:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return updated_client

@router.delete("/{client_id}")
def remove_client(client_id: int, db: Session = Depends(get_db)):
    deleted_client = delete_client(db, client_id)
    if not deleted_client:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return {"detail": "Пациент удален"}
