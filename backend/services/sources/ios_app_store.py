# iOS App Store reviews via RSS feed scraper (no API key needed)
import requests
from app_store_web_scraper import AppStoreEntry

from config import DEFAULT_REVIEW_COUNT
from .base import BaseSource, Review, SourceResult


class IOSAppStoreSource(BaseSource):
    platform_name = "iOS App Store"

    def _validate_app(self, app_id: str) -> bool:
        try:
            response = requests.get(
                f"https://itunes.apple.com/lookup?id={app_id}",
                timeout=30
            )
            data = response.json()
            return data.get("resultCount", 0) > 0
        except Exception:
            return False

    async def fetch_reviews(self, identifier: str, count: int = DEFAULT_REVIEW_COUNT) -> SourceResult:
        try:
            if not self._validate_app(identifier):
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=f"App with ID '{identifier}' not found on iOS App Store"
                )

            app = AppStoreEntry(
                app_id=int(identifier),
                country="us"
            )
            raw_reviews = list(app.reviews(limit=count))

            review_list = [
                Review(
                    id=str(r.id),
                    user=r.user_name or 'Anonymous',
                    rating=float(r.rating),
                    comment=f"{r.title}: {r.content}" if r.title else r.content,
                    date=r.date.strftime('%Y-%m-%d') if r.date else '',
                    platform=self.platform_name
                )
                for r in raw_reviews
            ]

            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=self.calculate_average_rating(review_list),
                total_reviews=len(review_list),
                reviews=review_list
            )

        except Exception as e:
            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=0,
                reviews=[],
                error=str(e)
            )
