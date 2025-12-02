# Three In Row (backend + frontend)
Приложение для игры «три в ряд» с таблицей лидеров. Stateless: всё состояние хранится в PostgreSQL.

## Режимы игры
- **Easy**: поле 12×12, цель 40 очков, очки за любые фишки, без штрафа за пустой свап.
- **Medium**: 8×8, цель 50, включён one-swap reset (свап без матча сбрасывает поле и снимает 5 очков).
- **Hard**: 8×8, цель 25, one-swap reset + random item (очки только за один случайный тип фишки).
- **Custom**: на экране создания можно задать размеры, цель, количество типов фишек, one-swap reset, random item (и зафиксировать конкретный тип), таймаут.

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
