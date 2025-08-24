from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# --- Конфигурация ---
SECRET_KEY = "your-secret-key"   # ⚡️ замени на более сложный и храни в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Контекст хеширования паролей ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Работа с паролями ---
def hash_password(password: str) -> str:
    """Хеширует пароль"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT: создание токена ---
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создаёт JWT-токен
    data -> словарь с данными (обычно {"sub": user.id})
    expires_delta -> время жизни токена
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- JWT: декодирование токена ---
def decode_token(token: str) -> int:
    """
    Декодирует JWT и возвращает user_id из поля "sub"
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Token missing user_id")
        return int(user_id)
    except JWTError:
        raise ValueError("Invalid or expired token")
