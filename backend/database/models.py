# SQLite database models for storing reviews and sentiment
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///./perception_scanner.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Product being scanned (e.g., Notion, WhatsApp)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    google_play_id = Column(String(255), nullable=True)
    ios_app_id = Column(String(255), nullable=True)
    youtube_video_id = Column(String(255), nullable=True)
    product_hunt_slug = Column(String(255), nullable=True)
    reddit_subreddit = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    sentiment_snapshots = relationship("SentimentSnapshot", back_populates="product", cascade="all, delete-orphan")


# Individual review from any platform
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    external_id = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    user = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    comment = Column(Text, nullable=True)
    review_date = Column(String(50), nullable=True)
    likes = Column(Integer, default=0)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String(20), nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")


# Aggregated sentiment at a point in time (for history tracking)
class SentimentSnapshot(Base):
    __tablename__ = "sentiment_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50), nullable=True)  # NULL means combined
    overall_sentiment = Column(String(20), nullable=False)
    average_score = Column(Float, nullable=False)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    keywords = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sentiment_snapshots")


def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
