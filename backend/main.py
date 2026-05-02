"""
Backend FastAPI приложение — каркас для Epics:

- Epic 1: Авторизация (регистрация / логин)
- Epic 2: Получение списка курсов

Текущее исполнение: in-memory хранилище пользователей и курсов для простого демо.
В коде отмечены места, где подключить реальную БД (PostgreSQL) и миграции.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import os
from typing import List

# Простой секрет для demo JWT. В реальном проекте вынести в секреты/ENV
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret_demo_key")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Educational Platform - Backend (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------- Простые Pydantic-схемы ----------------
class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Course(BaseModel):
    id: int
    title: str
    description: str


# --------------- In-memory хранилище (демо) --------------
# В реальной реализации здесь - подключение к БД через SQLAlchemy/SQLModel
users_db = {}  # username -> {password_hash}
courses_db = [
    {"id": 1, "title": "Введение в Python", "description": "Базовый курс по Python"},
    {"id": 2, "title": "Основы Flutter", "description": "Создание кросплатформенных UI"},
    {"id": 3, "title": "Разработка REST API", "description": "Проектирование и реализация API"},
]


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_token(username: str) -> str:
    # Простой JWT токен demo
    payload = {"sub": username}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(lambda: None)):
    # Заглушка: в реальном коде читать Authorization header и валидировать
    return None


@app.get("/", tags=["health"])
def read_root():
    return {"status": "ok", "note": "Backend for educational platform (MVP)"}


@app.post("/register", tags=["auth"])
def register(req: RegisterRequest):
    """Регистрация пользователя (Epic 1).

    Сейчас хранение временное (in-memory). В продакшне сюда нужно подключить БД.
    """
    if req.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[req.username] = {"password_hash": hash_password(req.password)}
    return {"msg": "User registered"}


@app.post("/login", tags=["auth"])
def login(req: LoginRequest):
    """Логин — возвращает JWT (demo) (Epic 1).

    В реальной реализации нужно хранить токены/refresh tokens и хранить пользователей в БД.
    """
    user = users_db.get(req.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(req.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/courses", response_model=List[Course], tags=["courses"])
def list_courses():
    """Возвращает список курсов (Epic 2)."""
    return courses_db


# Точки расширения/интеграции с БД:
# - Подключение SQLAlchemy engine: использовать переменную окружения DATABASE_URL
# - Создать модели пользователей/курсов и миграции alembic
# - Заменить users_db и courses_db реальными запросами

