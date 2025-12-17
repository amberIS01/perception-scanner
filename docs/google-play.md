# Google Play Store - Reviews Integration

## Overview

This integration fetches app reviews from the Google Play Store using the `google-play-scraper` Python library.

## Method

**Type:** Web Scraping (unofficial)

**Library:** [google-play-scraper](https://pypi.org/project/google-play-scraper/) v1.2.7

This integration uses an unofficial scraping library, not an official Google API. The library scrapes publicly available review data from the Google Play Store website.

## API Key Required

**No API key required.** This library works without any authentication.

## Setup Instructions

1. Install the library:

   ```bash
   pip install google-play-scraper
   ```
2. No additional configuration needed.

## Usage

To fetch reviews, you need the app's **package name** (e.g., `com.whatsapp`, `com.spotify.music`).

You can find the package name in the Google Play Store URL:

```
https://play.google.com/store/apps/details?id=com.whatsapp
                                              ^^^^^^^^^^^^
                                              package name
```

## Rate Limits

| Limit Type          | Value                    | Notes                                          |
| ------------------- | ------------------------ | ---------------------------------------------- |
| Official Rate Limit | None                     | No official rate limit (unofficial library)    |
| Practical Limit     | ~100-200 requests/minute | Avoid aggressive scraping to prevent IP blocks |
| Reviews per Request | 200 max                  | Library fetches up to 200 reviews per page     |

## Data Retrieved

| Field                    | Description                         |
| ------------------------ | ----------------------------------- |
| `reviewId`             | Unique review identifier            |
| `userName`             | Reviewer's display name             |
| `userImage`            | URL to reviewer's profile image     |
| `content`              | Review text                         |
| `score`                | Rating (1-5 stars)                  |
| `thumbsUpCount`        | Number of "helpful" votes           |
| `reviewCreatedVersion` | App version when review was written |
| `at`                   | Review date/time                    |
| `replyContent`         | Developer's reply (if any)          |
| `repliedAt`            | Developer reply date (if any)       |

## Limitations

1. **Unofficial Method**: This is web scraping, not an official API. Google could change their website structure at any time, breaking the library.
2. **No Real-time Data**: Reviews may be slightly delayed compared to what appears on the Play Store.
3. **Language/Country Specific**: Reviews are fetched for a specific language and country. To get all reviews, you'd need to query multiple country codes.
4. **No Write Access**: You can only read reviews, not respond to them. Use the official Google Play Developer Console for that.
5. **IP Blocking Risk**: Aggressive scraping may result in temporary IP blocks from Google.

## Official Alternative

Google offers an official [Google Play Developer API](https://developers.google.com/android-publisher) for developers who own the app. However:

- Requires ownership/access to the app's developer account
- Limited to 60 requests/hour for reviews
- More reliable but restricted access

## Useful Links

- [google-play-scraper PyPI](https://pypi.org/project/google-play-scraper/)
- [google-play-scraper GitHub](https://github.com/JoMingyu/google-play-scraper)
- [Google Play Developer API (official)](https://developers.google.com/android-publisher)
- [Google Play Console](https://play.google.com/console)

## Example Code

```python
from google_play_scraper import reviews, Sort

# Fetch 100 most recent reviews for WhatsApp
result, continuation_token = reviews(
    'com.whatsapp',
    lang='en',
    country='us',
    sort=Sort.NEWEST,
    count=100
)

for review in result:
    print(f"{review['userName']}: {review['score']} stars")
    print(f"  {review['content'][:100]}...")
```
