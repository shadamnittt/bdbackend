from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
import random
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 🔐 Единые пинкоды для каждой роли
PIN_CODES = {
    "doctor": "5267",
    "admin": "1111",
    "registrar": "8903"
}

# --- Регистрация нового пользователя ---
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_pw = get_password_hash(user.password)
    safe_name = user.full_name or generate_username(user.role or "registrar")

    db_user = User(
        email=user.email,
        full_name=safe_name,
        clinic_name=user.clinic_name,
        hashed_password=hashed_pw,
        role=user.role or "registrar",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def generate_username(role: str):
    suffix = random.randint(100000, 999999)
    role_map = {
        "superadmin": "admin",
        "admin": "registrar",
        "doctor": "doctor",
        "registrar": "registrar"
    }
    prefix = role_map.get(role.lower(), "user")
    return f"{prefix}{suffix}"

# --- Логин ---
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    # Проверка пинкода
    pin_code = form_data.scopes[0] if form_data.scopes else None
    expected_pin = PIN_CODES.get(user.role)
    if not expected_pin or pin_code != expected_pin:
        raise HTTPException(status_code=400, detail="Неверный пинкод")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "email": user.email,
        "full_name": user.full_name
    }

# --- Получение текущего пользователя ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Недействительный токен")
        user_id = int(user_id)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Недействительный токен: {e}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

# --- Красивые роли для фронтенда ---
ROLE_LABELS = {
    "doctor": "Врач",
    "admin": "Админ",
    "registrar": "Регистратор"
}

class UpdateProfile(BaseModel):
    full_name: str | None = None
    clinic_name: str | None = None

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    current_user.role = ROLE_LABELS.get(current_user.role, current_user.role)
    return current_user

class UpdateName(BaseModel):
    full_name: str

@router.put("/me/update_name", response_model=UserOut)
def update_name(data: UpdateName, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.full_name = data.full_name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/update_profile", response_model=UserOut)
def update_profile(data: UpdateProfile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.clinic_name is not None:
        current_user.clinic_name = data.clinic_name
    db.commit()
    db.refresh(current_user)
    return current_user
