from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class Review(BaseModel):
    id: str
    user: str
    rating: Optional[float] = None
    comment: str
    date: str
    platform: str
    likes: Optional[int] = None
    user_image: Optional[str] = None
    title: Optional[str] = None
    app_version: Optional[str] = None
    url: Optional[str] = None


class SourceResult(BaseModel):
    platform: str
    identifier: str
    average_rating: float
    total_reviews: int
    reviews: List[Review]
    error: Optional[str] = None


class BaseSource(ABC):
    platform_name: str = "Unknown"

    @abstractmethod
    async def fetch_reviews(self, identifier: str, count: int = 100) -> SourceResult:
        """Fetch reviews from the source platform."""
        pass

    def calculate_average_rating(self, reviews: List[Review]) -> float:
        """Calculate average rating from a list of reviews."""
        ratings = [r.rating for r in reviews if r.rating is not None]
        if not ratings:
            return 0.0
        return round(sum(ratings) / len(ratings), 2)
