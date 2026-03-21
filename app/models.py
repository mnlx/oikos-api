from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(255))
    base_url: Mapped[str] = mapped_column(String(500))
    active: Mapped[bool] = mapped_column(Boolean)


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    trigger_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    source_code: Mapped[str] = mapped_column(String(120))
    strategy: Mapped[str] = mapped_column(String(50))
    items_seen: Mapped[int] = mapped_column(Integer)
    items_inserted: Mapped[int] = mapped_column(Integer)
    items_updated: Mapped[int] = mapped_column(Integer)
    error_count: Mapped[int] = mapped_column(Integer)
    last_error: Mapped[str | None] = mapped_column(Text)


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    external_id: Mapped[str] = mapped_column(String(255))
    canonical_url: Mapped[str] = mapped_column(String(1000))
    title: Mapped[str] = mapped_column(String(500))
    transaction_type: Mapped[str] = mapped_column(String(30))
    property_type: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(120))
    state: Mapped[str] = mapped_column(String(2))
    neighborhood: Mapped[str | None] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(String(500))
    latitude: Mapped[float | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[float | None] = mapped_column(Numeric(10, 7))
    price_sale: Mapped[float | None] = mapped_column(Numeric(14, 2))
    price_rent: Mapped[float | None] = mapped_column(Numeric(14, 2))
    condo_fee: Mapped[float | None] = mapped_column(Numeric(14, 2))
    iptu: Mapped[float | None] = mapped_column(Numeric(14, 2))
    bedrooms: Mapped[int | None] = mapped_column(Integer)
    bathrooms: Mapped[int | None] = mapped_column(Integer)
    parking_spaces: Mapped[int | None] = mapped_column(Integer)
    area_m2: Mapped[float | None] = mapped_column(Numeric(10, 2))
    description: Mapped[str | None] = mapped_column(Text)
    broker_name: Mapped[str | None] = mapped_column(String(255))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean)
    raw_payload: Mapped[dict] = mapped_column(JSONB)

    source: Mapped[Source] = relationship()
