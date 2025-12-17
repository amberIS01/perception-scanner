# YouTube Source

## Overview

| Property         | Value                        |
| ---------------- | ---------------------------- |
| Platform         | YouTube                      |
| Method           | Official API                 |
| API Key Required | Yes (Free)                   |
| Max Comments     | Unlimited (quota-based)      |
| Rate Limits      | 10,000 units/day (free tier) |

## How It Works

This source uses the official YouTube Data API v3 to fetch comments from videos. It requires a free API key from Google Cloud Console.

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Perception Scanner")
4. Click "Create"

### Step 2: Enable YouTube Data API

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and click "Enable"

### Step 3: Create API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the generated API key
4. (Optional) Click "Restrict Key" to limit usage

### Step 4: Configure Environment

Add to your `.env` file:

```bash
YOUTUBE_API_KEY=your_api_key_here
```

### Step 5: Find Video ID

The video ID is in the YouTube URL:

```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Video ID: dQw4w9WgXcQ
```

## Configuration

Environment variables in `.env`:

```bash
# YouTube Data API v3 key (required)
YOUTUBE_API_KEY=AIzaSy...your_key_here
```

## Usage Example

```python
from services.sources import YouTubeSource

source = YouTubeSource()
result = await source.fetch_reviews("dQw4w9WgXcQ", count=100)

print(f"Comments: {result.total_reviews}")
for review in result.reviews:
    print(f"{review.user}: {review.comment[:50]}...")
```

## Rate Limits & Quota

YouTube API uses a quota system:

| Operation           | Quota Cost |
| ------------------- | ---------- |
| commentThreads.list | 1 unit     |
| videos.list         | 1 unit     |

**Daily Quota (Free Tier):** 10,000 units

This means you can fetch approximately:

- ~10,000 comment requests per day
- ~1,000,000 comments per day (100 per request)

### Quota Tips

- Comments are fetched in batches of 100 (max)
- Each batch costs 1 quota unit
- To fetch 1000 comments = 10 quota units
- Monitor usage in Google Cloud Console

## Limitations

1. **Comments Only**: YouTube doesn't have traditional "reviews" - we fetch video comments
2. **No Ratings**: Comments don't have star ratings (we use like count as engagement metric)
3. **Comments May Be Disabled**: Some videos disable comments
4. **Quota Limits**: Free tier has daily limits
5. **Video Must Be Public**: Cannot access private video comments

## Data Retrieved

| Field      | Description                   |
| ---------- | ----------------------------- |
| id         | Comment thread ID             |
| user       | Commenter's channel name      |
| comment    | Comment text                  |
| date       | Comment publish date          |
| likes      | Number of likes on comment    |
| user_image | Commenter's profile image URL |

## Terms & Conditions

- **YouTube Terms of Service**: https://www.youtube.com/t/terms
- **YouTube API Terms**: https://developers.google.com/youtube/terms/api-services-terms-of-service
- **Google Cloud Terms**: https://cloud.google.com/terms
- **Acceptable Use Policy**: https://developers.google.com/youtube/terms/developer-policies

## API Documentation

- **YouTube Data API v3**: https://developers.google.com/youtube/v3
- **CommentThreads Resource**: https://developers.google.com/youtube/v3/docs/commentThreads
- **Quota Calculator**: https://developers.google.com/youtube/v3/determine_quota_cost

## Error Handling

| Error                | Cause                         | Solution                                      |
| -------------------- | ----------------------------- | --------------------------------------------- |
| `commentsDisabled` | Comments disabled on video    | Cannot fetch - skip this video                |
| `quotaExceeded`    | Daily quota reached           | Wait until next day or request quota increase |
| `videoNotFound`    | Invalid video ID              | Verify video exists and is public             |
| `403 Forbidden`    | API key invalid or restricted | Check API key configuration                   |

## Increasing Quota

If you need more than 10,000 units/day:

1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Quotas"
3. Select YouTube Data API v3
4. Click "Request quota increase"
5. Fill out the form explaining your use case

**Note**: Quota increases require review and may take several days.
