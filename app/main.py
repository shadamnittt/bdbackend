import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base   # ⚡ добавили импорт engine и Base
from app.models import User, Client, VisitLog, Appointment

# --- создаём таблицы при старте ---
Base.metadata.create_all(bind=engine)   # ⚡ вот эта строка создаёт таблицы

# Импортируем только router из каждого модуля
from app.routers.user import router as user_router
from app.routers.admin import router as admin_router
from app.routers.clients import router as clients_router
from app.routers.auth import router as auth_router
from app.routers.appointment import router as appointment_router

app = FastAPI(
    title="BlackDent — Учёт Пациентов",
    version="1.0.0"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(clients_router)
app.include_router(auth_router)          # теперь /token и /register доступны напрямую
app.include_router(appointment_router)
app.include_router(user_router)
app.include_router(admin_router)         # админский роутер

@app.get("/")
async def root():
    return {"message": "API BlackDent работает"}

@app.get("/api/patients")
async def get_patients():
    example_patients = [
        {"id": 1, "name": "Иван Иванов", "age": 30},
        {"id": 2, "name": "Мария Петрова", "age": 25}
    ]
    return {"patients": example_patients}
