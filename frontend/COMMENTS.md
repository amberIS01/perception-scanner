# Frontend Code Comments Tracking

All comments added to explain what the code does and why.

## src/main.tsx
| Line | Comment |
|------|---------|
| 1 | `// React entry point - renders App into #root div` |

## src/lib/utils.ts
| Line | Comment |
|------|---------|
| 4 | `// Utility to merge Tailwind classes (used by all shadcn/ui components)` |

## src/App.tsx
| Line | Comment |
|------|---------|
| 14 | `// Single review from any platform` |
| 25 | `// VADER sentiment analysis result` |
| 43 | `// Reviews from one platform (Google Play, iOS, YouTube, etc.)` |
| 54 | `// Full API response from POST /api/reviews` |
| 62 | `// User input: identifiers for each platform` |
| 87 | `// Call backend API to fetch and analyze reviews` |
| 112 | `// Update source config when user types in input` |
| 120 | `// Enable scan button only if at least one source is configured` |
| 123 | `// Render 1-5 star rating (Google Play and iOS only - others have no ratings)` |
| 140 | `// Return platform-specific icon with brand color` |

## src/components/charts/SentimentCharts.tsx
| Line | Comment |
|------|---------|
| 1 | `// Recharts components for sentiment visualization` |
| 14 | `// Counts: how many positive/neutral/negative reviews` |
| 21 | `// Percentages: what % are positive/neutral/negative (adds to 100)` |
| 28 | `// Top keywords from reviews with their sentiment` |
| 36 | `// Sentiment data for one platform (used in comparison chart)` |
| 45 | `// Consistent colors: green=good, gray=neutral, red=bad` |
| 52 | `// Horizontal stacked bar showing sentiment distribution` |
| 108 | `// Horizontal bar chart showing top keywords by frequency` |
| 168 | `// Grouped bar chart comparing sentiment across platforms` |

---

**Total: 19 comments added**

All comments follow these rules:
- Short and direct (1 line)
- Explain what it does, not how
- No AI-generated verbosity
