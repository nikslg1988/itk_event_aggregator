# ITK Event Aggregator

Backend сервис для агрегации мероприятий из внешнего Event Provider.

Сервис синхронизирует события, получает доступные места, регистрирует пользователей и отменяет регистрацию через HTTP API внешнего провайдера.

## Возможности

- получение изменённых мероприятий;
- постраничная синхронизация событий;
- получение списка свободных мест;
- регистрация пользователя на мероприятие;
- отмена регистрации;
- асинхронная работа через HTTP API;
- unit тестирование с использованием pytest.

---

## Используемые технологии

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL 17
- Alembic
- httpx
- Pydantic v2
- pytest
- Ruff
- Docker
- Docker Compose

---

## Структура проекта

```text
.
├── alembic/
├── app/
│   ├── api/
│   ├── cache/
│   ├── clients/
│   ├── core/
│   ├── db/
│   ├── dependencies/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Установка

Клонировать репозиторий

```bash
git clone <repository-url>
cd itk-event-aggregator
```

Создать виртуальное окружение

```bash
uv venv
source .venv/bin/activate
```

Установить зависимости

```bash
uv sync
```

---

## Переменные окружения

Создать файл `.env` на основе шаблона

```text
cp .env.example .env
```

---

## Запуск PostgreSQL

```bash
docker compose up -d db
```

Проверить состояние контейнера

```bash
docker compose ps
```

---

## Применение миграций

```bash
alembic upgrade head
```

---

## Запуск приложения

```bash
uv run uvicorn app.main:app --reload
```

По умолчанию приложение будет доступно по адресу

```
http://127.0.0.1:8000
```

---

## Запуск тестов

Все тесты

```bash
uv run pytest
```

Подробный вывод

```bash
uv run pytest -vv
```

---

## Покрытие тестами

### EventsProviderClient

Проверены:

- получение изменённых событий;
- получение страницы событий;
- получение доступных мест;
- регистрация;
- отмена регистрации.

Во всех тестах проверяются:

- корректность HTTP запроса;
- параметры запроса;
- сериализация тела;
- десериализация ответа.

### EventsPaginator

Проверены сценарии:

- одна страница;
- несколько страниц;
- пустая страница.

Проверяется:

- последовательность вызовов клиента;
- переход между страницами;
- порядок возвращаемых событий.

---

## Архитектура

Проект разделён на независимые слои.

```text
API
    │
Services
    │
Repositories
    │
Database

Clients
    │
External Event Provider
```

Каждый слой отвечает только за собственную область ответственности.

---

## Качество кода

Используются:

- Ruff
- pytest
- pytest-asyncio
- unittest.mock

---

## Статус проекта

Проект находится в активной разработке.
