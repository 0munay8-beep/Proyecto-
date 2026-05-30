"""
Analytics model for historical data
"""

from sqlalchemy import String, Integer, Float, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class Analytics(Base, BaseModel):
    """Analytics model"""
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(Integer, index=True)
    date: Mapped[str] = mapped_column(String(50), index=True)

    # Daily statistics
    total_trips: Mapped[int] = mapped_column(Integer, default=0)
    total_passengers: Mapped[int] = mapped_column(Integer, default=0)
    average_occupancy: Mapped[float] = mapped_column(default=0.0)
    peak_occupancy: Mapped[float] = mapped_column(default=0.0)

    # Performance
    on_time_percentage: Mapped[float] = mapped_column(default=0.0)
    average_delay_minutes: Mapped[float] = mapped_column(default=0.0)
    incidents_count: Mapped[int] = mapped_column(default=0)

    # Seasonality & Trends
    day_of_week: Mapped[str] = mapped_column(String(20))
    is_holiday: Mapped[bool] = mapped_column(default=False)
    weather_conditions: Mapped[str] = mapped_column(String(255), nullable=True)
    temperature: Mapped[float] = mapped_column(nullable=True)

    # Forecast Data
    seasonal_index: Mapped[float] = mapped_column(nullable=True)
    trend_value: Mapped[float] = mapped_column(nullable=True)
    prediction_confidence: Mapped[float] = mapped_column(nullable=True)

    # Custom metrics
    metrics_data: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        Index("idx_analytics_route_date", "route_id", "date"),
        Index("idx_analytics_date", "date"),
    )