from pydantic import BaseModel
from typing import Optional, List


# --- Categories ---
class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None


# --- Brands ---
class BrandOut(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    logo_url: Optional[str] = None


# --- Products ---
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    created_at: Optional[str] = None
    avg_rating: Optional[float] = None
    review_count: Optional[int] = None
    category_name: Optional[str] = None
    brand_name: Optional[str] = None


class ProductImageOut(BaseModel):
    id: int
    product_id: int
    image_url: str
    is_main: int


# --- Reviewers ---
class ReviewerCreate(BaseModel):
    name: str
    email: Optional[str] = None


class ReviewerOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    registered_at: Optional[str] = None


# --- Reviews ---
class ReviewCreate(BaseModel):
    product_id: int
    reviewer_name: str
    reviewer_email: Optional[str] = None
    rating: int
    title: Optional[str] = None
    text: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None


class ReviewOut(BaseModel):
    id: int
    product_id: int
    reviewer_id: int
    rating: int
    title: Optional[str] = None
    text: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    created_at: Optional[str] = None
    is_verified: int = 0
    reviewer_name: Optional[str] = None
    reviewer_avatar: Optional[str] = None
    product_name: Optional[str] = None
    helpful_count: Optional[int] = 0
    not_helpful_count: Optional[int] = 0


# --- Votes ---
class VoteCreate(BaseModel):
    is_helpful: bool


# --- Admin ---
class AdminLogin(BaseModel):
    username: str
    password: str


class AdminOut(BaseModel):
    id: int
    username: str
    role: str


# --- Ratings ---
class RatingOut(BaseModel):
    product_id: int
    product_name: str
    avg_rating: float
    review_count: int
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    image_url: Optional[str] = None


class RatingStats(BaseModel):
    total_products: int
    total_reviews: int
    overall_avg_rating: float
    rating_distribution: dict
    top_products: List[RatingOut]
    worst_products: List[RatingOut]


# --- Search ---
class SearchResult(BaseModel):
    products: List[ProductOut]
    reviews: List[ReviewOut]
