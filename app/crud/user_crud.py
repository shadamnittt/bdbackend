from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UpdateUserRole
from app.core.security import get_password_hash


# 👉 Создание пользователя
def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        username=user.email,  # можно менять на отдельный username, если есть
        full_name=user.full_name,
        clinic_name=user.clinic_name,
        role=user.role,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 👉 Получение пользователя по email
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# 👉 Получение всех пользователей
def get_all_users(db: Session):
    return db.query(User).all()


# 👉 Обновление пользователя (например, смена пароля или имени)
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    if user.full_name is not None:
        db_user.full_name = user.full_name
    if user.password is not None:
        db_user.hashed_password = get_password_hash(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user


# 👉 Удаление пользователя
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# 👉 Обновление роли пользователя
def update_user_role(db: Session, user_id: int, role_data: UpdateUserRole):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db_user.role = role_data.role
    db.commit()
    db.refresh(db_user)
    return db_user
