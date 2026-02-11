from fastapi import APIRouter, Query, HTTPException
from database import get_db
from models import ReviewOut, ReviewCreate, VoteCreate
from typing import Optional, List

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.get("", response_model=List[ReviewOut])
def get_reviews(
    product_id: Optional[int] = None,
    rating: Optional[int] = None,
    sort: Optional[str] = Query(None, description="newest, oldest, rating_high, rating_low, helpful"),
    limit: int = 100,
    offset: int = 0,
):
    conn = get_db()
    query = """
        SELECT r.*, rv.name as reviewer_name, rv.avatar_url as reviewer_avatar,
            p.name as product_name,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 1) as helpful_count,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 0) as not_helpful_count
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        JOIN products p ON r.product_id = p.id
    """
    conditions = []
    params = []

    if product_id:
        conditions.append("r.product_id = ?")
        params.append(product_id)
    if rating:
        conditions.append("r.rating = ?")
        params.append(rating)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort == "newest":
        query += " ORDER BY r.created_at DESC"
    elif sort == "oldest":
        query += " ORDER BY r.created_at ASC"
    elif sort == "rating_high":
        query += " ORDER BY r.rating DESC"
    elif sort == "rating_low":
        query += " ORDER BY r.rating ASC"
    elif sort == "helpful":
        query += " ORDER BY helpful_count DESC"
    else:
        query += " ORDER BY r.created_at DESC"

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int):
    conn = get_db()
    row = conn.execute("""
        SELECT r.*, rv.name as reviewer_name, rv.avatar_url as reviewer_avatar,
            p.name as product_name,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 1) as helpful_count,
            (SELECT COUNT(*) FROM review_votes WHERE review_id = r.id AND is_helpful = 0) as not_helpful_count
        FROM reviews r
        JOIN reviewers rv ON r.reviewer_id = rv.id
        JOIN products p ON r.product_id = p.id
        WHERE r.id = ?
    """, (review_id,)).fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Review not found")

    conn.close()
    return dict(row)


@router.post("")
def create_review(review: ReviewCreate):
    conn = get_db()

    # Find or create reviewer
    existing = conn.execute(
        "SELECT id FROM reviewers WHERE name = ?", (review.reviewer_name,)
    ).fetchone()

    if existing:
        reviewer_id = existing["id"]
    else:
        cursor = conn.execute(
            "INSERT INTO reviewers (name, email) VALUES (?, ?)",
            (review.reviewer_name, review.reviewer_email),
        )
        reviewer_id = cursor.lastrowid

    cursor = conn.execute(
        "INSERT INTO reviews (product_id, reviewer_id, rating, title, text, pros, cons) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (review.product_id, reviewer_id, review.rating, review.title, review.text, review.pros, review.cons),
    )
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return {"id": review_id, "message": "Review created"}


@router.delete("/{review_id}")
def delete_review(review_id: int):
    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    return {"message": "Review deleted"}


@router.post("/{review_id}/vote")
def vote_review(review_id: int, vote: VoteCreate):
    conn = get_db()
    conn.execute(
        "INSERT INTO review_votes (review_id, is_helpful) VALUES (?, ?)",
        (review_id, 1 if vote.is_helpful else 0),
    )
    conn.commit()
    conn.close()
    return {"message": "Vote recorded"}
