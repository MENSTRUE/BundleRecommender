"""Typed response contracts shared with the frontend."""
from pydantic import BaseModel, Field

class RecommendRequest(BaseModel):
    items: list[str] = Field(min_length=1, max_length=20)
    dataset: str = Field(default="instacart", pattern="^(instacart|uci)$")
    limit: int = Field(default=8, ge=1, le=20)

class Suggestion(BaseModel):
    product: str
    score: float | None = None
    support: float | None = None
    confidence: float | None = None
    lift: float | None = None
    matched_input: list[str]
    source: str

class RecommendResponse(BaseModel):
    dataset: str
    items: list[str]
    suggestions: list[Suggestion]
    matched_rules: int
    scanned_rules: int
    disclaimer: str
