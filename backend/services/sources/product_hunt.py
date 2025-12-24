# Product Hunt reviews via GraphQL API (requires PRODUCT_HUNT_API_TOKEN)
# Note: API exposes comments + aggregate reviewsRating, not individual review ratings
import os
import requests

from config import DEFAULT_REVIEW_COUNT
from .base import BaseSource, Review, SourceResult


class ProductHuntSource(BaseSource):
    platform_name = "Product Hunt"
    api_url = "https://api.producthunt.com/v2/api/graphql"

    def _make_request(self, query: str) -> dict:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('PRODUCT_HUNT_API_TOKEN')}",
        }
        response = requests.post(
            self.api_url,
            headers=headers,
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    async def fetch_reviews(self, identifier: str, count: int = DEFAULT_REVIEW_COUNT) -> SourceResult:
        if not os.getenv("PRODUCT_HUNT_API_TOKEN"):
            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=0,
                reviews=[],
                error="PRODUCT_HUNT_API_TOKEN not configured. Get one from https://api.producthunt.com/v2/docs"
            )

        try:
            query = f"""
            query {{
                post(slug: "{identifier}") {{
                    id
                    name
                    tagline
                    votesCount
                    commentsCount
                    reviewsRating
                    comments(first: {min(count, 100)}) {{
                        edges {{
                            node {{
                                id
                                body
                                createdAt
                                votesCount
                                user {{
                                    name
                                    username
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            """

            data = self._make_request(query)

            if "errors" in data:
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=data["errors"][0].get("message", "Unknown error")
                )

            post = data.get("data", {}).get("post")
            if not post:
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=f"Product '{identifier}' not found on Product Hunt"
                )

            review_list = []
            comments_data = post.get("comments", {}).get("edges", [])

            # Get aggregate rating (not all products have ratings)
            reviews_rating = post.get("reviewsRating") or 0.0

            for edge in comments_data:
                node = edge.get("node", {})
                user = node.get("user", {})
                review = Review(
                    id=node.get("id", ""),
                    user=user.get("name") or user.get("username") or "Anonymous",
                    rating=None,  # Individual comments don't have ratings in PH API
                    comment=node.get("body", ""),
                    date=node.get("createdAt", "")[:10] if node.get("createdAt") else "",
                    platform=self.platform_name,
                    likes=node.get("votesCount", 0)
                )
                review_list.append(review)

            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=reviews_rating,
                total_reviews=post.get("commentsCount", len(review_list)),
                reviews=review_list
            )

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = "Invalid or expired API token"
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Try again later."
            else:
                error_msg = str(e)
            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=0,
                reviews=[],
                error=error_msg
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
