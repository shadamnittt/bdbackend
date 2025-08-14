import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import clients, auth, appointment  # добавил appointments

app = FastAPI(
    title="BlackDent — Учёт Пациентов",
    version="1.0.0"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки можно "*", в проде лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(clients)
app.include_router(auth)
app.include_router(appointment)  # вот здесь добавляем роутер appointments

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
