from backend.models.search import (
    SearchResponse,
    SearchResult,
)

from backend.models.school import (
    Address,
    School,
    SchoolRecommendation,
)

from backend.models.scholarship import (
    Scholarship,
    ScholarshipRecommendation,
)

from backend.models.legal import (
    LegalResource,
    LegalRecommendation,
)
from backend.models.counselling import CounsellingResponse

__all__ = (
    "SearchResult",
    "SearchResponse",

    "Address",
    "School",
    "SchoolRecommendation",

    "Scholarship",
    "ScholarshipRecommendation",

    "LegalResource",
    "LegalRecommendation",

    "Document",
    "DocumentChecklist",

    "Housing",
    "HousingRecommendation",

    "CounsellingResponse",
)
from backend.models.document import (
    Document,
    DocumentChecklist,
)

from backend.models.housing import (
    Housing,
    HousingRecommendation,
)