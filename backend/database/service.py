from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .models import Product, Review, SentimentSnapshot
from services.sentiment import sentiment_analyzer


class DatabaseService:
    def __init__(self, db: Session):
        self.db = db

    # Product operations
    def get_or_create_product(
        self,
        name: str,
        google_play_id: Optional[str] = None,
        ios_app_id: Optional[str] = None,
        youtube_video_id: Optional[str] = None,
        product_hunt_slug: Optional[str] = None,
        reddit_subreddit: Optional[str] = None
    ) -> Product:
        """Get existing product or create a new one."""
        product = self.db.query(Product).filter(Product.name == name).first()

        if not product:
            product = Product(
                name=name,
                google_play_id=google_play_id,
                ios_app_id=ios_app_id,
                youtube_video_id=youtube_video_id,
                product_hunt_slug=product_hunt_slug,
                reddit_subreddit=reddit_subreddit
            )
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
        else:
            # Update source IDs if provided
            updated = False
            if google_play_id and not product.google_play_id:
                product.google_play_id = google_play_id
                updated = True
            if ios_app_id and not product.ios_app_id:
                product.ios_app_id = ios_app_id
                updated = True
            if youtube_video_id and not product.youtube_video_id:
                product.youtube_video_id = youtube_video_id
                updated = True
            if product_hunt_slug and not product.product_hunt_slug:
                product.product_hunt_slug = product_hunt_slug
                updated = True
            if reddit_subreddit and not product.reddit_subreddit:
                product.reddit_subreddit = reddit_subreddit
                updated = True

            if updated:
                product.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(product)

        return product

    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        return self.db.query(Product).filter(Product.name == name).first()

    # Review operations
    def save_reviews(
        self,
        product_id: int,
        platform: str,
        reviews_data: List[Dict[str, Any]]
    ) -> List[Review]:
        """Save reviews to database, avoiding duplicates."""
        saved_reviews = []

        for r in reviews_data:
            external_id = str(r.get("id", ""))

            # Check if review already exists
            existing = self.db.query(Review).filter(
                and_(
                    Review.product_id == product_id,
                    Review.external_id == external_id,
                    Review.platform == platform
                )
            ).first()

            if existing:
                continue

            # Analyze sentiment
            comment = r.get("comment", "")
            sentiment = sentiment_analyzer.analyze_text(comment)

            review = Review(
                product_id=product_id,
                external_id=external_id,
                platform=platform,
                user=r.get("user", "Anonymous"),
                user_image=r.get("user_image"),
                rating=r.get("rating"),
                comment=comment,
                title=r.get("title"),
                review_date=r.get("date", ""),
                likes=r.get("likes", 0),
                app_version=r.get("app_version"),
                url=r.get("url"),
                sentiment_score=sentiment["compound"],
                sentiment_label=sentiment_analyzer.get_sentiment_label(sentiment["compound"])
            )
            self.db.add(review)
            saved_reviews.append(review)

        if saved_reviews:
            self.db.commit()

        return saved_reviews

    def get_reviews(
        self,
        product_id: int,
        platform: Optional[str] = None,
        limit: int = 100
    ) -> List[Review]:
        """Get reviews for a product."""
        query = self.db.query(Review).filter(Review.product_id == product_id)

        if platform:
            query = query.filter(Review.platform == platform)

        return query.order_by(Review.fetched_at.desc()).limit(limit).all()

    def get_cached_reviews(
        self,
        product_id: int,
        platform: str,
        max_age_hours: int = 24
    ) -> Optional[List[Review]]:
        """Get cached reviews if they're recent enough."""
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)

        reviews = self.db.query(Review).filter(
            and_(
                Review.product_id == product_id,
                Review.platform == platform,
                Review.fetched_at >= cutoff
            )
        ).all()

        return reviews if reviews else None

    # Sentiment snapshot operations
    def save_sentiment_snapshot(
        self,
        product_id: int,
        platform: Optional[str],
        sentiment_data: Dict[str, Any]
    ) -> SentimentSnapshot:
        """Save a sentiment analysis snapshot."""
        snapshot = SentimentSnapshot(
            product_id=product_id,
            platform=platform,
            overall_sentiment=sentiment_data.get("overall", "neutral"),
            average_score=sentiment_data.get("average_score", 0.0),
            positive_count=sentiment_data.get("breakdown", {}).get("positive", 0),
            negative_count=sentiment_data.get("breakdown", {}).get("negative", 0),
            neutral_count=sentiment_data.get("breakdown", {}).get("neutral", 0),
            total_reviews=sum(sentiment_data.get("breakdown", {}).values()),
            keywords=sentiment_data.get("keywords", [])
        )
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot

    def get_sentiment_history(
        self,
        product_id: int,
        platform: Optional[str] = None,
        days: int = 30
    ) -> List[SentimentSnapshot]:
        """Get sentiment history for a product."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        query = self.db.query(SentimentSnapshot).filter(
            and_(
                SentimentSnapshot.product_id == product_id,
                SentimentSnapshot.created_at >= cutoff
            )
        )

        if platform is not None:
            query = query.filter(SentimentSnapshot.platform == platform)

        return query.order_by(SentimentSnapshot.created_at.desc()).all()

    def get_latest_sentiment(
        self,
        product_id: int,
        platform: Optional[str] = None
    ) -> Optional[SentimentSnapshot]:
        """Get the latest sentiment snapshot."""
        query = self.db.query(SentimentSnapshot).filter(
            SentimentSnapshot.product_id == product_id
        )

        if platform is not None:
            query = query.filter(SentimentSnapshot.platform == platform)

        return query.order_by(SentimentSnapshot.created_at.desc()).first()
