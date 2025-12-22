# Product Hunt Source

## Overview

| Property         | Value                   |
| ---------------- | ----------------------- |
| Platform         | Product Hunt            |
| Method           | Official GraphQL API    |
| API Key Required | Yes (Free)              |
| Max Comments     | 100 per request         |
| Rate Limits      | 900 requests/15 minutes |

## How It Works

This source uses the official Product Hunt GraphQL API v2 to fetch comments from product pages. It requires a free Developer Token from Product Hunt.

## Setup Instructions

### Step 1: Create Product Hunt Account

1. Go to [Product Hunt](https://www.producthunt.com/)
2. Sign up or log in to your account

### Step 2: Create API Application

1. Go to [Product Hunt API Dashboard](https://api.producthunt.com/v2/oauth/applications)
2. Click "Add an Application"
3. Fill in the details:
   - **Name**: Your application name (e.g., "Perception Scanner")
   - **Redirect URI**: `https://localhost` (required but not used for server-to-server)
4. Click "Create Application"

### Step 3: Get Developer Token

1. After creating the application, you'll see:
   - **API Key**: Used for OAuth flows (not needed for basic access)
   - **Developer Token**: Used for direct API access
2. Copy the **Developer Token**

### Step 4: Configure Environment

Add to your `.env` file:

```bash
PRODUCT_HUNT_API_TOKEN=your_developer_token_here
```

### Step 5: Find Product Slug

The product slug is in the Product Hunt URL:

```
URL: https://www.producthunt.com/posts/notion
Product Slug: notion
```

**Note**: Use the slug (text identifier), not a numeric ID.

## Configuration

Environment variables in `.env`:

```bash
# Product Hunt Developer Token (required)
PRODUCT_HUNT_API_TOKEN=_8eDb-...your_token_here
```

## Usage Example

```python
from services.sources import ProductHuntSource

source = ProductHuntSource()
result = await source.fetch_reviews("notion", count=100)

print(f"Comments: {result.total_reviews}")
for review in result.reviews:
    print(f"{review.user}: {review.comment[:50]}...")
```

## Rate Limits

Product Hunt API has the following rate limits:

| Limit Type              | Value     |
| ----------------------- | --------- |
| Requests per 15 minutes | 900       |
| Comments per request    | 100 (max) |

**Note**: Rate limits are generous for most use cases. Monitor your usage in the API dashboard.

## Limitations

1. **Comments Only**: Product Hunt doesn't have traditional "reviews" - we fetch product comments
2. **No Ratings**: Comments don't have star ratings
3. **Pagination Limit**: Maximum 100 comments per request
4. **Public Products Only**: Cannot access private/unreleased products

## Data Retrieved

| Field   | Description                              |
| ------- | ---------------------------------------- |
| id      | Comment ID                               |
| user    | Commenter's name or username             |
| comment | Comment body text                        |
| date    | Comment creation date (YYYY-MM-DD)       |
| rating  | Always null (no ratings on Product Hunt) |
| likes   | Always null (not extracted)              |

## Terms & Conditions

- **Product Hunt Terms of Service**: https://www.producthunt.com/terms
- **API Terms of Use**: https://api.producthunt.com/v2/docs
- **Privacy Policy**: https://www.producthunt.com/privacy

## API Documentation

- **Product Hunt API v2**: https://api.producthunt.com/v2/docs
- **GraphQL Explorer**: https://api.producthunt.com/v2/docs/graphql_explorer
- **OAuth Guide**: https://api.producthunt.com/v2/docs/oauth_client_only_authentication

## GraphQL Query Structure

The API uses GraphQL. Here's the query structure we use:

```graphql
query {
  post(slug: "product-slug") {
    id
    name
    tagline
    votesCount
    commentsCount
    comments(first: 100) {
      edges {
        node {
          id
          body
          createdAt
          user {
            name
            username
            profileImage
          }
        }
      }
    }
  }
}
```

## Error Handling

| Error                     | Cause                    | Solution                              |
| ------------------------- | ------------------------ | ------------------------------------- |
| `401 Unauthorized`      | Invalid or expired token | Regenerate token in API dashboard     |
| `429 Too Many Requests` | Rate limit exceeded      | Wait and retry with backoff           |
| `Product not found`     | Invalid slug             | Verify product exists on Product Hunt |
| `403 Forbidden`         | Token lacks permissions  | Check token scopes                    |
