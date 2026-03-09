from pymongo import AsyncMongoClient


from app.core.config import settings


mongo_client = AsyncMongoClient(
    settings.MONGO_DB_URI,
    tz_aware=True,
    maxConnecting=5,
    appname=settings.API_TITLE,
    tls=settings.ENVIRONMENT == "production",
)
