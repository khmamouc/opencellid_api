from typing import Any, Dict

from sqlalchemy import and_, select, true
from sqlalchemy.sql.selectable import Select

from app.models import Tower
from app.schemas import TowerBase


async def list_towers(query_parameters: Dict[str, str]) -> Select[Any]:
    """List towers filtered by some Tower fields
    and located within a circular boundary
    specified by a latitude, longitude, and radius.
    """
    filters = {
        param: value
        for param, value in dict(query_parameters).items()
        if param in TowerBase.model_fields
    }
    center_lon = query_parameters.get("center_lon")
    center_lat = query_parameters.get("center_lat")
    radius = query_parameters.get("radius")
    where_clause = and_(
        Tower.cell == int(filters.get("cell", "0")) if "cell" in filters else true(),
        Tower.lat == float(filters.get("lat", "0")) if "lat" in filters else true(),
        Tower.lon == float(filters.get("lon", "0")) if "lon" in filters else true(),
        Tower.mcc == int(filters.get("mcc", "0")) if "mcc" in filters else true(),
        Tower.net == int(filters.get("net", "0")) if "net" in filters else true(),
        Tower.area == int(filters.get("area", "0")) if "area" in filters else true(),
        Tower.radio == filters.get("radio") if "radio" in filters else true(),
        Tower.range == int(filters.get("range", "0")) if "range" in filters else true(),
        Tower.unit == int(filters.get("unit", "0")) if "unit" in filters else true(),
        Tower.distance_from_point(float(center_lon), float(center_lat)) <= float(radius)
        if (center_lon and center_lat and radius)
        else true(),
    )
    query = select(Tower).where(where_clause)
    return query
