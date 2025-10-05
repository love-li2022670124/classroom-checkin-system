import os
from datetime import timedelta


class Settings:
    db_url: str = os.getenv("DB_URL", "mysql+pymysql://root:password@127.0.0.1:3306/ClassCheckInDB")
    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = "HS256"
    jwt_expire: timedelta = timedelta(minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "720")))


settings = Settings()
