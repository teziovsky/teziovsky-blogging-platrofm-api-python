from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
