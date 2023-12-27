import pytest
from httpx import AsyncClient

from app.main import app
from app.utils import get_logger

logger = get_logger(__name__)

pytestmark = pytest.mark.asyncio


async def test_root() -> None:
    """Test home page"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/?mcc=1&net=1")
    assert response.status_code == 200
