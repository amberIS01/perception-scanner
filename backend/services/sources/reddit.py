# Reddit comments via public JSON API (no API key needed)
import requests
from datetime import datetime

from config import DEFAULT_REVIEW_COUNT
from .base import BaseSource, Review, SourceResult


class RedditSource(BaseSource):
    platform_name = "Reddit"

    def _fetch_json(self, url: str) -> dict:
        headers = {"User-Agent": "PerceptionScanner/1.0"}
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def _timestamp_to_date(self, timestamp) -> str:
        if not timestamp:
            return ""
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    async def fetch_reviews(self, identifier: str, count: int = DEFAULT_REVIEW_COUNT) -> SourceResult:
        try:
            if identifier.startswith("r/") or "/" in identifier:
                url = f"https://www.reddit.com/{identifier}.json?limit={count}"
            else:
                url = f"https://www.reddit.com/r/{identifier}/hot.json?limit=25"

            data = self._fetch_json(url)

            if isinstance(data, dict) and data.get("error"):
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=f"Reddit returned error: {data.get('message', 'Not found')}"
                )

            review_list = []

            if isinstance(data, list) and len(data) > 1:
                comments = data[1].get("data", {}).get("children", [])
                for item in comments[:count]:
                    if item.get("kind") != "t1":
                        continue
                    comment = item.get("data", {})
                    if not comment.get("body"):
                        continue
                    review = Review(
                        id=comment.get("id", ""),
                        user=comment.get("author", "Anonymous"),
                        rating=None,
                        comment=comment.get("body", ""),
                        date=self._timestamp_to_date(comment.get("created_utc")),
                        platform=self.platform_name,
                        likes=comment.get("score", 0)
                    )
                    review_list.append(review)
            else:
                posts = data.get("data", {}).get("children", [])

                if not posts:
                    return SourceResult(
                        platform=self.platform_name,
                        identifier=identifier,
                        average_rating=0.0,
                        total_reviews=0,
                        reviews=[],
                        error=f"Subreddit 'r/{identifier}' not found or empty"
                    )

                for post in posts[:10]:
                    post_data = post.get("data", {})
                    permalink = post_data.get("permalink", "")
                    if not permalink:
                        continue

                    try:
                        post_url = f"https://www.reddit.com{permalink}.json?limit=10"
                        post_json = self._fetch_json(post_url)

                        if isinstance(post_json, list) and len(post_json) > 1:
                            comments = post_json[1].get("data", {}).get("children", [])
                            for item in comments[:10]:
                                if item.get("kind") != "t1":
                                    continue
                                comment = item.get("data", {})
                                if not comment.get("body"):
                                    continue
                                review = Review(
                                    id=comment.get("id", ""),
                                    user=comment.get("author", "Anonymous"),
                                    rating=None,
                                    comment=comment.get("body", ""),
                                    date=self._timestamp_to_date(comment.get("created_utc")),
                                    platform=self.platform_name,
                                    likes=comment.get("score", 0)
                                )
                                review_list.append(review)

                                if len(review_list) >= count:
                                    break
                    except Exception:
                        continue

                    if len(review_list) >= count:
                        break

            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=len(review_list),
                reviews=review_list[:count]
            )

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"Subreddit or post '{identifier}' not found"
            elif e.response.status_code == 403:
                error_msg = "Subreddit is private or banned"
            elif e.response.status_code == 429:
                error_msg = "Rate limited. Try again later."
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
