"""
Incident model for anomaly tracking
"""

from enum import Enum
from sqlalchemy import String, Integer, Boolean, Float, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class IncidentSeverity(str, Enum):
    """Severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentStatus(str, Enum):
    """Incident status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentType(str, Enum):
    """Types of incidents"""
    MECHANICAL = "mechanical"
    DRIVER_BEHAVIOR = "driver_behavior"
    TRAFFIC = "traffic"
    PASSENGER_INCIDENT = "passenger_incident"
    GPS_ANOMALY = "gps_anomaly"
    PERFORMANCE = "performance"
    SAFETY = "safety"


class Incident(Base, BaseModel):
    """Incident model"""
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    bus_id: Mapped[int] = mapped_column(Integer, index=True)
    incident_type: Mapped[IncidentType] = mapped_column()
    severity: Mapped[IncidentSeverity] = mapped_column()
    status: Mapped[IncidentStatus] = mapped_column(default=IncidentStatus.OPEN)

    # Details
    description: Mapped[str] = mapped_column(String(1000))
    detected_by: Mapped[str] = mapped_column(String(50))
    anomaly_score: Mapped[float] = mapped_column(Float, nullable=True)

    # Location
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Resolution
    resolution_notes: Mapped[str] = mapped_column(String(1000), nullable=True)
    resolved_by: Mapped[int] = mapped_column(Integer, nullable=True)

    # Notifications
    notified_to_operators: Mapped[bool] = mapped_column(default=False)
    sms_sent: Mapped[bool] = mapped_column(default=False)
    ticket_generated: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        Index("idx_incident_bus", "bus_id"),
        Index("idx_incident_severity", "severity"),
        Index("idx_incident_status", "status"),
    )