"""
Maintenance ticket model
"""

from enum import Enum
from sqlalchemy import String, Integer, Float, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class TicketPriority(str, Enum):
    """Priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TicketStatus(str, Enum):
    """Status"""
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"


class MaintenanceTicket(Base, BaseModel):
    """Maintenance ticket model"""
    __tablename__ = "maintenance_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    bus_id: Mapped[int] = mapped_column(Integer, index=True)
    incident_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # Details
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    priority: Mapped[TicketPriority] = mapped_column()
    status: Mapped[TicketStatus] = mapped_column(default=TicketStatus.OPEN)

    # Assignment
    assigned_to: Mapped[int] = mapped_column(Integer, nullable=True)
    estimated_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    actual_hours: Mapped[int] = mapped_column(Integer, nullable=True)

    # Scheduling
    scheduled_date: Mapped[str] = mapped_column(String(50), nullable=True)
    completed_date: Mapped[str] = mapped_column(String(50), nullable=True)

    # Resolution
    resolution_notes: Mapped[str] = mapped_column(String(1000), nullable=True)
    parts_replaced: Mapped[str] = mapped_column(String(255), nullable=True)

    # Auto-generation
    auto_generated: Mapped[bool] = mapped_column(default=False)
    auto_priority_score: Mapped[float] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("idx_ticket_bus", "bus_id"),
        Index("idx_ticket_status", "status"),
        Index("idx_ticket_priority", "priority"),
    )