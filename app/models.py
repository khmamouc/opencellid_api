import datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import Function

from app.utils import get_logger

from .database import Base

logger = get_logger(__name__)


class Tower(Base):
    __tablename__ = "tower"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    radio: Mapped[str] = mapped_column()
    mcc: Mapped[int] = mapped_column()
    net: Mapped[int] = mapped_column()
    area: Mapped[int] = mapped_column()
    cell: Mapped[int] = mapped_column()
    unit: Mapped[int] = mapped_column()
    lon: Mapped[float] = mapped_column()
    lat: Mapped[float] = mapped_column()
    range: Mapped[int] = mapped_column()
    samples: Mapped[int] = mapped_column()
    changeable: Mapped[bool] = mapped_column()
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    averageSignal: Mapped[int] = mapped_column()

    __table_args__ = (
        UniqueConstraint("mcc", "net", "area", "cell", name="tower_identifier"),
    )

    @hybrid_method
    def distance_from_point(self, lon: float, lat: float) -> None:
        pass

    @distance_from_point.expression
    def distance_from_point_cls(cls, lon: float, lat: float) -> Function[Any]:
        """Computes the distance btw two points
        given the longitude and latitude
        """
        distance = func.ST_Distance(
            func.ST_Point(cls.lon, cls.lat), func.ST_Point(lon, lat)
        )
        return distance
