from fastapi import APIRouter, Query
from database import get_db
from typing import Optional

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(
    q: str = Query(..., description="Search query"),
    sort: Optional[str] = Query(None, description="relevance, price_asc, price_desc, rating, newest"),
    category_id: Optional[int] = None,
):
    conn = get_db()
    search_term = f"%{q}%"

    # Search products
    product_query = """
        SELECT p.*,
            c.name as category_name,
            b.name as brand_name,
            COALESCE(AVG(r.rating), 0) as avg_rating,
            COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON r.product_id = p.id
        WHERE (p.name LIKE ? OR p.description LIKE ?)
    """
    product_params = [search_term, search_term]

    if category_id:
        product_query += " AND p.category_id = ?"
        product_params.append(category_id)

    product_query += " GROUP BY p.id"

    if sort == "price_asc":
        product_query += " ORDER BY p.price ASC"
    elif sort == "price_desc":
        product_query += " ORDER BY p.price DESC"
    elif sort == "rating":
        product_query += " ORDER BY avg_rating DESC"
    elif sort == "newest":
        product_query += " ORDER BY p.created_at DESC"

    products = conn.execute(product_query, product_params).fetchall()

    # Search reviews
    review_query = """
        SELECT r.*, rv.name as reviewer_name, rv.avatar_url as reviewer_avatar,
            p.name as product_name,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 1) as helpful_count,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 0) as not_helpful_count
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        JOIN products p ON r.product_id = p.id
        WHERE r.title LIKE ? OR r.text LIKE ? OR r.pros LIKE ? OR r.cons LIKE ?
        ORDER BY r.created_at DESC
    """
    reviews = conn.execute(review_query, [search_term] * 4).fetchall()

    conn.close()

    return {
        "products": [dict(p) for p in products],
        "reviews": [dict(r) for r in reviews],
    }
