from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class NovelBase(BaseModel):
    """小説の基本スキーマ"""
    title: str = Field(..., min_length=1, max_length=200, description="小説のタイトル")
    description: Optional[str] = Field(None, max_length=2000, description="小説の説明")
    genre: Optional[str] = Field(None, description="小説のジャンル")
    status: str = Field("draft", description="小説の状態 (draft, published, archived)")
    is_public: bool = Field(False, description="公開状態")
    language: str = Field("ja", description="小説の言語")

class NovelCreate(NovelBase):
    """小説作成用スキーマ"""
    author_id: int = Field(..., description="作者のID")
    tags: Optional[List[str]] = Field(default=[], description="小説のタグ")

class NovelUpdate(BaseModel):
    """小説更新用スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    genre: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None

class NovelResponse(NovelBase):
    """小説レスポース用スキーマ"""
    id: int = Field(..., description="小説のID")
    author_id: int = Field(..., description="作者のID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    word_count: int = Field(0, description="総単語数")
    chapter_count: int = Field(0, description="章の数")
    tags: List[str] = Field(default=[], description="小説のタグ")
    average_rating: Optional[float] = Field(None, description="平均評価")
    view_count: int = Field(0, description="閲覧数")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "素晴らしい物語",
                "description": "心温まる冒険の物語",
                "author_id": 1,
                "genre": "ファンタジー",
                "status": "published",
                "is_public": True,
                "language": "ja",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "word_count": 50000,
                "chapter_count": 10,
                "tags": ["ファンタジー", "冒険"],
                "average_rating": 4.5,
                "view_count": 1000
            }
        }