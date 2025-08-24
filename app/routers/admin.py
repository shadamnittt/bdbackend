from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_current_user, role_required
from app.schemas.client_schema import ClientOut, ClientCreate, ClientUpdate
from app.crud.client_crud import create_client, get_clients, update_client, delete_client
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Админ"]
)

# --- КЛИЕНТЫ ---

# Только admin и registrar могут добавлять клиентов
@router.post("/clients/", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
def add_client(client: ClientCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_client(db, client, current_user.id)

# Только admin и registrar могут редактировать клиентов
@router.put("/clients/{client_id}", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
def edit_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    updated_client = update_client(db, client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return updated_client

# Только admin и registrar могут удалять клиентов
@router.delete("/clients/{client_id}", dependencies=[Depends(role_required(["admin", "registrar"]))])
def remove_client(client_id: int, db: Session = Depends(get_db)):
    deleted_client = delete_client(db, client_id)
    if not deleted_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return {"detail": "Пациент удален"}

# Все роли могут просматривать клиентов
@router.get("/clients/", response_model=List[ClientOut])
def list_clients(
    db: Session = Depends(get_db),
    full_name: str = None,
    status: str = None,
    date_created: str = None,
):
    return get_clients(db)
