from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SourceConfig(BaseModel):
    youtube_channel: Optional[str] = None
    instagram_account: Optional[str] = None
    product_hunt_product: Optional[str] = None
    google_play_app: Optional[str] = None
    ios_app: Optional[str] = None
    google_workspace_app: Optional[str] = None

class ProductReviewRequest(BaseModel):
    product_name: str
    sources: SourceConfig

@app.post("/api/reviews")
async def get_reviews(request: ProductReviewRequest):
    # Hardcoded reviews database organized by source type
    reviews_by_source = {
        "youtube": [
            {
                "id": 1,
                "user": "TechReviewer123",
                "rating": 5,
                "comment": "Great tutorial! This product has really helped streamline my workflow. The interface is intuitive and the features are exactly what I needed.",
                "date": "2024-12-05",
                "likes": 342,
                "platform": "YouTube"
            },
            {
                "id": 2,
                "user": "ProductivityGuru",
                "rating": 4,
                "comment": "Solid product, though there's a bit of a learning curve. Once you get past that, it's incredibly powerful.",
                "date": "2024-12-01",
                "likes": 128,
                "platform": "YouTube"
            },
            {
                "id": 3,
                "user": "DigitalNomad",
                "rating": 5,
                "comment": "This has become essential to my daily routine. Can't imagine working without it now!",
                "date": "2024-11-28",
                "likes": 256,
                "platform": "YouTube"
            }
        ],
        "instagram": [
            {
                "id": 1,
                "user": "@startuplife",
                "rating": 5,
                "comment": "Game changer for our team! 🚀 Highly recommend to anyone looking to boost productivity.",
                "date": "2024-12-07",
                "likes": 892,
                "platform": "Instagram"
            },
            {
                "id": 2,
                "user": "@creativeagency",
                "rating": 4,
                "comment": "Love the clean design and smooth user experience. A few features could be improved but overall excellent!",
                "date": "2024-12-03",
                "likes": 445,
                "platform": "Instagram"
            },
            {
                "id": 3,
                "user": "@techenthusiast",
                "rating": 5,
                "comment": "Finally found the perfect solution! The integration options are fantastic. 💯",
                "date": "2024-11-30",
                "likes": 621,
                "platform": "Instagram"
            }
        ],
        "product_hunt": [
            {
                "id": 1,
                "user": "sarah_founder",
                "rating": 5,
                "comment": "Congrats on the launch! This is exactly what the market needs. The execution is flawless and the value proposition is clear.",
                "date": "2024-12-08",
                "upvotes": 234,
                "platform": "Product Hunt"
            },
            {
                "id": 2,
                "user": "dev_mike",
                "rating": 4,
                "comment": "Really impressive product. The API documentation could use some work, but the core functionality is solid.",
                "date": "2024-12-08",
                "upvotes": 189,
                "platform": "Product Hunt"
            },
            {
                "id": 3,
                "user": "entrepreneur_jane",
                "rating": 5,
                "comment": "Been using this in beta for weeks. It's revolutionized how we work. Definitely deserves Product of the Day!",
                "date": "2024-12-08",
                "upvotes": 301,
                "platform": "Product Hunt"
            }
        ],
        "google_play": [
            {
                "id": 1,
                "user": "Alex Thompson",
                "rating": 5,
                "comment": "Best app in its category! Fast, reliable, and the UI is beautiful. Worth every penny of the subscription.",
                "date": "2024-12-06",
                "helpful": 156,
                "platform": "Google Play Store"
            },
            {
                "id": 2,
                "user": "Maria Garcia",
                "rating": 4,
                "comment": "Very useful app. Sometimes crashes on older devices but overall works great. Customer support is responsive.",
                "date": "2024-12-02",
                "helpful": 89,
                "platform": "Google Play Store"
            },
            {
                "id": 3,
                "user": "James Wilson",
                "rating": 5,
                "comment": "Downloaded this on a whim and now use it daily. Syncs perfectly across all my devices. Highly recommended!",
                "date": "2024-11-29",
                "helpful": 203,
                "platform": "Google Play Store"
            },
            {
                "id": 4,
                "user": "Lisa Chen",
                "rating": 3,
                "comment": "Good app but the free tier is too limited. Would be nice to have more features available without subscription.",
                "date": "2024-11-25",
                "helpful": 67,
                "platform": "Google Play Store"
            }
        ],
        "ios_app": [
            {
                "id": 1,
                "user": "TechSavvyUser",
                "rating": 5,
                "comment": "Phenomenal app! Integrates beautifully with iOS ecosystem. The widgets are particularly well-designed.",
                "date": "2024-12-07",
                "helpful": 178,
                "platform": "iOS App Store"
            },
            {
                "id": 2,
                "user": "DesignerDave",
                "rating": 5,
                "comment": "Finally, an app that looks native and performs flawlessly. The attention to detail is incredible.",
                "date": "2024-12-04",
                "helpful": 145,
                "platform": "iOS App Store"
            },
            {
                "id": 3,
                "user": "BusyMom2023",
                "rating": 4,
                "comment": "Very helpful for organizing my day. Would love to see more customization options in future updates.",
                "date": "2024-12-01",
                "helpful": 92,
                "platform": "iOS App Store"
            },
            {
                "id": 4,
                "user": "StudentLife",
                "rating": 5,
                "comment": "This app has been a lifesaver during finals week. Clean interface, powerful features. 10/10!",
                "date": "2024-11-27",
                "helpful": 234,
                "platform": "iOS App Store"
            }
        ],
        "google_workspace": [
            {
                "id": 1,
                "user": "IT Manager - TechCorp",
                "rating": 5,
                "comment": "Seamless integration with Google Workspace. Our team adopted it immediately. The admin controls are comprehensive.",
                "date": "2024-12-05",
                "helpful": 89,
                "platform": "Google Workspace Marketplace"
            },
            {
                "id": 2,
                "user": "Operations Director",
                "rating": 4,
                "comment": "Great add-on for Workspace. Saves us hours every week. Pricing is a bit high for small teams though.",
                "date": "2024-12-01",
                "helpful": 56,
                "platform": "Google Workspace Marketplace"
            },
            {
                "id": 3,
                "user": "Project Manager",
                "rating": 5,
                "comment": "Works perfectly with Gmail and Calendar. The permissions system is well thought out. Highly recommend for enterprise use.",
                "date": "2024-11-28",
                "helpful": 112,
                "platform": "Google Workspace Marketplace"
            }
        ]
    }

    # Build response based on configured sources
    result = {
        "product_name": request.product_name,
        "sources": []
    }

    if request.sources.youtube_channel:
        result["sources"].append({
            "platform": "YouTube",
            "identifier": request.sources.youtube_channel,
            "average_rating": 4.7,
            "total_reviews": 3,
            "reviews": reviews_by_source["youtube"]
        })

    if request.sources.instagram_account:
        result["sources"].append({
            "platform": "Instagram",
            "identifier": request.sources.instagram_account,
            "average_rating": 4.7,
            "total_reviews": 3,
            "reviews": reviews_by_source["instagram"]
        })

    if request.sources.product_hunt_product:
        result["sources"].append({
            "platform": "Product Hunt",
            "identifier": request.sources.product_hunt_product,
            "average_rating": 4.7,
            "total_reviews": 3,
            "reviews": reviews_by_source["product_hunt"]
        })

    if request.sources.google_play_app:
        result["sources"].append({
            "platform": "Google Play Store",
            "identifier": request.sources.google_play_app,
            "average_rating": 4.2,
            "total_reviews": 4,
            "reviews": reviews_by_source["google_play"]
        })

    if request.sources.ios_app:
        result["sources"].append({
            "platform": "iOS App Store",
            "identifier": request.sources.ios_app,
            "average_rating": 4.8,
            "total_reviews": 4,
            "reviews": reviews_by_source["ios_app"]
        })

    if request.sources.google_workspace_app:
        result["sources"].append({
            "platform": "Google Workspace",
            "identifier": request.sources.google_workspace_app,
            "average_rating": 4.7,
            "total_reviews": 3,
            "reviews": reviews_by_source["google_workspace"]
        })

    return result
