# Google Play Store reviews via google-play-scraper (no API key needed)
from google_play_scraper import reviews, Sort
from google_play_scraper.exceptions import NotFoundError
from .base import BaseSource, Review, SourceResult


class GooglePlaySource(BaseSource):
    platform_name = "Google Play Store"

    async def fetch_reviews(self, identifier: str, count: int = 100) -> SourceResult:
        try:
            result, _ = reviews(
                identifier,
                lang="en",
                country="us",
                sort=Sort.NEWEST,
                count=count
            )

            if not result:
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=None
                )

            review_list = []

            for r in result:
                review = Review(
                    id=r.get("reviewId", ""),
                    user=r.get("userName", "Anonymous"),
                    rating=float(r.get("score", 0)),
                    comment=r.get("content", ""),
                    date=str(r.get("at", ""))[:10] if r.get("at") else "",
                    platform=self.platform_name,
                    likes=r.get("thumbsUpCount", 0)
                )
                review_list.append(review)

            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=self.calculate_average_rating(review_list),
                total_reviews=len(review_list),
                reviews=review_list
            )

        except NotFoundError:
            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=0,
                reviews=[],
                error=f"App '{identifier}' not found on Google Play Store"
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
