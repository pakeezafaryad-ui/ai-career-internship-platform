
import os
from pathlib import Path

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(512), nullable=False
    )


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    plan_json: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    progress_percent: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    company: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(40), default="Interested", nullable=False
    )


# Keep the database path configurable for deployment.
database_path = Path(
    os.getenv("CAREER_DB_PATH", "career_app.db")
).resolve()

engine = create_engine(
    f"sqlite:///{database_path}",
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db():
    """Create database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

