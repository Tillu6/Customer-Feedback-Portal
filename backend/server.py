from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class FeedbackCategory(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"
    SUPPORT = "support"
    OVERALL = "overall"

class FeedbackCreate(BaseModel):
    customer_name: str
    customer_email: str
    category: FeedbackCategory
    rating: int = Field(..., ge=1, le=5)
    comment: str
    additional_data: Optional[dict] = {}

class Feedback(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    customer_email: str
    category: FeedbackCategory
    rating: int
    comment: str
    additional_data: Optional[dict] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sentiment_score: Optional[float] = None

class FeedbackStats(BaseModel):
    total_feedback: int
    avg_rating: float
    category_breakdown: dict
    rating_distribution: dict
    recent_feedback: List[Feedback]

# Simple sentiment analysis function (can be enhanced with AI)
def analyze_sentiment(text: str) -> float:
    """Simple sentiment analysis - returns score between -1 (negative) and 1 (positive)"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect', 'outstanding']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'disappointing', 'poor', 'useless']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count + negative_count == 0:
        return 0.0
    
    return (positive_count - negative_count) / (positive_count + negative_count)

# Routes
@api_router.get("/")
async def root():
    return {"message": "Customer Feedback Portal API"}

@api_router.post("/feedback", response_model=Feedback)
async def create_feedback(feedback_data: FeedbackCreate):
    """Create a new feedback entry with sentiment analysis"""
    feedback_dict = feedback_data.dict()
    
    # Add sentiment analysis
    sentiment_score = analyze_sentiment(feedback_dict['comment'])
    feedback_dict['sentiment_score'] = sentiment_score
    
    feedback_obj = Feedback(**feedback_dict)
    
    # Insert into database
    result = await db.feedback.insert_one(feedback_obj.dict())
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create feedback")
    
    return feedback_obj

@api_router.get("/feedback", response_model=List[Feedback])
async def get_all_feedback():
    """Get all feedback entries"""
    feedback_list = await db.feedback.find().to_list(1000)
    return [Feedback(**feedback) for feedback in feedback_list]

@api_router.get("/feedback/stats", response_model=FeedbackStats)
async def get_feedback_stats():
    """Get comprehensive feedback statistics for 3D visualization"""
    # Get all feedback
    all_feedback = await db.feedback.find().to_list(1000)
    
    if not all_feedback:
        return FeedbackStats(
            total_feedback=0,
            avg_rating=0.0,
            category_breakdown={},
            rating_distribution={},
            recent_feedback=[]
        )
    
    feedback_objects = [Feedback(**feedback) for feedback in all_feedback]
    
    # Calculate statistics
    total_feedback = len(feedback_objects)
    avg_rating = sum(f.rating for f in feedback_objects) / total_feedback
    
    # Category breakdown
    category_breakdown = {}
    for category in FeedbackCategory:
        category_feedback = [f for f in feedback_objects if f.category == category]
        if category_feedback:
            category_breakdown[category.value] = {
                'count': len(category_feedback),
                'avg_rating': sum(f.rating for f in category_feedback) / len(category_feedback),
                'avg_sentiment': sum(f.sentiment_score or 0 for f in category_feedback) / len(category_feedback)
            }
    
    # Rating distribution
    rating_distribution = {}
    for rating in range(1, 6):
        count = len([f for f in feedback_objects if f.rating == rating])
        rating_distribution[str(rating)] = count
    
    # Recent feedback (last 10)
    recent_feedback = sorted(feedback_objects, key=lambda x: x.timestamp, reverse=True)[:10]
    
    return FeedbackStats(
        total_feedback=total_feedback,
        avg_rating=avg_rating,
        category_breakdown=category_breakdown,
        rating_distribution=rating_distribution,
        recent_feedback=recent_feedback
    )

@api_router.get("/feedback/category/{category}")
async def get_feedback_by_category(category: FeedbackCategory):
    """Get feedback by specific category"""
    feedback_list = await db.feedback.find({"category": category.value}).to_list(1000)
    return [Feedback(**feedback) for feedback in feedback_list]

@api_router.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: str):
    """Delete a feedback entry"""
    result = await db.feedback.delete_one({"id": feedback_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()