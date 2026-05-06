# Задача 1. Сравнение threading, multiprocessing и async

Цель: сравнить три подхода параллельного выполнения на задаче вычисления суммы чисел от `1` до `10_000_000_000_000`.

## Файлы

- `threading_sum.py` — реализация через `threading`.
- `multiprocessing_sum.py` — реализация через `multiprocessing`.
- `async_sum.py` — реализация через `asyncio`.

Во всех файлах реализована функция `calculate_sum(start, end)`, а диапазон разбивается на 8 подзадач.

## Запуск

```bash
python threading_sum.py
python multiprocessing_sum.py
python async_sum.py
```

## Ожидаемые выводы

- Все варианты возвращают одинаковую сумму.
- Для CPU-задач подход `multiprocessing` обычно полезнее `threading` из-за GIL.
- `asyncio` без выноса в процессы/потоки не ускоряет CPU-heavy вычисления, но удобен для I/O задач.
