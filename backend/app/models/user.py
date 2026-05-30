"""
User model with RBAC
"""

from enum import Enum
from sqlalchemy import String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, BaseModel


class UserRole(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"
    USER = "user"


class User(Base, BaseModel):
    """User model with role-based access control"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[str] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_role", "role"),
    )