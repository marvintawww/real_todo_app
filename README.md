# Todo App API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

> Backend-ориентированное веб-приложение для управления задачами (Todo List) с аутентификацией и авторизацией.

## 📋 Описание проекта

RESTful API для управления задачами с полноценной системой аутентификации на основе JWT токенов. Проект построен с использованием современных технологий и паттернов разработки, демонстрирующих навыки backend-разработки.

## 🏗 Архитектура

```
src/
├── config.py          # Конфигурация приложения
├── main.py            # Точка входа в приложение
├── core/              # Ядро приложения (токены, безопасность)
├── database/          # Настройка базы данных
├── dependencies/      # Зависимости FastAPI (DI)
├── entities/          # DTO/Схемы запросов и ответов
├── exceptions/        # Кастомные исключения и обработчики
├── models/            # SQLAlchemy модели
├── repositories/      # Слой доступа к данным
├── routes/            # API эндпоинты
├── services/          # Бизнес-логика
└── utils/             # Утилиты
```

### Паттерн проектирования

Приложение использует **слоистую архитектуру** (Layered Architecture):

```
Request → Routes → Services → Repositories → Models → Database
```

Каждый слой имеет свою зону ответственности:
- **Routes** — обработка HTTP запросов, валидация
- **Services** — бизнес-логика
- **Repositories** — доступ к данным
- **Models** — представление данных в БД

## 🛠 Технологический стек

| Категория | Технология |
|-----------|------------|
| Framework | FastAPI |
| Язык | Python 3.11+ |
| База данных | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 (async) |
| Драйвер БД | asyncpg |
| Аутентификация | JWT (python-jose) |
| Хеширование | Passlib + Argon2 |
| Миграции | Alembic |
| Контейнеризация | Docker Compose |
| Тестирование | Pytest + httpx |

## 📚 API Эндпоинты

### Аутентификация

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/auth/register` | Регистрация нового пользователя |
| `POST` | `/api/v1/auth/login` | Вход в систему |
| `POST` | `/api/v1/auth/logout` | Выход из системы |
| `POST` | `/api/v1/auth/refresh` | Обновление пары токенов |

### Пользователи

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/api/v1/users/profile` | Получение профиля текущего пользователя |

### Типы задач

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/api/v1/types` | Список типов задач |
| `POST` | `/api/v1/types/type` | Создание типа задачи |
| `GET` | `/api/v1/types/type/{type_id}` | Получение типа задачи |

### Задачи

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/api/v1/tasks` | Список задач пользователя |
| `POST` | `/api/v1/tasks/create/{type_id}` | Создание задачи |
| `GET` | `/api/v1/tasks/{task_id}` | Получение задачи |
| `PATCH` | `/api/v1/tasks/{task_id}` | Обновление задачи |
| `DELETE` | `/api/v1/tasks/{task_id}` | Удаление задачи |
| `PATCH` | `/api/v1/tasks/{task_id}/status` | Изменение статуса задачи |

## 🔐 Аутентификация и авторизация

### Flow

```
1. Регистрация: POST /api/v1/auth/register
   → Создание пользователя
   → Возврат пары токенов (access + refresh)

2. Вход: POST /api/v1/auth/login
   → Проверка credentials
   → Возврат пары токенов

3. Доступ к защищённым ресурсам:
   → Заголовок Authorization: Bearer <access_token>
   → Валидация токена
   → Извлечение user_id из payload

4. Обновление токенов: POST /api/v1/auth/refresh
   → Валидация refresh_token
   → Генерация новой пары токенов
   → Инвалидация старого refresh_token

5. Выход: POST /api/v1/auth/logout
   → Инвалидация refresh_token
```

### Структура JWT токена

**Access Token** (время жизни: 15 минут):
```json
{
  "sub": "user_id",
  "type": "access",
  "exp": "timestamp"
}
```

**Refresh Token** (время жизни: 7 дней):
```json
{
  "sub": "user_id",
  "type": "refresh",
  "exp": "timestamp"
}
```

## 🚀 Запуск проекта

### Требования

- Python 3.11+
- Docker и Docker Compose

### Вариант 1: Docker Compose (рекомендуемый)

```bash
# Клонирование репозитория
git clone <repository-url>
cd real_todo_app

# Запуск всех сервисов
cd src
docker-compose up -d
```

Сервисы:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **PgAdmin**: http://localhost:5050 (admin@admin.com / admin)

### Вариант 2: Локальный запуск

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
# Создайте файл .env на основе .env.example
cp .env.example .env

# Запуск PostgreSQL через Docker
docker run -d \
  --name todo-postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=todo \
  -p 5432:5432 \
  postgres:15

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn src.main:app --reload
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=src --cov-report=html

# Запуск только интеграционных тестов
pytest tests/integration/

# Запуск только юнит-тестов
pytest tests/unit/
```

### Структура тестов

```
tests/
├── conftest.py              # Общие фикстуры
├── integration/             # Интеграционные тесты
│   ├── conftest.py
│   ├── test_jwt_repo.py
│   ├── test_task_repo.py
│   ├── test_type_repo.py
│   └── test_user_repo.py
└── unit/                    # Юнит-тесты
```

## 📁 Структура проекта

```
real_todo_app/
├── README.md                # Документация
├── requirements.txt         # Python зависимости
├── alembic.ini              # Конфигурация Alembic
├── pytest.ini               # Конфигурация Pytest
├── migrations/              # Миграции БД
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── src/                     # Исходный код
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── docker-compose.yml
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── entities/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   └── utils/
├── frontend/                # Фронтенд (HTML/JS)
└── tests/                   # Тесты
```

## 🔑 Ключевые особенности для портфолио

### Backend навыки

- ✅ **Асинхронное программирование** — полная поддержка async/await
- ✅ **RESTful API** — правильная структура эндпоинтов
- ✅ **JWT Аутентификация** — access + refresh токены с blacklist
- ✅ **Dependency Injection** — использование FastAPI Depends
- ✅ **Repository Pattern** — разделение логики доступа к данным
- ✅ **Migrations** — управление схемой БД через Alembic
- ✅ **Docker** — контейнеризация приложения
- ✅ **Тестирование** — unit и integration тесты
- ✅ **Type Hints** — полная типизация Python
- ✅ **Error Handling** — кастомные исключения и обработчики

## 📄 Лицензия

MIT License

---

Разработано с использованием FastAPI и PostgreSQL

