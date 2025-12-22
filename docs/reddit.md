# Reddit Source

## Overview

| Property         | Value                      |
| ---------------- | -------------------------- |
| Platform         | Reddit                     |
| Method           | Public JSON Endpoints      |
| API Key Required | No                         |
| Max Posts        | ~100 per request           |
| Rate Limits      | Unofficial (be respectful) |

## How It Works

This source uses Reddit's public JSON endpoints (append `.json` to any Reddit URL) to fetch posts and comments from subreddits. No API key or authentication is required.

## Setup Instructions

### Step 1: No API Key Needed

Reddit's public JSON endpoints are freely accessible without authentication.

### Step 2: Configure User Agent (Optional)

Add to your `.env` file:

```bash
REDDIT_USER_AGENT=PerceptionScanner/1.0
```

**Note**: A descriptive User-Agent helps Reddit identify your application and is considered good practice.

### Step 3: Find Subreddit Name

The subreddit name is in the Reddit URL:

```
URL: https://www.reddit.com/r/notion
Subreddit: notion
```

**Note**: Use just the subreddit name without "r/" prefix.

## Configuration

Environment variables in `.env`:

```bash
# Custom User-Agent string (recommended)
REDDIT_USER_AGENT=PerceptionScanner/1.0
```

## Usage Example

```python
from services.sources import RedditSource

source = RedditSource()
result = await source.fetch_reviews("notion", count=100)

print(f"Posts: {result.total_reviews}")
for review in result.reviews:
    print(f"{review.user}: {review.comment[:50]}...")
```

## Rate Limits

Since this uses public endpoints (not the official API):

| Consideration     | Recommendation                   |
| ----------------- | -------------------------------- |
| Request frequency | Max 1 request per 2 seconds      |
| Daily requests    | No official limit, be respectful |
| Burst requests    | Avoid rapid consecutive requests |

**Important**: Excessive requests may result in temporary IP blocks.

## Limitations

1. **Public Endpoints**: Uses unofficial JSON endpoints, not OAuth API
2. **No Authentication**: Cannot access private subreddits or user-specific data
3. **Posts Only**: Fetches top-level posts, not nested comment threads
4. **Sorting Fixed**: Returns "hot" posts by default
5. **Rate Limits**: May be rate-limited without warning
6. **Subject to Change**: Public endpoints may change without notice

## Data Retrieved

| Field   | Description                      |
| ------- | -------------------------------- |
| id      | Reddit comment ID                |
| user    | Author's username                |
| comment | Comment body text                |
| date    | Comment creation date            |
| likes   | Comment score (upvotes - downvotes) |
| rating  | Always null (no ratings)         |

## Terms & Conditions

- **Reddit User Agreement**: https://www.redditinc.com/policies/user-agreement
- **Reddit API Terms**: https://www.reddit.com/wiki/api-terms
- **Reddit Privacy Policy**: https://www.reddit.com/policies/privacy-policy
- **Content Policy**: https://www.redditinc.com/policies/content-policy

## API Documentation

- **Reddit API Overview**: https://www.reddit.com/dev/api/
- **JSON Endpoints**: https://github.com/reddit-archive/reddit/wiki/JSON
- **Official API (OAuth)**: https://www.reddit.com/wiki/api

## Public JSON Endpoint Structure

Reddit provides JSON data by appending `.json` to URLs:

```
Subreddit posts: https://www.reddit.com/r/{subreddit}.json
Post comments: https://www.reddit.com/r/{subreddit}/comments/{id}.json
```

### Query Parameters

| Parameter | Description               | Example              |
| --------- | ------------------------- | -------------------- |
| `limit` | Number of posts (max 100) | `?limit=100`       |
| `after` | Pagination cursor         | `?after=t3_abc123` |
| `sort`  | Sort order                | `?sort=hot`        |

## Error Handling

| Error                     | Cause                        | Solution                       |
| ------------------------- | ---------------------------- | ------------------------------ |
| `403 Forbidden`         | Blocked or private subreddit | Verify subreddit is public     |
| `404 Not Found`         | Subreddit doesn't exist      | Check subreddit name spelling  |
| `429 Too Many Requests` | Rate limited                 | Wait and retry with backoff    |
| Connection timeout        | Network issues               | Retry with exponential backoff |

## Subreddit Search Tips

When searching for product feedback on Reddit:

- Search for `r/{productname}` - Official subreddit
- Search for `r/{productname}app` - App-specific subreddit
