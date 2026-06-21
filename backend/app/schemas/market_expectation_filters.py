from datetime import datetime

from pydantic import Field

from app.schemas.market_expectations import ApiModel, MarketExpectationInterval


class MarketExpectationDateRange(ApiModel):
    min: datetime | None
    max: datetime | None


class MarketExpectationFilterCandidate(ApiModel):
    candidate_catalog_id: int = Field(alias="candidateCatalogId")
    display_name: str = Field(alias="displayName")


class MarketExpectationFiltersResponse(ApiModel):
    date_range: MarketExpectationDateRange = Field(alias="dateRange")
    intervals: list[MarketExpectationInterval]
    candidates: list[MarketExpectationFilterCandidate]
