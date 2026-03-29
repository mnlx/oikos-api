from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ListingListItem(BaseModel):
    id: int
    title: str
    canonical_url: str
    transaction_type: str
    property_type: str
    city: str
    state: str
    neighborhood: str | None
    address: str | None
    latitude: float | None
    longitude: float | None
    price_sale: float | None
    price_rent: float | None
    bedrooms: int | None
    bathrooms: int | None
    parking_spaces: int | None
    area_m2: float | None
    broker_name: str | None
    last_scraped_at: datetime
    source_code: str
    source_name: str
    image_count: int
    has_asset_links: bool
    raw_payload: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class ListingDetail(ListingListItem):
    description: str | None
    condo_fee: float | None
    iptu: float | None
    published_at: datetime | None
    first_seen_at: datetime
    last_seen_at: datetime
    is_active: bool
    image_uris: list[str]
