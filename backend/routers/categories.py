from fastapi import APIRouter
from database import get_db
from models import CategoryOut, BrandOut
from typing import List

router = APIRouter(prefix="/api", tags=["categories & brands"])


@router.get("/categories", response_model=List[CategoryOut])
def get_categories():
    conn = get_db()
    rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/brands", response_model=List[BrandOut])
def get_brands():
    conn = get_db()
    rows = conn.execute("SELECT * FROM brands ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]
