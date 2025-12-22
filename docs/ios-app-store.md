# iOS App Store Source

## Overview

| Property         | Value                      |
| ---------------- | -------------------------- |
| Platform         | iOS App Store              |
| Method           | Web Scraping (RSS Feed)    |
| API Key Required | No                         |
| Max Reviews      | ~500 per request           |
| Rate Limits      | Unofficial (be respectful) |

## How It Works

This source uses the `app-store-web-scraper` library, which fetches reviews from Apple's public RSS feeds and web pages. No API key is required.

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install app-store-web-scraper
```

### Step 2: No API Key Needed

iOS App Store scraping doesn't require any API key or authentication.

### Step 3: Find Your App Identifier

1. Go to [Apple App Store](https://apps.apple.com)
2. Search for your app
3. Open the app page
4. Copy the numeric ID from the URL

**Example:**

```
URL: https://apps.apple.com/app/notion-notes-docs-tasks/id1232780281
Identifier: 1232780281
```

**Note:** The identifier is the numeric ID only (e.g., `1232780281`), not the full path.

## Configuration

Environment variables in `.env`:

```bash
# Country code for reviews (ISO 3166-1 alpha-2)
IOS_APP_STORE_COUNTRY=us
```

## Usage Example

```python
from services.sources import IOSAppStoreSource

source = IOSAppStoreSource()
result = await source.fetch_reviews("1232780281", count=100)

print(f"Reviews: {result.total_reviews}")
print(f"Average Rating: {result.average_rating}")
```

## Rate Limits

Since this uses web scraping (not an official API):

- No official rate limits
- Apple's RSS feeds are public but rate-limited
- Recommended: Max 1 request per second
- Too many requests may result in temporary blocks

## Limitations

1. **RSS Feed Limit**: Apple's RSS feed only returns the ~500 most recent reviews
2. **No Historical Data**: Cannot fetch all historical reviews
3. **Country-Specific**: Reviews are filtered by country code
4. **No Official API**: Apple doesn't provide a public API for App Store reviews
5. **Scraping Risks**: Apple may change their feed structure

## Data Retrieved

| Field   | Description                              |
| ------- | ---------------------------------------- |
| id      | Unique review ID                         |
| user    | Reviewer's display name                  |
| rating  | Star rating (1-5)                        |
| comment | Review title + content combined          |
| date    | Review date (YYYY-MM-DD)                 |
| likes   | Always null (not available from source) |

## Terms & Conditions

- **Apple Developer Agreement**: https://developer.apple.com/support/terms/
- **App Store Review Guidelines**: https://developer.apple.com/app-store/review/guidelines/
- **Apple Terms of Service**: https://www.apple.com/legal/internet-services/itunes/

Library Documentation

- **app-store-web-scraper**: https://github.com/nickreynolds/app-store-web-scraper
- **PyPI**: https://pypi.org/project/app-store-web-scraper/

## Error Handling

| Error              | Cause                 | Solution                         |
| ------------------ | --------------------- | -------------------------------- |
| App not found      | Invalid app ID        | Verify app exists on App Store   |
| Empty reviews      | New app or no reviews | Normal for apps with few reviews |
| Connection timeout | Network issues        | Retry with exponential backoff   |

## Validating App ID

Before fetching reviews, we validate the app ID using iTunes Lookup API:

```python
import requests

def validate_app(app_id):
    response = requests.get(f"https://itunes.apple.com/lookup?id={app_id}")
    data = response.json()
    return data.get("resultCount", 0) > 0
```

## Country Codes

Common country codes for `IOS_APP_STORE_COUNTRY`:

| Code | Country        |
| ---- | -------------- |
| us   | United States  |
| gb   | United Kingdom |
| ca   | Canada         |
| au   | Australia      |
| de   | Germany        |
| fr   | France         |
| jp   | Japan          |
| in   | India          |
