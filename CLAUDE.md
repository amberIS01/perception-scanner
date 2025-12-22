# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Perception Scanner is a full-stack application for aggregating and analyzing product reviews from multiple platforms (Google Play, iOS App Store, YouTube, Product Hunt, Reddit) with sentiment analysis.

## Development Commands

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate       # activate virtual environment
pip install -r requirements.txt  # install dependencies
uvicorn main:app --reload      # runs on http://localhost:8000
```

### Frontend (React + Vite)
```bash
cd frontend
npm install     # install dependencies
npm run dev     # runs on http://localhost:5173
npm run build   # build for production (runs tsc -b && vite build)
npm run preview # preview production build locally
npm run lint    # run eslint
```

### Running Both Servers
Open two terminal windows and run the backend and frontend commands above. The frontend makes direct API calls to the backend via CORS (configured in `backend/main.py`).

## Architecture

### Backend Structure
- `backend/main.py` - FastAPI application with endpoints for fetching and storing reviews
- `backend/config.py` - Configuration constants (DEFAULT_REVIEW_COUNT)
- `backend/database/` - SQLAlchemy models and database service
  - `models.py` - Product, Review, SentimentSnapshot tables
  - `service.py` - DatabaseService for CRUD operations
- `backend/services/` - Core business logic
  - `sentiment.py` - VADER-based sentiment analysis
  - `sources/` - Review source implementations

### Source Pattern
All review sources inherit from `BaseSource` (in `services/sources/base.py`):
- Must implement `async fetch_reviews(identifier: str, count: int) -> SourceResult`
- Returns `SourceResult` with platform, reviews list, average rating, and optional error
- Each `Review` has: id, user, comment, date, platform, with optional `rating` (null for comment-based sources) and `likes`

Current sources: GooglePlaySource, IOSAppStoreSource, YouTubeSource, ProductHuntSource, RedditSource

### Data Flow
1. Frontend sends `POST /api/reviews` with product name and source identifiers
2. Backend fetches reviews from each configured source in parallel
3. Sentiment analysis (VADER) runs on all reviews
4. Reviews and sentiment snapshots are stored in SQLite database
5. Combined sentiment across all sources is calculated and returned

### Frontend Structure
- React 19 with TypeScript, Vite, Tailwind CSS
- `frontend/src/App.tsx` - Main application with form inputs and results display
- `frontend/src/components/ui/` - shadcn/ui components
- `frontend/src/components/charts/` - Recharts-based sentiment visualizations

## API Endpoints

- `GET /api/health` - Health check with source availability status
- `POST /api/reviews` - Fetch reviews from configured sources (saves to DB)
- `GET /api/products/{product_name}/history` - Sentiment history over time
- `GET /api/products/{product_name}/reviews` - Stored reviews with optional platform filter

## Environment Setup

Copy `backend/.env.example` to `backend/.env` and configure:
- YouTube requires `YOUTUBE_API_KEY` (Google Cloud Console)
- Product Hunt requires `PRODUCT_HUNT_API_TOKEN`
- Google Play, iOS App Store, and Reddit work without API keys

## Adding a New Review Source

1. Create a new file in `backend/services/sources/` (e.g., `twitter.py`)
2. Inherit from `BaseSource` and implement `fetch_reviews()`
3. Set `platform_name` class attribute
4. Export the source class in `backend/services/sources/__init__.py`
5. Instantiate and wire it in `backend/main.py` (add to SourceConfig and POST /api/reviews)

## UI/UX Design Guidelines

Follow these principles when building dashboard and data visualization components:

### Core Principles

- **5-Second Rule**: User should understand the main message within 5 seconds
- **Max 2-3 visualizations per view**: Avoid chart clutter, don't overwhelm users
- **One story per visual**: Each chart should convey a single clear message
- **Progressive disclosure**: Hide detailed data behind expandable sections or tabs

### Data Visualization Best Practices

- Prefer bar charts over pie/donut charts for comparisons
- Avoid gauges and circular charts when possible
- Use micro-visualizations (sparklines, indicators) for compact data
- Hide granular data in hover tooltips, not on screen
- Remove data labels unless absolutely necessary

### Layout Guidelines

- Key metrics at top with strong visual weight
- Use whitespace to separate sections and reduce cognitive load
- Secondary data in tabs or expandable sections
- Consistent color coding: green (positive), gray (neutral), red (negative)

### Current Sentiment Display Strategy

- Hero metric: Overall sentiment label (Positive/Neutral/Negative) as headline
- Primary viz: Single stacked bar for distribution
- Details on demand: Keywords, platform comparison in expandable sections

## Git Commit Guidelines

- Keep commit messages short and simple
- Never include Claude Code attribution or co-author tags
- Format: `type: brief description` (e.g., `fix: clean up gitignore`, `feat: add youtube source`)

## Important Context (from Manager Code Review - Dec 19, 2025)

Read `others/transcripts/meeting-2025-12-19.txt` and `others/MEETING_SUMMARY.md` for full context.

### Key Rules from Manager

1. **No Dead Code**: Every line must be understood and used. No day-one tech debt.
2. **Understand Your Code**: Don't use AI-generated code you don't understand. Manager will hold YOU accountable, not your AI.
3. **Only Secrets in .env**: API keys/tokens only. Other config stays hardcoded in `config.py`.
4. **Review Process**: Self-review → Peer review (Aryan) → Manager review
5. **Documentation Must Match Code**: If docs say a field exists, it must actually be in the code.

### Code Review Fixes Applied (Dec 19, 2025)

1. **Fixed docs/** - Removed undocumented fields (`user_image`, `reply_content`, `app_version`, etc.) from all source documentation that weren't in the actual Review model
2. **Fixed others/notes/me.md** - Removed inaccurate field list
3. **Simplified config.py** - Removed Pydantic Settings, now just a simple constant `DEFAULT_REVIEW_COUNT = 100`
4. **Verified .env.example** - Contains only secrets (correct)

### Review Model (Actual Fields)

```python
class Review(BaseModel):
    id: str
    user: str
    rating: Optional[float] = None  # null for YouTube, Reddit, Product Hunt
    comment: str
    date: str
    platform: str
    likes: Optional[int] = None
```

### Project Context

- **Sahil**: Works on Perception Scanner (this project)
- **Aryan**: Works on AI Meeting Assistant (Cluely clone)
- **Manager**: Expects code quality, understanding, and peer reviews
- **Hosting**: Railway for now, AWS/GCP with Terraform later

### Files to Read for Context

- `others/MEETING_SUMMARY.md` - All meeting summaries consolidated
- `others/transcripts/` - Raw meeting transcripts
- `others/test-data/test_products.md` - Test identifiers for various apps
