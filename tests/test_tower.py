import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from app.main import app, get_db
from app.utils import get_logger

logger = get_logger(__name__)

pytestmark = pytest.mark.asyncio


async def override_get_db() -> None:
    raise HTTPException(status_code=400, detail="VALUE ERROR")


async def test_list_pagination() -> None:
    """In the test db, we have 100 towers, with a page_size = 10,
    we should have 10 pages
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/towers/?size=10&page=10")
    res = response.json()
    assert response.status_code == 200
    assert res.get("size") == 10
    assert res.get("page") == 10
    assert res.get("pages") == 10
    assert res.get("total") / res.get("pages") == len(res.get("items"))


async def test_list_towers_with_filters() -> None:
    """Test filtering on area, cell, mcc and net"""
    expected_cell = 22222
    expected_area = 12
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/towers/?area={expected_area}&cell={expected_cell}")
    res = response.json()
    assert response.status_code == 200
    assert res.get("total") == 1
    assert res.get("page") == 1
    assert res.get("size") == 50
    assert res.get("pages") == 1
    for tower in res.get("items"):
        assert tower.get("cell") == expected_cell
        assert tower.get("area") == expected_area


async def test_filtering_by_distance_and_radius() -> None:
    """Filtering on radius = 0 should return only one point"""
    expected_lon = 7.270173
    expected_lat = 43.703404
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/towers/?center_lon={expected_lon}&center_lat={expected_lat}&radius=0"
        )
    res = response.json()
    assert response.status_code == 200
    assert res.get("total") == 1
    assert res.get("page") == 1
    assert res.get("size") == 50
    assert res.get("pages") == 1
    for tower in res.get("items"):
        assert tower.get("lon") == expected_lon
        assert tower.get("lat") == expected_lat


async def test_filtering_by_bad_value_type() -> None:
    """Filtering on radius = 0 should return only one point"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/towers/?mcc=ok")
    assert response.status_code == 400
    assert response.json() == {"detail": "invalid literal for int() with base 10: 'ok'"}


async def test_bad_connection_to_db() -> None:
    """Filtering on radius = 0 should return only one point"""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/towers/")
    assert response.status_code == 400
    assert response.json() == {"detail": "VALUE ERROR"}
