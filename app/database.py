from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app import config
from app.utils import get_logger

logger = get_logger(__name__)

global_settings = config.get_settings()
DATABASE_URL = global_settings.asyncpg_url

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
