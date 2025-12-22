# Backend Code Comments Tracking

All comments added to explain what the code does.

## main.py
| Line | Comment |
|------|---------|
| 1 | `# FastAPI backend for Perception Scanner` |
| 32 | `# Allow frontend to call API (CORS)` |
| 42 | `# Request body: which platform identifiers to scan` |

## database/models.py
| Line | Comment |
|------|---------|
| 1 | `# SQLite database models for storing reviews and sentiment` |
| 12 | `# Product being scanned (e.g., Notion, WhatsApp)` |
| 30 | `# Individual review from any platform` |
| 50 | `# Aggregated sentiment at a point in time (for history tracking)` |

## database/service.py
| Line | Comment |
|------|---------|
| 1 | `# Database CRUD operations for products, reviews, and sentiment` |

## services/sentiment.py
| Line | Comment |
|------|---------|
| 1 | `# Sentiment analysis using VADER (works well for social media text)` |
| 81 | `# Main method - analyzes list of reviews and returns overall sentiment` |
| 140 | `# Singleton instance used by main.py and service.py` |

## services/sources/base.py
| Line | Comment |
|------|---------|
| 1 | `# Base classes for all review sources` |
| 7 | `# Standard review format - all sources return this` |
| 18 | `# What fetch_reviews() returns` |
| 28 | `# Abstract class - all sources inherit from this` |

## services/sources/google_play.py
| Line | Comment |
|------|---------|
| 1 | `# Google Play Store reviews via google-play-scraper (no API key needed)` |

## services/sources/ios_app_store.py
| Line | Comment |
|------|---------|
| 1 | `# iOS App Store reviews via RSS feed scraper (no API key needed)` |

## services/sources/youtube.py
| Line | Comment |
|------|---------|
| 1 | `# YouTube comments via official API (requires YOUTUBE_API_KEY)` |

## services/sources/product_hunt.py
| Line | Comment |
|------|---------|
| 1 | `# Product Hunt comments via GraphQL API (requires PRODUCT_HUNT_API_TOKEN)` |

## services/sources/reddit.py
| Line | Comment |
|------|---------|
| 1 | `# Reddit comments via public JSON API (no API key needed)` |

---

**Total: 18 backend comments added**
