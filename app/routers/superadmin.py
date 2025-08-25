# app/routers/superadmin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.client_schema import ClientOut
from app.crud.user_crud import create_user, delete_user, get_all_users
from app.crud.client_crud import get_clients
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/superadmin",
    tags=["SuperAdmin"]
)

# Проверка роли супер-админа
def superadmin_required(current_user: User = Depends(get_current_user)):
    if current_user.role.lower() != "superadmin":
        raise HTTPException(status_code=403, detail="Нет прав супер-админа")
    return current_user


# 🔹 Создание админа
@router.post("/users/admin", response_model=UserOut, dependencies=[Depends(superadmin_required)])
def create_admin(user: UserCreate, db: Session = Depends(get_db)):
    user.role = "admin"  # фиксируем роль
    return create_user(db, user)


# 🔹 Удаление пользователя
@router.delete("/users/{user_id}", dependencies=[Depends(superadmin_required)])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удалён"}


# 🔹 Получить всех клиентов
@router.get("/clients/all", response_model=List[ClientOut], dependencies=[Depends(superadmin_required)])
def get_all_clients(db: Session = Depends(get_db)):
    return get_clients(db)  # возвращаем всех, без фильтрации по врачу/клинике


# 🔹 Мониторинг активности (пример: список всех пользователей и клиентов)
@router.get("/activity", dependencies=[Depends(superadmin_required)])
def get_activity(db: Session = Depends(get_db)):
    users = get_all_users(db)
    clients = get_clients(db)
    return {"users": users, "clients": clients}
