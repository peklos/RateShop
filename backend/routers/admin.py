from fastapi import APIRouter, HTTPException
from database import get_db
from models import AdminLogin, AdminOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login")
def admin_login(creds: AdminLogin):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM admin_users WHERE username = ? AND password = ?",
        (creds.username, creds.password),
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"id": row["id"], "username": row["username"], "role": row["role"]}


@router.get("/reviews")
def get_all_reviews_admin():
    conn = get_db()
    rows = conn.execute("""
        SELECT r.*, rv.name as reviewer_name, rv.email as reviewer_email,
            p.name as product_name,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 1) as helpful_count,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 0) as not_helpful_count
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        JOIN products p ON r.product_id = p.id
        ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.delete("/reviews/{review_id}")
def delete_review_admin(review_id: int):
    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    return {"message": "Review deleted"}


@router.get("/stats")
def get_admin_stats():
    conn = get_db()
    products_count = conn.execute("SELECT COUNT(*) as c FROM products").fetchone()["c"]
    reviews_count = conn.execute("SELECT COUNT(*) as c FROM reviews").fetchone()["c"]
    reviewers_count = conn.execute("SELECT COUNT(*) as c FROM reviewers").fetchone()["c"]
    avg_rating = conn.execute("SELECT COALESCE(AVG(rating), 0) as avg FROM reviews").fetchone()["avg"]

    recent_reviews = conn.execute("""
        SELECT r.*, rv.name as reviewer_name, p.name as product_name
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        JOIN products p ON r.product_id = p.id
        ORDER BY r.created_at DESC LIMIT 10
    """).fetchall()

    conn.close()
    return {
        "products_count": products_count,
        "reviews_count": reviews_count,
        "reviewers_count": reviewers_count,
        "avg_rating": round(avg_rating, 2),
        "recent_reviews": [dict(r) for r in recent_reviews],
    }


@router.get("/products")
def get_all_products_admin():
    conn = get_db()
    rows = conn.execute("""
        SELECT p.*, c.name as category_name, b.name as brand_name,
            COALESCE(AVG(r.rating), 0) as avg_rating,
            COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON r.product_id = p.id
        GROUP BY p.id
        ORDER BY p.id
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/categories")
def get_categories_admin():
    conn = get_db()
    rows = conn.execute("""
        SELECT c.*, COUNT(p.id) as products_count
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id
        GROUP BY c.id
        ORDER BY c.name
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/brands")
def get_brands_admin():
    conn = get_db()
    rows = conn.execute("""
        SELECT b.*, COUNT(p.id) as products_count
        FROM brands b
        LEFT JOIN products p ON p.brand_id = b.id
        GROUP BY b.id
        ORDER BY b.name
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]
