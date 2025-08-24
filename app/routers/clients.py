# from fastapi import APIRouter, Depends, Query, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app.schemas.client_schema import ClientCreate, ClientOut, ClientUpdate
# from app.crud.client_crud import create_client, get_clients, update_client, delete_client
# from app.database import get_db
# from app.models.user import User
# from app.dependencies import get_current_user, role_required

# router = APIRouter(
#     prefix="/clients",
#     tags=["Клиенты"]
# )

# # --- Добавить клиента (только админ и регистратор) ---
# @router.post("/", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
# def add_client(
#     client: ClientCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return create_client(db, client, current_user.id)


# # --- Получить список клиентов (все авторизованные пользователи) ---
# @router.get("/", response_model=List[ClientOut])
# def list_clients(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
#     full_name: Optional[str] = Query(None),
#     status: Optional[str] = Query(None),
#     date_created: Optional[str] = Query(None),
# ):
#     return get_clients(db)


# # --- Обновить клиента (только админ и регистратор) ---
# @router.put("/{client_id}", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
# def edit_client(
#     client_id: int,
#     client: ClientUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     updated_client = update_client(db, client_id, client)
#     if not updated_client:
#         raise HTTPException(status_code=404, detail="Клиент не найден")
#     return updated_client


# # --- Удалить клиента (только админ) ---
# @router.delete("/{client_id}", dependencies=[Depends(role_required(["admin"]))])
# def remove_client(
#     client_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     deleted_client = delete_client(db, client_id)
#     if not deleted_client:
#         raise HTTPException(status_code=404, detail="Клиент не найден")
#     return {"detail": "Пациент удален"}

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.client_schema import ClientCreate, ClientOut, ClientUpdate
from app.crud.client_crud import create_client, get_clients, update_client, delete_client
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, role_required

router = APIRouter(
    prefix="/clients",
    tags=["Клиенты"]
)

# --- Добавить клиента (только админ и регистратор) ---
@router.post("/", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
def add_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_client(db, client, current_user.id)

# --- Получить список клиентов (все авторизованные пользователи) ---
@router.get("/", response_model=List[ClientOut])
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    full_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_created: Optional[str] = Query(None),
):
    if current_user.role == "doctor":
        # фильтруем только клиентов, привязанных к врачу
        clients = get_clients(db, user_id=current_user.id)
    else:
        # для остальных ролей возвращаем всех клиентов
        clients = get_clients(db)
    return clients

# --- Обновить клиента (только админ и регистратор) ---
@router.put("/{client_id}", response_model=ClientOut, dependencies=[Depends(role_required(["admin", "registrar"]))])
def edit_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_client = update_client(db, client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return updated_client

# --- Удалить клиента (только админ) ---
@router.delete("/{client_id}", dependencies=[Depends(role_required(["admin"]))])
def remove_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_client = delete_client(db, client_id)
    if not deleted_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return {"detail": "Пациент удален"}
