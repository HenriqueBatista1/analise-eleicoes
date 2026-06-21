from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import CandidateCatalog, PolymarketProbability
from app.schemas.market_expectation_filters import (
    MarketExpectationDateRange,
    MarketExpectationFilterCandidate,
    MarketExpectationFiltersResponse,
)
from app.services.market_expectations import SUPPORTED_MARKET_EXPECTATION_INTERVALS


def get_market_expectation_filters(db: Session) -> MarketExpectationFiltersResponse:
    min_timestamp, max_timestamp = _get_market_expectation_date_range(db)

    return MarketExpectationFiltersResponse(
        date_range=MarketExpectationDateRange(
            min=min_timestamp,
            max=max_timestamp,
        ),
        intervals=list(SUPPORTED_MARKET_EXPECTATION_INTERVALS),
        candidates=_get_market_expectation_candidates(db),
    )


def _get_market_expectation_date_range(db: Session):
    return (
        db.query(
            func.min(PolymarketProbability.timestamp),
            func.max(PolymarketProbability.timestamp),
        )
        .one()
    )


def _get_market_expectation_candidates(
    db: Session,
) -> list[MarketExpectationFilterCandidate]:
    candidates = (
        db.query(
            CandidateCatalog.id,
            CandidateCatalog.display_name,
        )
        .join(
            PolymarketProbability,
            PolymarketProbability.candidate_catalog_id == CandidateCatalog.id,
        )
        .distinct()
        .all()
    )

    return [
        MarketExpectationFilterCandidate(
            candidate_catalog_id=candidate.id,
            display_name=candidate.display_name,
        )
        for candidate in candidates
    ]
