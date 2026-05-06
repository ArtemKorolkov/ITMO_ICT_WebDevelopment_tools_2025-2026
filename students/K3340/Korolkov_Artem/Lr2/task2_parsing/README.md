# Задача 2. Параллельный парсинг и запись в БД

Цель: сравнить `threading`, `multiprocessing`, `asyncio` для I/O-задачи (загрузка страниц и сохранение заголовков в БД из ЛР1).

## Что сохраняется в БД

Используется таблица `tag` из проекта ЛР1 (в БД `time_manager_db`).
В поле `name` записывается заголовок страницы (`<title>`) с суффиксом времени, чтобы избежать конфликта `UNIQUE`.

## Файлы

- `threading_parser.py`
- `multiprocessing_parser.py`
- `async_parser.py`

Во всех вариантах есть функция `parse_and_save(url, ...)`.

## Подготовка

1. Создайте `.env` рядом с файлами ЛР2 и укажите `DB_URL`.
2. Убедитесь, что БД из ЛР1 доступна и таблица `tag` существует.
3. Установите зависимости:

```bash
pip install -r ../requirements.txt
```

## Запуск

```bash
python threading_parser.py
python multiprocessing_parser.py
python async_parser.py
```

Каждый скрипт выводит сохраненные URL/заголовки и общее время выполнения.
