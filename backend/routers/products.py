from fastapi import APIRouter, Query, HTTPException
from database import get_db
from models import ProductOut, ProductCreate, ProductUpdate, ProductImageOut
from typing import Optional, List

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[ProductOut])
def get_products(
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    sort: Optional[str] = Query(None, description="price_asc, price_desc, rating, newest"),
):
    conn = get_db()
    query = """
        SELECT p.*,
            c.name as category_name,
            b.name as brand_name,
            COALESCE(AVG(r.rating), 0) as avg_rating,
            COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON r.product_id = p.id
    """
    conditions = []
    params = []

    if category_id:
        conditions.append("p.category_id = ?")
        params.append(category_id)
    if brand_id:
        conditions.append("p.brand_id = ?")
        params.append(brand_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY p.id"

    if sort == "price_asc":
        query += " ORDER BY p.price ASC"
    elif sort == "price_desc":
        query += " ORDER BY p.price DESC"
    elif sort == "rating":
        query += " ORDER BY avg_rating DESC"
    elif sort == "newest":
        query += " ORDER BY p.created_at DESC"
    else:
        query += " ORDER BY p.id"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{product_id}")
def get_product(product_id: int):
    conn = get_db()

    row = conn.execute("""
        SELECT p.*,
            c.name as category_name,
            b.name as brand_name,
            COALESCE(AVG(r.rating), 0) as avg_rating,
            COUNT(r.id) as review_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON r.product_id = p.id
        WHERE p.id = ?
        GROUP BY p.id
    """, (product_id,)).fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    product = dict(row)

    # Get images
    images = conn.execute(
        "SELECT * FROM product_images WHERE product_id = ? ORDER BY is_main DESC",
        (product_id,)
    ).fetchall()
    product["images"] = [dict(img) for img in images]

    # Get reviews
    reviews = conn.execute("""
        SELECT r.*, rv.name as reviewer_name, rv.avatar_url as reviewer_avatar,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 1) as helpful_count,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 0) as not_helpful_count
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        WHERE r.product_id = ?
        ORDER BY r.created_at DESC
    """, (product_id,)).fetchall()
    product["reviews"] = [dict(rev) for rev in reviews]

    # Rating distribution
    dist = conn.execute("""
        SELECT rating, COUNT(*) as count
        FROM reviews WHERE product_id = ?
        GROUP BY rating ORDER BY rating
    """, (product_id,)).fetchall()
    product["rating_distribution"] = {str(i): 0 for i in range(1, 6)}
    for d in dist:
        product["rating_distribution"][str(d["rating"])] = d["count"]

    conn.close()
    return product


@router.post("")
def create_product(product: ProductCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO products (name, description, price, image_url, category_id, brand_id) VALUES (?, ?, ?, ?, ?, ?)",
        (product.name, product.description, product.price, product.image_url, product.category_id, product.brand_id),
    )
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return {"id": product_id, "message": "Product created"}


@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    conn = get_db()
    existing = conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    updates = []
    params = []
    for field, value in product.model_dump(exclude_unset=True).items():
        if value is not None:
            updates.append(f"{field} = ?")
            params.append(value)

    if updates:
        params.append(product_id)
        conn.execute(f"UPDATE products SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()

    conn.close()
    return {"message": "Product updated"}


@router.delete("/{product_id}")
def delete_product(product_id: int):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"message": "Product deleted"}
