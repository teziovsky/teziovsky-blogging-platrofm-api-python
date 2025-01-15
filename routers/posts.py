from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import models
from database.config import get_db
from schemas.post import Post, PostCreate

router = APIRouter()


@router.get("/posts", response_model=List[Post])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    term: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    db: Optional[Session] = None,
):
    db = db or Depends(get_db)()
    query = db.query(models.Post)

    if term:
        query = query.filter(
            or_(
                models.Post.title.ilike(f"%{term}%"),
                models.Post.content.ilike(f"%{term}%"),
                models.Post.category.ilike(f"%{term}%"),
            )
        )
    if category:
        query = query.filter(models.Post.category == category)
    if tag:
        query = query.filter(models.Post.tags.any(tag))

    posts = query.offset(skip).limit(limit).all()
    return posts


@router.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int, db: Optional[Session] = None):
    db = db or Depends(get_db)()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/posts", response_model=Post)
def create_post(post: PostCreate, db: Optional[Session] = None):
    db = db or Depends(get_db)()
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostCreate, db: Optional[Session] = None):
    db = db or Depends(get_db)()
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db_post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Optional[Session] = None):
    db = db or Depends(get_db)()
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
