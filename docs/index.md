# Отчет по практикам и лабораторной работе 1

Студент: **Корольков Артем**  
Дисциплина: **Средства Web-программирования**  
Тема ЛР1: **Серверное приложение FastAPI (тайм-менеджер)**

---

## Ссылки на репозиторий и выполненные работы

- Форк репозитория: [ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026)
- Ветка выполнения: [`main`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/tree/main)
- Практика 1: [папка `Pr1`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/tree/main/Pr1), [коммиты `Pr1`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/commits/main/?path=Pr1)
- Практика 2: [папка `Pr2`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/tree/main/Pr2), [коммиты `Pr2`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/commits/main/?path=Pr2)
- Практика 3: [папка `Pr3`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/tree/main/Pr3), [коммиты `Pr3`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/commits/main/?path=Pr3)
- Лабораторная работа 1: [папка `Lr1`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/tree/main/Lr1), [коммиты `Lr1`](https://github.com/ArtemKorolkov/ITMO_ICT_WebDevelopment_tools_2025-2026/commits/main/?path=Lr1)

---

## Что реализовано по практикам 1.1-1.3

### Практика 1.1 (базовый FastAPI и типизация)
- Созданы API-роуты.
- Добавлены модели данных и аннотация типов.
- Реализована структура проекта с выносом моделей в отдельные файлы.

### Практика 1.2 (SQLModel + PostgreSQL + ORM)
- Реализованы таблицы SQLModel.
- Выполнены связи one-to-many и many-to-many.
- Реализованы CRUD-методы с работой через `Session` и зависимости FastAPI.
- Добавлены вложенные ответы для связанных сущностей.

### Практика 1.3 (Alembic + ENV + gitignore)
- Добавлены `alembic.ini` и `migrations/*`.
- Настроено чтение `DB_URL` из `.env` в миграциях.
- Добавлены `.env.example` и `.gitignore` с исключением env-файлов.

---

## Лабораторная 1 (максимальный вариант, 15 баллов)

### Используемый стек
- FastAPI
- SQLModel (SQLAlchemy under the hood)
- PostgreSQL
- Alembic
- JWT (PyJWT)
- Хэширование паролей (`hashlib`)

### Модели (финальная версия)

Файл: `Lr1/app/models.py`

- `User`
- `Project`
- `Task`
- `Tag`
- `TaskTagLink` (ассоциативная сущность)
- `TimeEntry`
- `DailyPlan`

Также используются перечисления:
- `TaskPriority`
- `TaskStatus`

#### Выполнение критериев по структуре БД
- Таблиц: **7** (требование: 5+).
- `one-to-many`: `User -> Project`, `Project -> Task`, `Task -> TimeEntry`.
- `many-to-many`: `Task <-> Tag` через `TaskTagLink`.
- Ассоциативная сущность содержит поле связи `relevance_score` (кроме FK).

---

## Код подключения к БД (финальная версия)

Файл: `Lr1/app/db.py`

```python
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import DB_URL

engine = create_engine(DB_URL, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

## Реализованные эндпоинты (финальная версия)

### Системный
- `GET /` — проверка работоспособности API.

### Auth
- `POST /auth/login` — авторизация, получение JWT.

### Users
- `POST /users/register` — регистрация пользователя.
- `GET /users/me` — данные текущего пользователя.
- `GET /users/` — список пользователей.
- `PATCH /users/change-password` — смена пароля.

### Projects
- `POST /projects/` — создать проект.
- `GET /projects/` — список проектов текущего пользователя.
- `GET /projects/{project_id}/with-tasks` — проект с вложенными задачами.
- `DELETE /projects/{project_id}` — удалить проект.

### Tasks
- `POST /tasks/` — создать задачу.
- `GET /tasks/{task_id}` — получить задачу.
- `GET /tasks/{task_id}/full` — получить задачу со связанными записями времени.
- `PATCH /tasks/{task_id}` — обновить задачу.
- `DELETE /tasks/{task_id}` — удалить задачу.
- `POST /tasks/{task_id}/tags/{tag_id}` — привязать тег к задаче (с `relevance_score`).

### Tags
- `POST /tags/` — создать тег.
- `GET /tags/` — список тегов.

### Time Entries
- `POST /tasks/{task_id}/time-entries/` — добавить запись времени по задаче.

---

## Реализация требований на 15 баллов

- Регистрация и авторизация пользователей.
- Генерация JWT токена.
- Аутентификация по JWT (через dependency `get_current_user`).
- Хэширование паролей.
- API для:
  - информации о текущем пользователе,
  - списка пользователей,
  - смены пароля.

---

## Миграции и окружение

- Конфигурация Alembic: `Lr1/alembic.ini`, `Lr1/migrations/*`.
- Начальная миграция: `Lr1/migrations/versions/0001_initial.py`.
- Работа с ENV:
  - шаблон: `Lr1/.env.example`,
  - исключение env: `Lr1/.gitignore`,
  - чтение `DB_URL` в приложении и в Alembic `env.py`.

---

## Вывод

Лабораторная работа выполнена в соответствии с требованиями практик 1.1-1.3 и задания ЛР1 на максимальный балл: реализовано серверное приложение FastAPI с PostgreSQL, ORM, CRUD, связями, миграциями, JWT-аутентификацией, хэшированием и разделенной структурой проекта.
