from fastapi import APIRouter, Query
from database import get_db
from models import RatingOut, RatingStats
from typing import Optional, List

router = APIRouter(prefix="/api/ratings", tags=["ratings"])


@router.get("", response_model=List[RatingOut])
def get_ratings(
    sort: Optional[str] = Query(None, description="rating_high, rating_low, reviews_count"),
):
    conn = get_db()
    query = """
        SELECT p.id as product_id, p.name as product_name, p.image_url,
            c.name as category_name, b.name as brand_name,
            COALESCE(AVG(r.rating), 0) as avg_rating,
            COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON r.product_id = p.id
        GROUP BY p.id
        HAVING review_count > 0
    """

    if sort == "rating_low":
        query += " ORDER BY avg_rating ASC"
    elif sort == "reviews_count":
        query += " ORDER BY review_count DESC"
    else:
        query += " ORDER BY avg_rating DESC"

    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/stats", response_model=RatingStats)
def get_stats():
    conn = get_db()

    total_products = conn.execute("SELECT COUNT(*) as c FROM products").fetchone()["c"]
    total_reviews = conn.execute("SELECT COUNT(*) as c FROM reviews").fetchone()["c"]
    overall_avg = conn.execute("SELECT COALESCE(AVG(rating), 0) as avg FROM reviews").fetchone()["avg"]

    dist_rows = conn.execute(
        "SELECT rating, COUNT(*) as count FROM reviews GROUP BY rating ORDER BY rating"
    ).fetchall()
    rating_distribution = {str(i): 0 for i in range(1, 6)}
    for row in dist_rows:
        rating_distribution[str(row["rating"])] = row["count"]

    top = conn.execute("""
        SELECT p.id as product_id, p.name as product_name, p.image_url,
            c.name as category_name, b.name as brand_name,
            AVG(r.rating) as avg_rating, COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        JOIN reviews r ON r.product_id = p.id
        GROUP BY p.id
        ORDER BY avg_rating DESC
        LIMIT 5
    """).fetchall()

    worst = conn.execute("""
        SELECT p.id as product_id, p.name as product_name, p.image_url,
            c.name as category_name, b.name as brand_name,
            AVG(r.rating) as avg_rating, COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        JOIN reviews r ON r.product_id = p.id
        GROUP BY p.id
        ORDER BY avg_rating ASC
        LIMIT 5
    """).fetchall()

    conn.close()

    return {
        "total_products": total_products,
        "total_reviews": total_reviews,
        "overall_avg_rating": round(overall_avg, 2),
        "rating_distribution": rating_distribution,
        "top_products": [dict(r) for r in top],
        "worst_products": [dict(r) for r in worst],
    }
