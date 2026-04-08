# Лабораторная работа 1 (FastAPI Time Manager)

Реализовано серверное приложение для тайм-менеджмента с учетом практик 1.1-1.3 и задания на 15 баллов.

## Что реализовано

- FastAPI + SQLModel + PostgreSQL.
- 7 таблиц: `user`, `project`, `task`, `tag`, `tasktaglink`, `timeentry`, `dailyplan`.
- Связи:
  - `one-to-many`: User -> Project, Project -> Task, Task -> TimeEntry.
  - `many-to-many`: Task <-> Tag через `TaskTagLink`.
  - В ассоциативной сущности есть дополнительное поле `relevance_score`.
- CRUD API для основных сущностей.
- Вложенные объекты в ответах (например, теги у задачи).
- Регистрация/авторизация пользователей.
- JWT-токены и JWT-аутентификация.
- Хэширование паролей.
- Дополнительные методы: `users/me`, `users/`, `users/change-password`.
- Alembic миграции.
- `.env` + исключение env-файлов через `.gitignore`.

## Запуск

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Создать `.env` по примеру `.env.example`.

3. Применить миграции:

```bash
alembic upgrade head
```

4. Запустить API:

```bash
uvicorn app.main:app --reload
```

Документация: `http://127.0.0.1:8000/docs`.
