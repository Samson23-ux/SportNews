import sentry_sdk
from zoneinfo import ZoneInfo
from fastapi import FastAPI, Request
from datetime import datetime, timezone
import sentry_sdk.logger as sentry_logger


from app.core.config import settings


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)


sentry_sdk.init(
    dsn=settings.SENTRY_SDK_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    profile_lifecycle="trace",
    enable_logs=True,
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    utc_dt: datetime = datetime.now(timezone.utc)
    app_tz = ZoneInfo(settings.API_DEFAULT_TIMEZONE)
    app_dt: datetime = utc_dt.astimezone(app_tz)

    log_msg: str = f"{request.method} {request.url} {app_dt}"

    sentry_logger.info(log_msg)

    response = await call_next(request)
    response.headers["X-App-Name"] = "SportNews API"

    return response


@app.get("/api/v1/health", status_code=200)
async def check_health():
    return {"message": "OK"}
