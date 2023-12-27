import argparse
import asyncio
import os

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models import Base, Tower
from app.utils import get_logger

logger = get_logger(__name__)

pg_user: str = os.getenv("POSTGRES_USER", "cell_user")
pg_pass: str = os.getenv("POSTGRES_PASSWORD", "S3cret")
pg_database: str = os.getenv("POSTGRES_DB", "cell_db")

# engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@db:5432/{pg_database}")
DATABASE_URL = f"postgresql+asyncpg://{pg_user}:{pg_pass}@db:5432/{pg_database}"
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
)

# Base.metadata.create_all(bind=engine)
chunksize = 10000

Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Session = sessionmaker(bind=engine)
session = Session()

# csv_file = "data/270.csv"


async def insert_towers(chunk):
    """INSERT statements via the ORM (batched with RETURNING if available),
    fetching generated row id"""
    # session = Session(bind=engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with Session() as session:
        try:
            session.add_all([Tower(**row) for _, row in chunk.iterrows()])
            await session.flush()
            await session.commit()
        except (
            Exception
        ) as error:  # TODO:  couldn't catch IntegrityError for async mode
            logger.warning(error.__dict__.get("orig"))
            await session.rollback()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script with parameters.")
    # Add arguments
    parser.add_argument(
        "--csv_file",
        type=str,
        required=True,
        help="path to csv file containing tower data",
    )
    args = parser.parse_args()
    csv_file = args.csv_file

    for df in pd.read_csv(csv_file, chunksize=chunksize):
        df["changeable"] = df["created"].astype(bool)
        df["created"] = pd.to_datetime(df["created"], unit="s").dt.tz_localize("UTC")
        df["updated"] = pd.to_datetime(df["updated"], unit="s").dt.tz_localize("UTC")
        asyncio.run(insert_towers(df))

    logger.info(f"{csv_file} was successfully feeded")
