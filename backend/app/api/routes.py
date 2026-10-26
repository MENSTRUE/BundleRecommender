"""BundleRecommender HTTP endpoints. Rule identifiers remain unchanged."""
from fastapi import APIRouter, HTTPException, Query

from app.schemas.recommendation import RecommendRequest, RecommendResponse
from app.services.product_names import product_metadata
from app.services.rules import DATASETS, catalog, recommend, status

router = APIRouter(prefix="/api/v1")


def handle_error(exc: Exception) -> None:
    code = 503 if isinstance(exc, (FileNotFoundError, OSError)) else 422
    raise HTTPException(status_code=code, detail=str(exc)) from exc


def validate_dataset(dataset: str) -> None:
    if dataset not in DATASETS:
        raise HTTPException(status_code=422, detail="dataset must be instacart or uci")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "datasets": status(), "research_only": True}


@router.get("/catalog")
def get_catalog(dataset: str = Query(default="instacart")) -> dict:
    validate_dataset(dataset)
    try:
        products = catalog(dataset)
    except (ValueError, FileNotFoundError, OSError) as exc:
        handle_error(exc)
    return {"dataset": dataset, "products": products, "count": len(products)}


@router.get("/catalog/details")
def get_catalog_details(dataset: str = Query(default="instacart")) -> dict:
    """Supplementary display-only data; /catalog remains backward compatible."""
    validate_dataset(dataset)
    try:
        product_ids = catalog(dataset)
        products = product_metadata(dataset, product_ids)
    except (ValueError, FileNotFoundError, OSError) as exc:
        handle_error(exc)
    return {
        "dataset": dataset,
        "products": products,
        "count": len(products),
        "named_count": sum(bool(item["has_description"]) for item in products),
    }


@router.post("/recommend", response_model=RecommendResponse)
def get_recommendations(payload: RecommendRequest) -> dict:
    try:
        return recommend(payload.dataset, payload.items, payload.limit)
    except (ValueError, FileNotFoundError, OSError) as exc:
        handle_error(exc)
