# Perception Scanner

Aggregate and analyze product reviews from multiple platforms with sentiment analysis.

## Features

- Fetch reviews from Google Play, iOS App Store, YouTube, Product Hunt, and Reddit
- VADER-based sentiment analysis with keyword extraction
- SQLite database for storing reviews and sentiment history
- React dashboard with data visualization

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Add your API keys (optional)
uvicorn main:app --reload
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## API Keys (Optional)

Only required if you want to use these sources:

- **YouTube**: Get key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (enable YouTube Data API v3)
- **Product Hunt**: Get token from [Product Hunt API](https://api.producthunt.com/v2/docs)

Google Play, iOS App Store, and Reddit work without API keys.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check with source availability |
| POST | `/api/reviews` | Fetch reviews from configured sources |
| GET | `/api/products/{name}/history` | Sentiment history over time |
| GET | `/api/products/{name}/reviews` | Stored reviews with optional platform filter |

## Tech Stack

**Backend**: FastAPI, SQLAlchemy, VADER Sentiment, google-play-scraper, app-store-web-scraper

**Frontend**: React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui, Recharts
