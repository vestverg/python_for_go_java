"""
Data models for the API.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    """User model."""
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

class Post(BaseModel):
    """Blog post model."""
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    author_id: int
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class Comment(BaseModel):
    """Comment model."""
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class PostCreate(BaseModel):
    """Model for creating a new post."""
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    tags: List[str] = Field(default_factory=list) 