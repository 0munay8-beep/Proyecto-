"""
Route model with waypoints and optimization
"""

from sqlalchemy import String, Integer, Float, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class Route(Base, BaseModel):
    """Route model for managing bus routes"""
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000), nullable=True)

    # Route Details
    start_point: Mapped[str] = mapped_column(String(255))
    end_point: Mapped[str] = mapped_column(String(255))
    distance_km: Mapped[float] = mapped_column(Float)
    estimated_time_minutes: Mapped[int] = mapped_column(Integer)

    # Schedule
    first_departure: Mapped[str] = mapped_column(String(50))
    last_departure: Mapped[str] = mapped_column(String(50))
    frequency_minutes: Mapped[int] = mapped_column(Integer, default=15)

    # Waypoints (GeoJSON)
    waypoints: Mapped[dict] = mapped_column(JSON, nullable=True)
    stops: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Optimization
    estimated_demand: Mapped[int] = mapped_column(Integer, default=0)
    peak_hours: Mapped[str] = mapped_column(String(255), nullable=True)

    __table_args__ = (Index("idx_route_number", "route_number"),)