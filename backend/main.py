from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from config import settings
from database import init_db, get_db, DatabaseService
from services.sources import (
    GooglePlaySource,
    IOSAppStoreSource,
    YouTubeSource,
    ProductHuntSource,
    RedditSource
)
from services.sentiment import sentiment_analyzer

# Initialize database
init_db()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# Initialize sources
google_play_source = GooglePlaySource()
ios_app_store_source = IOSAppStoreSource()
youtube_source = YouTubeSource()
product_hunt_source = ProductHuntSource()
reddit_source = RedditSource()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SourceConfig(BaseModel):
    youtube_video: Optional[str] = None
    product_hunt_product: Optional[str] = None
    google_play_app: Optional[str] = None
    ios_app: Optional[str] = None
    reddit_subreddit: Optional[str] = None


class ProductReviewRequest(BaseModel):
    product_name: str
    sources: SourceConfig


def process_source_result(source_result) -> dict:
    """Process source result and add sentiment analysis."""
    reviews = [r.model_dump() for r in source_result.reviews]
    sentiment = sentiment_analyzer.analyze_reviews(reviews)

    return {
        "platform": source_result.platform,
        "identifier": source_result.identifier,
        "average_rating": source_result.average_rating,
        "total_reviews": source_result.total_reviews,
        "reviews": reviews,
        "error": source_result.error,
        "sentiment": {
            "overall": sentiment["overall"],
            "breakdown": sentiment["breakdown"],
            "average_score": sentiment["average_score"],
            "keywords": sentiment["keywords"][:10]
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "sources": {
            "google_play": {"available": True, "requires_key": False},
            "ios_app_store": {"available": True, "requires_key": False},
            "youtube": {
                "available": settings.youtube_api_key is not None,
                "requires_key": True
            },
            "product_hunt": {
                "available": settings.product_hunt_api_token is not None,
                "requires_key": True
            },
            "reddit": {"available": True, "requires_key": False},
        }
    }


@app.post("/api/reviews")
async def get_reviews(request: ProductReviewRequest, db: Session = Depends(get_db)):
    """Fetch reviews from configured sources and store in database."""
    db_service = DatabaseService(db)

    # Get or create product
    product = db_service.get_or_create_product(
        name=request.product_name,
        google_play_id=request.sources.google_play_app,
        ios_app_id=request.sources.ios_app,
        youtube_video_id=request.sources.youtube_video,
        product_hunt_slug=request.sources.product_hunt_product,
        reddit_subreddit=request.sources.reddit_subreddit
    )

    result = {
        "product_name": request.product_name,
        "product_id": product.id,
        "sources": [],
        "combined_sentiment": None,
        "errors": []
    }

    all_reviews = []
    count = settings.default_review_count

    # Google Play Store
    if request.sources.google_play_app:
        gplay_result = await google_play_source.fetch_reviews(
            request.sources.google_play_app,
            count=count
        )
        processed = process_source_result(gplay_result)
        result["sources"].append(processed)

        if processed["error"]:
            result["errors"].append({
                "platform": "Google Play Store",
                "error": processed["error"]
            })
        else:
            all_reviews.extend(processed["reviews"])
            # Save to database
            db_service.save_reviews(product.id, "Google Play Store", processed["reviews"])
            db_service.save_sentiment_snapshot(product.id, "Google Play Store", processed["sentiment"])

    # iOS App Store
    if request.sources.ios_app:
        ios_result = await ios_app_store_source.fetch_reviews(
            request.sources.ios_app,
            count=count
        )
        processed = process_source_result(ios_result)
        result["sources"].append(processed)

        if processed["error"]:
            result["errors"].append({
                "platform": "iOS App Store",
                "error": processed["error"]
            })
        else:
            all_reviews.extend(processed["reviews"])
            db_service.save_reviews(product.id, "iOS App Store", processed["reviews"])
            db_service.save_sentiment_snapshot(product.id, "iOS App Store", processed["sentiment"])

    # YouTube
    if request.sources.youtube_video:
        yt_result = await youtube_source.fetch_reviews(
            request.sources.youtube_video,
            count=count
        )
        processed = process_source_result(yt_result)
        result["sources"].append(processed)

        if processed["error"]:
            result["errors"].append({
                "platform": "YouTube",
                "error": processed["error"]
            })
        else:
            all_reviews.extend(processed["reviews"])
            db_service.save_reviews(product.id, "YouTube", processed["reviews"])
            db_service.save_sentiment_snapshot(product.id, "YouTube", processed["sentiment"])

    # Product Hunt
    if request.sources.product_hunt_product:
        ph_result = await product_hunt_source.fetch_reviews(
            request.sources.product_hunt_product,
            count=count
        )
        processed = process_source_result(ph_result)
        result["sources"].append(processed)

        if processed["error"]:
            result["errors"].append({
                "platform": "Product Hunt",
                "error": processed["error"]
            })
        else:
            all_reviews.extend(processed["reviews"])
            db_service.save_reviews(product.id, "Product Hunt", processed["reviews"])
            db_service.save_sentiment_snapshot(product.id, "Product Hunt", processed["sentiment"])

    # Reddit
    if request.sources.reddit_subreddit:
        reddit_result = await reddit_source.fetch_reviews(
            request.sources.reddit_subreddit,
            count=count
        )
        processed = process_source_result(reddit_result)
        result["sources"].append(processed)

        if processed["error"]:
            result["errors"].append({
                "platform": "Reddit",
                "error": processed["error"]
            })
        else:
            all_reviews.extend(processed["reviews"])
            db_service.save_reviews(product.id, "Reddit", processed["reviews"])
            db_service.save_sentiment_snapshot(product.id, "Reddit", processed["sentiment"])

    # Combined sentiment analysis
    if all_reviews:
        combined = sentiment_analyzer.analyze_reviews(all_reviews)
        result["combined_sentiment"] = {
            "overall": combined["overall"],
            "breakdown": combined["breakdown"],
            "average_score": combined["average_score"],
            "keywords": combined["keywords"][:20]
        }
        # Save combined sentiment snapshot
        db_service.save_sentiment_snapshot(product.id, None, combined)

    return result


@app.get("/api/products/{product_name}/history")
async def get_product_history(product_name: str, days: int = 30, db: Session = Depends(get_db)):
    """Get sentiment history for a product."""
    db_service = DatabaseService(db)
    product = db_service.get_product_by_name(product_name)

    if not product:
        return {"error": f"Product '{product_name}' not found"}

    history = db_service.get_sentiment_history(product.id, days=days)

    return {
        "product_name": product_name,
        "history": [
            {
                "platform": s.platform or "Combined",
                "overall": s.overall_sentiment,
                "average_score": s.average_score,
                "breakdown": {
                    "positive": s.positive_count,
                    "negative": s.negative_count,
                    "neutral": s.neutral_count
                },
                "total_reviews": s.total_reviews,
                "timestamp": s.created_at.isoformat()
            }
            for s in history
        ]
    }


@app.get("/api/products/{product_name}/reviews")
async def get_stored_reviews(
    product_name: str,
    platform: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get stored reviews for a product."""
    db_service = DatabaseService(db)
    product = db_service.get_product_by_name(product_name)

    if not product:
        return {"error": f"Product '{product_name}' not found"}

    reviews = db_service.get_reviews(product.id, platform=platform, limit=limit)

    return {
        "product_name": product_name,
        "total": len(reviews),
        "reviews": [
            {
                "id": r.external_id,
                "platform": r.platform,
                "user": r.user,
                "rating": r.rating,
                "comment": r.comment,
                "date": r.review_date,
                "sentiment_score": r.sentiment_score,
                "sentiment_label": r.sentiment_label
            }
            for r in reviews
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
