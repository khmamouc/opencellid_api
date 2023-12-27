import datetime

from pydantic import BaseModel, ConfigDict


class TowerBase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    radio: str
    mcc: int
    net: int
    area: int
    cell: int
    unit: int
    lon: float
    lat: float
    range: int
    samples: int
    changeable: bool
    created: datetime.datetime
    updated: datetime.datetime
    averageSignal: int
