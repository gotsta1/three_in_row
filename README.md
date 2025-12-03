# Three In Row (backend + frontend)
Приложение для игры «три в ряд» с таблицей лидеров. Stateless: всё состояние хранится в PostgreSQL.

## Режимы игры
- **Easy**: поле 12×12, цель 40 очков. Очки идут за любые фишки, пустой свап запрещён (400), штрафов нет.
- **Medium**: 8×8, цель 50. Включён one-swap reset — любой свап без матча сбрасывает поле и снимает 5 очков (не ниже нуля).
- **Hard**: 8×8, цель 25. One-swap reset + режим random item: очки начисляются только за один случайно выбранный тип фишки (показывается в инфо игры); остальные сгорают без очков.
- **Custom**: задаются размеры, цель, количество разных цветов, one-swap reset, можно зафиксировать нужный тип. Штраф за сброс — 5 очков.

Таймаут без действий — 1 час, после чего игра считается проигранной.

## Стек
- Backend: FastAPI, SQLAlchemy Async, Alembic, PostgreSQL.
- Frontend: React + Vite.
- Инфра: Docker Compose (db, backend, frontend, nginx, adminer).

## Запуск
### Через Docker (рекомендуется)
```bash
cp .env.example .env   # при необходимости поправьте URL'ы
docker compose up --build
```
Сервисы: backend `:8000`, frontend `:5173`, nginx `:80`, adminer `:8080` (логин: postgres/postgres, host: db, db: three_in_row).

### Локально без Docker
1) Поднимите PostgreSQL и создайте БД `three_in_row`; задайте `DATABASE_URL`.
2) Бэкенд:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload --app-dir backend/src
```
3) Фронтенд:
```bash
cd frontend
npm install
npm run dev -- --host
```

## Основные эндпоинты
- `POST /games` — создать игру (difficulty/custom + player).
- `GET /games/{id}` — получить состояние.
- `POST /games/{id}/swap` — сделать ход; в ответе цепочка снимков (каждый шаг падения/сгорания, reset_applied при авто-регенерации).
- `POST /games/{id}/reset` — сброс поля, штраф -5.
- `GET /leaderboard?difficulty=` — топ-10 по времени (фильтр по сложности).
- `POST /leaderboard` — сохранить результат вручную (обычно пишется авто при победе).
- `GET /health` — проверка живости.
- Swagger/OpenAPI: `/docs`.

## Автор
Беляев Вадим
