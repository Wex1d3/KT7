# KT6 — Fullstack Task Manager API

Учебный backend-проект на FastAPI: пользователи, проекты и задачи.

## Запуск на Windows (CMD)

1. Установите Docker Desktop и запустите его.
2. Откройте CMD в папке проекта.
3. Создайте файл `.env` из шаблона:

```cmd
copy .env.example .env
```

4. Запустите весь стек:

```cmd
docker compose up --build
```

После запуска:
- Swagger UI: http://localhost:8000/docs
- Проверка: http://localhost:8000/health
- PostgreSQL: localhost:5432
- Redis: localhost:6379

Остановка: `Ctrl+C`, затем `docker compose down`.
Удаление БД вместе с данными: `docker compose down -v`.

## Основные эндпоинты

- `POST /auth/register` — регистрация (JSON: `email`, `password`, минимум 8 символов).
- `POST /auth/login` — вход через OAuth2 Password Flow. В форме OAuth2 поле `username` заполняется email, поле `password` — паролем. Лимит: 5 запросов в минуту.
- `GET /auth/me` — текущий пользователь.
- `GET /auth/admin-only` — пример RBAC, доступен только роли `admin`.
- `POST /projects` — создать проект.
- `GET /projects` — список своих проектов.
- `POST /tasks` — создать задачу в своём проекте; ставится фоновая задача Celery.
- `GET /tasks` — список задач своих проектов.

Для запросов после входа нажмите Authorize в Swagger и вставьте access token.

## Миграции и тесты

При старте контейнера выполняется `alembic upgrade head`.
Локально (при активной БД и установленном Python):
```cmd
pip install -r requirements.txt
alembic upgrade head
pytest -q
```

## Назначение роли администратора

После регистрации можно вручную назначить роль в PostgreSQL:
```sql
UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';
```

## Деплой

Проект подготовлен для контейнерного деплоя. Для Railway создайте сервисы PostgreSQL и Redis, подключите репозиторий и задайте переменные окружения `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `CORS_ORIGINS_RAW`. Для `DATABASE_URL` используйте формат `postgresql+psycopg://...`. Отдельный worker-сервис запускайте командой:
`celery -A app.tasks.celery_app worker --loglevel=info`.

Публичный адрес не создан автоматически: для реального деплоя нужны ваш аккаунт и доступ к Railway/VPS.
