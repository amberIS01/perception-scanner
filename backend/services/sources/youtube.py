# YouTube comments via official API (requires YOUTUBE_API_KEY)
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import DEFAULT_REVIEW_COUNT
from .base import BaseSource, Review, SourceResult


class YouTubeSource(BaseSource):
    platform_name = "YouTube"

    def _get_youtube_client(self):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return None
        return build("youtube", "v3", developerKey=api_key)

    async def fetch_reviews(self, identifier: str, count: int = DEFAULT_REVIEW_COUNT) -> SourceResult:
        if not os.getenv("YOUTUBE_API_KEY"):
            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=0,
                reviews=[],
                error="YOUTUBE_API_KEY not configured. Get one from https://console.cloud.google.com/apis/library/youtube.googleapis.com"
            )

        try:
            youtube = self._get_youtube_client()

            video_response = youtube.videos().list(
                part="snippet",
                id=identifier
            ).execute()

            if not video_response.get("items"):
                return SourceResult(
                    platform=self.platform_name,
                    identifier=identifier,
                    average_rating=0.0,
                    total_reviews=0,
                    reviews=[],
                    error=f"Video '{identifier}' not found on YouTube"
                )

            review_list = []
            next_page_token = None

            while len(review_list) < count:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=identifier,
                    maxResults=min(100, count - len(review_list)),
                    pageToken=next_page_token,
                    textFormat="plainText",
                    order="time"  # Newest comments first
                ).execute()

                for item in response.get("items", []):
                    snippet = item["snippet"]["topLevelComment"]["snippet"]
                    review = Review(
                        id=item["id"],
                        user=snippet.get("authorDisplayName", "Anonymous"),
                        rating=None,
                        comment=snippet.get("textDisplay", ""),
                        date=snippet.get("publishedAt", "")[:10],
                        platform=self.platform_name,
                        likes=snippet.get("likeCount", 0)
                    )
                    review_list.append(review)

                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break

            return SourceResult(
                platform=self.platform_name,
                identifier=identifier,
                average_rating=0.0,
                total_reviews=len(review_list),
                reviews=review_list
            )

        except HttpError as e:
            error_msg = str(e)
            if "commentsDisabled" in error_msg:
                error_msg = "Comments are disabled for this video"
            elif "quotaExceeded" in error_msg:
                error_msg = "YouTube API quota exceeded. Try again tomorrow."
            elif "videoNotFound" in error_msg:
                error_msg = f"Video '{identifier}' not found on YouTube"
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
