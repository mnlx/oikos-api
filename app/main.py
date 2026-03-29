from datetime import datetime
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Select, desc, func, or_, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import MartListing, ScrapeRun, Source
from app.schemas import ListingDetail, ListingListItem, SummaryResponse


settings = get_settings()
app = FastAPI(title="Oikos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_float(value: Decimal | float | int | None) -> float | None:
    if value is None:
        return None
    return float(value)


def serialize_listing(listing: MartListing) -> ListingDetail:
    return ListingDetail(
        id=listing.id,
        title=listing.title,
        canonical_url=listing.canonical_url,
        transaction_type=listing.transaction_type,
        property_type=listing.property_type,
        city=listing.city,
        state=listing.state,
        neighborhood=listing.neighborhood,
        address=listing.address,
        latitude=to_float(listing.latitude),
        longitude=to_float(listing.longitude),
        price_sale=to_float(listing.price_sale),
        price_rent=to_float(listing.price_rent),
        condo_fee=to_float(listing.condo_fee),
        iptu=to_float(listing.iptu),
        bedrooms=listing.bedrooms,
        bathrooms=listing.bathrooms,
        parking_spaces=listing.parking_spaces,
        area_m2=to_float(listing.area_m2),
        broker_name=listing.broker_name,
        description=listing.description,
        published_at=listing.published_at,
        first_seen_at=listing.first_seen_at,
        last_seen_at=listing.last_seen_at,
        last_scraped_at=listing.last_scraped_at,
        is_active=listing.is_active,
        source_code=listing.source_code,
        source_name=listing.source_name,
        image_uris=listing.image_uris or [],
        image_count=listing.image_count or 0,
        has_asset_links=listing.has_asset_links or False,
        raw_payload=listing.raw_payload or {},
    )


def listing_query() -> Select[tuple[MartListing]]:
    return select(MartListing).order_by(desc(MartListing.last_scraped_at), desc(MartListing.id))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/listings", response_model=list[ListingListItem])
def get_listings(
    db: Session = Depends(get_db),
    city: str | None = Query(default=None),
    transaction_type: str | None = Query(default=None),
    property_type: str | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
) -> list[ListingListItem]:
    stmt = listing_query().limit(limit)
    if city:
        stmt = stmt.where(MartListing.city.ilike(city))
    if transaction_type:
        stmt = stmt.where(MartListing.transaction_type == transaction_type)
    if property_type:
        stmt = stmt.where(MartListing.property_type == property_type)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                MartListing.title.ilike(pattern),
                MartListing.neighborhood.ilike(pattern),
                MartListing.address.ilike(pattern),
                MartListing.description.ilike(pattern),
            )
        )

    rows = db.scalars(stmt).all()
    return [serialize_listing(listing) for listing in rows]


@app.get("/api/listings/{listing_id}", response_model=ListingDetail)
def get_listing(listing_id: int, db: Session = Depends(get_db)) -> ListingDetail:
    listing = db.scalar(listing_query().where(MartListing.id == listing_id))
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return serialize_listing(listing)


@app.get("/api/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)) -> SummaryResponse:
    latest_run = db.scalar(select(ScrapeRun).order_by(desc(ScrapeRun.started_at)).limit(1))
    listing_count = db.scalar(select(func.count()).select_from(MartListing)) or 0
    active_listing_count = (
        db.scalar(select(func.count()).select_from(MartListing).where(MartListing.is_active.is_(True))) or 0
    )
    source_count = db.scalar(select(func.count()).select_from(Source).where(Source.active.is_(True))) or 0
    return SummaryResponse(
        listing_count=listing_count,
        active_listing_count=active_listing_count,
        source_count=source_count,
        latest_scrape_started_at=latest_run.started_at if latest_run else None,
        latest_scrape_finished_at=latest_run.finished_at if latest_run else None,
        latest_scrape_status=latest_run.status if latest_run else None,
    )
