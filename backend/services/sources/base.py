# Base classes for all review sources
from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel

from config import DEFAULT_REVIEW_COUNT


# Standard review format - all sources return this
class Review(BaseModel):
    id: str
    user: str
    rating: Optional[float] = None
    comment: str
    date: str
    platform: str
    likes: Optional[int] = None


# What fetch_reviews() returns
class SourceResult(BaseModel):
    platform: str
    identifier: str
    average_rating: float
    total_reviews: int
    reviews: List[Review]
    error: Optional[str] = None


# Abstract class - all sources inherit from this
class BaseSource(ABC):
    platform_name: str = "Unknown"

    @abstractmethod
    async def fetch_reviews(self, identifier: str, count: int = DEFAULT_REVIEW_COUNT) -> SourceResult:
        """Fetch reviews from the source platform."""
        pass

    def calculate_average_rating(self, reviews: List[Review]) -> float:
        """Calculate average rating from a list of reviews."""
        ratings = [r.rating for r in reviews if r.rating is not None]
        if not ratings:
            return 0.0
        return round(sum(ratings) / len(ratings), 2)
