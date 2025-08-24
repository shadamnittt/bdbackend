from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Алгоритм и секретный ключ
SECRET_KEY = "supersecretkey"  # ⚠️ поменяй на свой
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 👉 Хэширование пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 👉 Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 👉 Создание JWT токена
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
