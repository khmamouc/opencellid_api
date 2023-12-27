from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from asyncpg.exceptions import _base
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from app.crud import list_towers as crud_list_towers
from app.database import Base
from app.database import SessionLocal as SessionLocal
from app.database import engine
from app.schemas import TowerBase
from app.utils import get_logger

description = """
OpenCellid API helps getting information about Cellular Towers. 🚀

## Towers

You will be able to:

* **List cellular towers**
"""
logger = get_logger(__name__)

app = FastAPI(
    title="OpenCellidAPI",
    description=description,
    summary="Cellular towers information",
    version="0.0.1",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


async def get_db() -> AsyncGenerator[Any, Any]:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except _base.PostgresError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    async with SessionLocal() as session:
        yield session


@app.get("/")
def root(request: Request) -> _TemplateResponse:
    homepage = "homepage.html"
    template = templates.TemplateResponse(homepage, {"request": request})
    return template


@app.get("/towers/", response_model=Page[TowerBase])
async def list_towers(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List towers"""
    query_parameters = dict(request.query_params)
    try:
        query = await crud_list_towers(query_parameters)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return await paginate(db, query)


add_pagination(app)
