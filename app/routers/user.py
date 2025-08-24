from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut, UpdateUserRole
from app.crud.user_crud import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    update_user_role,
)

router = APIRouter(prefix="/users", tags=["Users"])


# 🔹 Создание пользователя
@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return create_user(db, user)


# 🔹 Получение всех пользователей
@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# 🔹 Обновление пользователя (имя, пароль)
@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


# 🔹 Удаление пользователя
@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удалён"}


# 🔹 Обновление роли
@router.put("/{user_id}/role", response_model=UserOut)
def change_user_role(user_id: int, role_data: UpdateUserRole, db: Session = Depends(get_db)):
    db_user = update_user_role(db, user_id, role_data)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
