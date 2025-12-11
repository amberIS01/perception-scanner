import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Star, Youtube, Instagram, TrendingUp, Smartphone, AppWindow, Briefcase } from 'lucide-react'

interface Review {
  id: number
  user: string
  rating: number
  comment: string
  date: string
  likes?: number
  upvotes?: number
  helpful?: number
  platform: string
}

interface SourceReviews {
  platform: string
  identifier: string
  average_rating: number
  total_reviews: number
  reviews: Review[]
}

interface ProductReviewsResponse {
  product_name: string
  sources: SourceReviews[]
}

interface SourceConfig {
  youtube_channel: string
  instagram_account: string
  product_hunt_product: string
  google_play_app: string
  ios_app: string
  google_workspace_app: string
}

function App() {
  const [productName, setProductName] = useState<string>('My SaaS Product')
  const [sourceConfig, setSourceConfig] = useState<SourceConfig>({
    youtube_channel: '@mysaaschannel',
    instagram_account: '@mysaasproduct',
    product_hunt_product: 'my-saas-product',
    google_play_app: 'com.mysaas.app',
    ios_app: 'id123456789',
    google_workspace_app: 'my-saas-workspace'
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
          product_name: productName,
          sources: sourceConfig
        })
      })
      const data = await response.json()
      setReviews(data)
    } catch (error) {
      setError('Failed to fetch reviews. Make sure the FastAPI server is running.')
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

  const renderStars = (rating: number) => {
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
      case 'Instagram':
        return <Instagram className="w-5 h-5 text-pink-600" />
      case 'Product Hunt':
        return <TrendingUp className="w-5 h-5 text-orange-600" />
      case 'Google Play Store':
        return <Smartphone className="w-5 h-5 text-green-600" />
      case 'iOS App Store':
        return <AppWindow className="w-5 h-5 text-blue-600" />
      case 'Google Workspace':
        return <Briefcase className="w-5 h-5 text-blue-700" />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-3 text-gray-900">SaaS Perception Scanner</h1>
          <p className="text-lg text-gray-600">Aggregate reviews from multiple platforms in one place</p>
        </div>

        <Card className="border-gray-200 shadow-sm">
          <CardHeader className="bg-gray-50 border-b border-gray-200">
            <CardTitle className="text-2xl text-gray-900">Configure Product Sources</CardTitle>
            <CardDescription className="text-gray-600">Enter your product name and configure the sources to scan</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 pt-6 bg-white">
            <div className="space-y-3">
              <Label htmlFor="product-name" className="text-sm font-semibold text-gray-700">Product Name</Label>
              <Input
                id="product-name"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Enter your SaaS product name"
                className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
              />
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <Label htmlFor="youtube" className="text-sm font-semibold text-gray-700">YouTube Channel</Label>
                <Input
                  id="youtube"
                  value={sourceConfig.youtube_channel}
                  onChange={(e) => handleSourceChange('youtube_channel', e.target.value)}
                  placeholder="@yourchannelname"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="instagram" className="text-sm font-semibold text-gray-700">Instagram Account</Label>
                <Input
                  id="instagram"
                  value={sourceConfig.instagram_account}
                  onChange={(e) => handleSourceChange('instagram_account', e.target.value)}
                  placeholder="@yourproduct"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="product-hunt" className="text-sm font-semibold text-gray-700">Product Hunt</Label>
                <Input
                  id="product-hunt"
                  value={sourceConfig.product_hunt_product}
                  onChange={(e) => handleSourceChange('product_hunt_product', e.target.value)}
                  placeholder="your-product-slug"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="google-play" className="text-sm font-semibold text-gray-700">Google Play Store</Label>
                <Input
                  id="google-play"
                  value={sourceConfig.google_play_app}
                  onChange={(e) => handleSourceChange('google_play_app', e.target.value)}
                  placeholder="com.yourapp.package"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="ios-app" className="text-sm font-semibold text-gray-700">iOS App Store</Label>
                <Input
                  id="ios-app"
                  value={sourceConfig.ios_app}
                  onChange={(e) => handleSourceChange('ios_app', e.target.value)}
                  placeholder="id123456789"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="workspace" className="text-sm font-semibold text-gray-700">Google Workspace</Label>
                <Input
                  id="workspace"
                  value={sourceConfig.google_workspace_app}
                  onChange={(e) => handleSourceChange('google_workspace_app', e.target.value)}
                  placeholder="your-workspace-app"
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900"
                />
              </div>
            </div>

            <Button onClick={fetchReviews} disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-6 text-lg">
              {loading ? 'Scanning...' : 'Scan Reviews'}
            </Button>
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
            <div className="text-center py-6 border-b border-gray-200">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{reviews.product_name}</h2>
              <p className="text-gray-600">Reviews from {reviews.sources.length} sources</p>
            </div>

            <Tabs defaultValue={reviews.sources[0]?.platform} className="w-full">
              <TabsList className="grid w-full grid-cols-6 bg-gray-100 h-auto p-2 gap-2">
                {reviews.sources.map((source) => (
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

              {reviews.sources.map((source) => (
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
                          {renderStars(Math.round(source.average_rating))}
                          <span className="font-bold text-gray-900 text-lg">{source.average_rating}</span>
                          <span className="text-gray-500 text-sm">
                            ({source.total_reviews} reviews)
                          </span>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4 pt-6">
                      {source.reviews.map((review) => (
                        <Card key={review.id} className="bg-white border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                          <CardHeader className="pb-3">
                            <div className="flex justify-between items-start gap-4">
                              <div className="flex-1">
                                <CardTitle className="text-base font-semibold text-gray-900">{review.user}</CardTitle>
                                <CardDescription className="text-xs text-gray-500 mt-1">{review.date}</CardDescription>
                              </div>
                              <div className="flex flex-col items-end gap-2">
                                {renderStars(review.rating)}
                                <div className="flex flex-col items-end">
                                  {review.likes !== undefined && (
                                    <span className="text-xs text-gray-600 font-medium">{review.likes} likes</span>
                                  )}
                                  {review.upvotes !== undefined && (
                                    <span className="text-xs text-gray-600 font-medium">{review.upvotes} upvotes</span>
                                  )}
                                  {review.helpful !== undefined && (
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
                      ))}
                    </CardContent>
                  </Card>
                </TabsContent>
              ))}
            </Tabs>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
