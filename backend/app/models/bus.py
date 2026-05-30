"""
Bus model with GPS and status tracking
"""

from enum import Enum
from sqlalchemy import String, Float, Integer, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class BusStatus(str, Enum):
    """Bus operational status"""
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"
    ROUTE_CHANGE = "route_change"


class Bus(Base, BaseModel):
    """Bus model for fleet management"""
    __tablename__ = "buses"

    id: Mapped[int] = mapped_column(primary_key=True)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    bus_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    capacity: Mapped[int] = mapped_column(Integer)
    status: Mapped[BusStatus] = mapped_column(default=BusStatus.ACTIVE)

    # GPS Location
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    last_gps_update: Mapped[str] = mapped_column(String(50), nullable=True)

    # Current Trip
    current_route_id: Mapped[int] = mapped_column(Integer, nullable=True)
    current_passengers: Mapped[int] = mapped_column(default=0)
    occupancy_percentage: Mapped[float] = mapped_column(default=0.0)

    # Maintenance
    total_km: Mapped[float] = mapped_column(default=0.0)
    next_maintenance_km: Mapped[float] = mapped_column(default=10000.0)
    last_maintenance_date: Mapped[str] = mapped_column(String(50), nullable=True)

    # Status
    is_connected: Mapped[bool] = mapped_column(Boolean, default=False)
    has_incidents: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("idx_bus_license", "license_plate"),
        Index("idx_bus_status", "status"),
        Index("idx_bus_route", "current_route_id"),
    )