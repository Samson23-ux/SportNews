import sentry_sdk
from hashlib import sha256
from typing import Optional
from uuid import UUID, uuid4
from jose import jwt, JWTError
from pwdlib import PasswordHash
from sentry_sdk import logger as sentry_logger
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timezone, timedelta
from pymongo.asynchronous.client_session import AsyncClientSession
from authlib.integrations.starlette_client import OAuth, OAuthError


from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.api.v1.repo.auth_repo import auth_repo_v1
from app.api.v1.schemas.auth import TokenDataV1, RefreshTokenV1, TokenStatus


arg2_hasher = PasswordHash([Argon2Hasher()])


# oauth2
oauth: OAuth = OAuth()

oauth.register(
    name="google",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email",
        "redirect_url": "http://localhost:8000/api/v1/auth/callback",
    },
)


async def hash_password(password: str) -> str:
    password: str = password + settings.ARGON2_PEPPER
    return arg2_hasher.hash(password)


async def hash_refresh_token(refresh_token: str) -> str:
    return sha256(refresh_token).hexdigest()


async def verify_password(password: str, hash_password: str) -> bool:
    password: str = password + settings.ARGON2_PEPPER
    return arg2_hasher.verify(password, hash_password)


async def create_access_token(
    token_data: TokenDataV1, expire_time: Optional[datetime] = None
) -> str:
    if not expire_time:
        expire_time: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_TIME
        )
    else:
        expire_time: datetime = expire_time + datetime.now(timezone.utc)

    payload: dict = {
        "sub": str(token_data.email),
        "exp": expire_time,
        "iat": datetime.now(timezone.utc),
    }

    token: str = jwt.encode(
        claims=payload,
        key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


async def create_refresh_token(
    token_data: TokenDataV1, expire_time: Optional[datetime] = None
) -> tuple:
    if not expire_time:
        expire_time: datetime = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_TIME
        )
    else:
        expire_time: datetime = expire_time + datetime.now(timezone.utc)

    payload: dict = {
        "sub": str(token_data.email),
        "exp": expire_time,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid4()),
    }

    token: str = jwt.encode(
        claims=payload,
        key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, payload["jti"], expire_time


# verify token
async def decode_token(token: str, key: str) -> dict | None:
    try:
        payload: dict = jwt.decode(
            token=token, key=key, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        sentry_logger.error("User provided an invalid token")
        sentry_sdk.capture_exception(e)
        return None


# verify the received id_token
async def decode_id_token(token: str, key: str) -> dict | None:
    try:
        payload: dict = jwt.decode(
            token=token,
            key=key,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.CLIENT_ID,
        )
        return payload
    except OAuthError as e:
        sentry_logger.error("Invalid id_token received")
        sentry_sdk.capture_exception(e)
        return None


# verify the received refresh token from client
async def verify_refresh_token(
    refresh_token: str, db: AsyncClientSession
) -> RefreshTokenV1:
    if refresh_token is None:
        sentry_logger.error("User not authenticated")
        raise AuthenticationError()

    payload: dict | None = await decode_token(
        refresh_token, settings.REFRESH_TOKEN_SECRET_KEY
    )

    if payload is None:
        sentry_logger.error("User not authenticated")
        raise AuthenticationError()

    token_id: UUID = payload.get("jti")

    refresh_token: RefreshTokenV1 | None = await auth_repo_v1.get_refresh_token(
        token_id, db
    )

    if (
        refresh_token.status == TokenStatus.REVOKED
        or refresh_token.status == TokenStatus.USED
    ):
        sentry_logger.error("User not authenticated")
        raise AuthenticationError()

    return refresh_token
