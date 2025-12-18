import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Star, Youtube, TrendingUp, Smartphone, AppWindow, MessageCircle, AlertCircle } from 'lucide-react'

interface Review {
  id: string
  user: string
  rating: number | null
  comment: string
  date: string
  likes?: number
  upvotes?: number
  helpful?: number
  platform: string
}

interface SentimentData {
  overall: {
    positive_percent: number
    neutral_percent: number
    negative_percent: number
    average_score: number
    total_analyzed: number
  }
  breakdown: {
    positive: number
    neutral: number
    negative: number
  }
  keywords: { word: string; count: number }[]
}

interface SourceReviews {
  platform: string
  identifier: string
  average_rating: number
  total_reviews: number
  reviews: Review[]
  error: string | null
  sentiment: SentimentData
}

interface ProductReviewsResponse {
  product_name: string
  sources: SourceReviews[]
  combined_sentiment: SentimentData | null
  errors: { platform: string; error: string }[]
}

interface SourceConfig {
  youtube_video: string
  product_hunt_product: string
  google_play_app: string
  ios_app: string
  reddit_subreddit: string
}

function App() {
  const [productName, setProductName] = useState<string>('')
  const [sourceConfig, setSourceConfig] = useState<SourceConfig>({
    youtube_video: '',
    product_hunt_product: '',
    google_play_app: '',
    ios_app: '',
    reddit_subreddit: ''
  })
  const [reviews, setReviews] = useState<ProductReviewsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const fetchReviews = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch('http://localhost:8000/api/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_name: productName || 'Unnamed Product',
          sources: sourceConfig
        })
      })
      const data = await response.json()
      setReviews(data)
    } catch {
      setError('Failed to fetch reviews. Make sure the FastAPI server is running on http://localhost:8000')
      setReviews(null)
    } finally {
      setLoading(false)
    }
  }

  const handleSourceChange = (field: keyof SourceConfig, value: string) => {
    setSourceConfig(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const hasAnySource = Object.values(sourceConfig).some(v => v.trim() !== '')

  const renderStars = (rating: number | null) => {
    if (rating === null) return null
    return (
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating
                ? 'fill-yellow-400 text-yellow-400'
                : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    )
  }

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'YouTube':
        return <Youtube className="w-5 h-5 text-red-600" />
      case 'Product Hunt':
        return <TrendingUp className="w-5 h-5 text-orange-600" />
      case 'Google Play Store':
        return <Smartphone className="w-5 h-5 text-green-600" />
      case 'iOS App Store':
        return <AppWindow className="w-5 h-5 text-blue-600" />
      case 'Reddit':
        return <MessageCircle className="w-5 h-5 text-orange-500" />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-3 text-gray-900">Perception Scanner</h1>
          <p className="text-lg text-gray-600">Aggregate reviews from multiple platforms in one place</p>
        </div>

        <Card className="border-gray-200 shadow-sm">
          <CardHeader className="bg-gray-50 border-b border-gray-200">
            <CardTitle className="text-2xl text-gray-900">Configure Product Sources</CardTitle>
            <CardDescription className="text-gray-600">Enter your product identifiers for each platform you want to scan</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 pt-6 bg-white">
            <div className="space-y-3">
              <Label htmlFor="product-name" className="text-sm font-semibold text-gray-700">Product Name</Label>
              <Input
                id="product-name"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Enter your product name"
                className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
              />
            </div>

            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Data Sources</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <Label htmlFor="google-play" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <Smartphone className="w-4 h-4 text-green-600" />
                    Google Play Store
                  </Label>
                  <Input
                    id="google-play"
                    value={sourceConfig.google_play_app}
                    onChange={(e) => handleSourceChange('google_play_app', e.target.value)}
                    placeholder="com.example.app"
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                  />
                  <p className="text-xs text-gray-500">Package name from Play Store URL</p>
                </div>

                <div className="space-y-3">
                  <Label htmlFor="ios-app" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <AppWindow className="w-4 h-4 text-blue-600" />
                    iOS App Store
                  </Label>
                  <Input
                    id="ios-app"
                    value={sourceConfig.ios_app}
                    onChange={(e) => handleSourceChange('ios_app', e.target.value)}
                    placeholder="1234567890"
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                  />
                  <p className="text-xs text-gray-500">Numeric App ID from App Store URL</p>
                </div>

                <div className="space-y-3">
                  <Label htmlFor="youtube" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <Youtube className="w-4 h-4 text-red-600" />
                    YouTube Video
                  </Label>
                  <Input
                    id="youtube"
                    value={sourceConfig.youtube_video}
                    onChange={(e) => handleSourceChange('youtube_video', e.target.value)}
                    placeholder="dQw4w9WgXcQ"
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                  />
                  <p className="text-xs text-gray-500">Video ID from YouTube URL (requires API key)</p>
                </div>

                <div className="space-y-3">
                  <Label htmlFor="product-hunt" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-orange-600" />
                    Product Hunt
                  </Label>
                  <Input
                    id="product-hunt"
                    value={sourceConfig.product_hunt_product}
                    onChange={(e) => handleSourceChange('product_hunt_product', e.target.value)}
                    placeholder="notion"
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                  />
                  <p className="text-xs text-gray-500">Product slug from Product Hunt URL (requires API token)</p>
                </div>

                <div className="space-y-3">
                  <Label htmlFor="reddit" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <MessageCircle className="w-4 h-4 text-orange-500" />
                    Reddit
                  </Label>
                  <Input
                    id="reddit"
                    value={sourceConfig.reddit_subreddit}
                    onChange={(e) => handleSourceChange('reddit_subreddit', e.target.value)}
                    placeholder="notion"
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                  />
                  <p className="text-xs text-gray-500">Subreddit name (without r/)</p>
                </div>
              </div>
            </div>

            <Button
              onClick={fetchReviews}
              disabled={loading || !hasAnySource}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-6 text-lg disabled:opacity-50"
            >
              {loading ? 'Scanning...' : 'Scan Reviews'}
            </Button>
            {!hasAnySource && (
              <p className="text-sm text-gray-500 text-center">Enter at least one source identifier to scan</p>
            )}
          </CardContent>
        </Card>

        {error && (
          <Card className="border-red-300 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-700 text-center font-medium">{error}</p>
            </CardContent>
          </Card>
        )}

        {reviews && !loading && (
          <div className="space-y-6">
            {reviews.errors && reviews.errors.length > 0 && (
              <Card className="border-yellow-300 bg-yellow-50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg text-yellow-800 flex items-center gap-2">
                    <AlertCircle className="w-5 h-5" />
                    Some sources had errors
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-1">
                    {reviews.errors.map((err, idx) => (
                      <li key={idx} className="text-sm text-yellow-700">
                        <span className="font-medium">{err.platform}:</span> {err.error}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            <div className="text-center py-6 border-b border-gray-200">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{reviews.product_name}</h2>
              <p className="text-gray-600">
                {reviews.sources.filter(s => !s.error).length} sources scanned successfully
              </p>
            </div>

            {reviews.combined_sentiment && (
              <Card className="border-gray-200 shadow-sm">
                <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50 border-b border-gray-200">
                  <CardTitle className="text-xl text-gray-900">Combined Sentiment Analysis</CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-3xl font-bold text-green-600">
                        {reviews.combined_sentiment.overall.positive_percent}%
                      </div>
                      <div className="text-sm text-green-700">Positive</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-3xl font-bold text-gray-600">
                        {reviews.combined_sentiment.overall.neutral_percent}%
                      </div>
                      <div className="text-sm text-gray-700">Neutral</div>
                    </div>
                    <div className="text-center p-4 bg-red-50 rounded-lg">
                      <div className="text-3xl font-bold text-red-600">
                        {reviews.combined_sentiment.overall.negative_percent}%
                      </div>
                      <div className="text-sm text-red-700">Negative</div>
                    </div>
                  </div>
                  {reviews.combined_sentiment.keywords.length > 0 && (
                    <div className="mt-6">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Top Keywords</h4>
                      <div className="flex flex-wrap gap-2">
                        {reviews.combined_sentiment.keywords.slice(0, 10).map((kw, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {kw.word} ({kw.count})
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {reviews.sources.filter(s => !s.error).length > 0 && (
              <Tabs defaultValue={reviews.sources.find(s => !s.error)?.platform} className="w-full">
                <TabsList className="grid w-full grid-cols-5 bg-gray-100 h-auto p-2 gap-2">
                  {reviews.sources.filter(s => !s.error).map((source) => (
                    <TabsTrigger
                      key={source.platform}
                      value={source.platform}
                      className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:text-blue-600"
                    >
                      {getPlatformIcon(source.platform)}
                      <span className="hidden md:inline">{source.platform}</span>
                    </TabsTrigger>
                  ))}
                </TabsList>

                {reviews.sources.filter(s => !s.error).map((source) => (
                  <TabsContent key={source.platform} value={source.platform} className="mt-6">
                    <Card className="border-gray-200 shadow-sm">
                      <CardHeader className="bg-gray-50 border-b border-gray-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            {getPlatformIcon(source.platform)}
                            <div>
                              <CardTitle className="text-2xl text-gray-900">{source.platform}</CardTitle>
                              <CardDescription className="text-sm text-gray-600 mt-1">{source.identifier}</CardDescription>
                            </div>
                          </div>
                          <div className="flex items-center gap-3 bg-white px-4 py-3 rounded-lg border border-gray-200">
                            {source.average_rating > 0 && renderStars(Math.round(source.average_rating))}
                            {source.average_rating > 0 && (
                              <span className="font-bold text-gray-900 text-lg">{source.average_rating}</span>
                            )}
                            <span className="text-gray-500 text-sm">
                              ({source.total_reviews} reviews)
                            </span>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-4 pt-6">
                        {source.reviews.length === 0 ? (
                          <p className="text-gray-500 text-center py-8">No reviews found</p>
                        ) : (
                          source.reviews.map((review) => (
                            <Card key={review.id} className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                              <CardHeader className="pb-3">
                                <div className="flex justify-between items-start gap-4">
                                  <div className="flex-1">
                                    <CardTitle className="text-base font-semibold text-gray-900">{review.user}</CardTitle>
                                    <CardDescription className="text-xs text-gray-500 mt-1">{review.date}</CardDescription>
                                  </div>
                                  <div className="flex flex-col items-end gap-2">
                                    {review.rating !== null && renderStars(review.rating)}
                                    <div className="flex flex-col items-end">
                                      {review.likes !== undefined && review.likes > 0 && (
                                        <span className="text-xs text-gray-600 font-medium">{review.likes} likes</span>
                                      )}
                                      {review.upvotes !== undefined && review.upvotes > 0 && (
                                        <span className="text-xs text-gray-600 font-medium">{review.upvotes} upvotes</span>
                                      )}
                                      {review.helpful !== undefined && review.helpful > 0 && (
                                        <span className="text-xs text-gray-600 font-medium">{review.helpful} helpful</span>
                                      )}
                                    </div>
                                  </div>
                                </div>
                              </CardHeader>
                              <CardContent className="pt-0">
                                <p className="text-sm text-gray-700 leading-relaxed">{review.comment}</p>
                              </CardContent>
                            </Card>
                          ))
                        )}
                      </CardContent>
                    </Card>
                  </TabsContent>
                ))}
              </Tabs>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
