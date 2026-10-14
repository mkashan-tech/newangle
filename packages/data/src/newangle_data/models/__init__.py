"""NewAngle Phase 1 data model.

Importing this package registers every ORM model with SQLAlchemy's
declarative mapper configuration, which is required for the string-based
relationship references used across model modules (e.g.
`relationship("Company")`) to resolve correctly, and for
`Base.metadata.create_all()` / Alembic autogenerate to see every table.
"""

from newangle_data.models.base import Base
from newangle_data.models.company import Company
from newangle_data.models.enums import Exchange, PromoterHoldingObservationType, SourceType
from newangle_data.models.events import CorporateEvent
from newangle_data.models.promoter_holdings import PromoterHoldingObservation
from newangle_data.models.security import ListedSecurity
from newangle_data.models.source import Source

__all__ = [
    "Base",
    "Company",
    "ListedSecurity",
    "Source",
    "CorporateEvent",
    "PromoterHoldingObservation",
    "Exchange",
    "SourceType",
    "PromoterHoldingObservationType",
]
