## Backend

- Framework: FastAPI
- DB: MySQL (database: `ClassCheckInDB`)
- ORM: SQLAlchemy 2.0
- Cache: Redis

### Dev Run (Windows PowerShell)
```bash
python -m venv .venv; . .venv/Scripts/Activate.ps1
pip install -r backend/requirements.txt
$env:DB_URL = "mysql+pymysql://USER:PASSWORD@127.0.0.1:3306/ClassCheckInDB"
$env:REDIS_URL = "redis://127.0.0.1:6379/0"
$env:JWT_SECRET = "change-me"
uvicorn backend.app.main:app --reload --port 8000
```
