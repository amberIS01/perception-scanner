// Recharts components for sentiment visualization
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'

// Counts: how many positive/neutral/negative reviews
interface SentimentBreakdown {
  positive: number
  neutral: number
  negative: number
}

// Percentages: what % are positive/neutral/negative (adds to 100)
interface SentimentPercentages {
  positive: number
  neutral: number
  negative: number
}

// Top keywords from reviews with their sentiment
interface Keyword {
  word: string
  count: number
  sentiment?: string
  score?: number
}

// Sentiment data for one platform (used in comparison chart)
interface PlatformSentiment {
  platform: string
  percentages: SentimentPercentages
  breakdown: SentimentBreakdown
  average_score: number
  total_analyzed: number
}

// Consistent colors: green=good, gray=neutral, red=bad
const COLORS = {
  positive: '#22c55e',
  neutral: '#6b7280',
  negative: '#ef4444',
}

// Horizontal stacked bar showing sentiment distribution
export function SentimentStackedBar({
  percentages,
  showLabels = true,
}: {
  percentages: SentimentPercentages
  showLabels?: boolean
}) {
  return (
    <div className="w-full">
      <div className="flex h-8 rounded-lg overflow-hidden">
        {percentages.positive > 0 && (
          <div
            className="bg-green-500 flex items-center justify-center text-white text-xs font-medium transition-all"
            style={{ width: `${percentages.positive}%` }}
          >
            {showLabels && percentages.positive >= 10 && `${percentages.positive}%`}
          </div>
        )}
        {percentages.neutral > 0 && (
          <div
            className="bg-gray-400 flex items-center justify-center text-white text-xs font-medium transition-all"
            style={{ width: `${percentages.neutral}%` }}
          >
            {showLabels && percentages.neutral >= 10 && `${percentages.neutral}%`}
          </div>
        )}
        {percentages.negative > 0 && (
          <div
            className="bg-red-500 flex items-center justify-center text-white text-xs font-medium transition-all"
            style={{ width: `${percentages.negative}%` }}
          >
            {showLabels && percentages.negative >= 10 && `${percentages.negative}%`}
          </div>
        )}
      </div>
      {showLabels && (
        <div className="flex justify-between mt-2 text-xs text-gray-600">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 bg-green-500 rounded-sm"></span>
            Positive ({percentages.positive}%)
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 bg-gray-400 rounded-sm"></span>
            Neutral ({percentages.neutral}%)
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 bg-red-500 rounded-sm"></span>
            Negative ({percentages.negative}%)
          </span>
        </div>
      )}
    </div>
  )
}

// Horizontal bar chart showing top keywords by frequency
export function KeywordBarChart({
  keywords,
  maxItems = 10,
}: {
  keywords: Keyword[]
  maxItems?: number
}) {
  const data = keywords.slice(0, maxItems).map((k) => ({
    word: k.word,
    count: k.count,
    sentiment: k.sentiment || 'neutral',
  }))

  const getBarColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return COLORS.positive
      case 'negative':
        return COLORS.negative
      default:
        return COLORS.neutral
    }
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" />
          <YAxis
            type="category"
            dataKey="word"
            width={70}
            tick={{ fontSize: 12 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            formatter={(value) => [`${value} mentions`, 'Count']}
          />
          <Bar dataKey="count" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getBarColor(entry.sentiment)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Grouped bar chart comparing sentiment across platforms
export function VerticalSentimentBars({
  platforms,
}: {
  platforms: PlatformSentiment[]
}) {
  const data = platforms.map((p) => ({
    platform: p.platform.replace(' Store', '').replace('Google Play', 'Play'),
    Positive: p.percentages.positive,
    Neutral: p.percentages.neutral,
    Negative: p.percentages.negative,
  }))

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="platform" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
          <Tooltip
            formatter={(value) => [`${value}%`, '']}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey="Positive" fill={COLORS.positive} radius={[4, 4, 0, 0]} />
          <Bar dataKey="Neutral" fill={COLORS.neutral} radius={[4, 4, 0, 0]} />
          <Bar dataKey="Negative" fill={COLORS.negative} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
