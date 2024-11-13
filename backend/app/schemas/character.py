from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class CharacterRole(str, Enum):
    """キャラクターの役割を定義する列挙型"""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    SUPPORTING = "supporting"
    MINOR = "minor"

class CharacterBase(BaseModel):
    """キャラクターの基本属性を定義する基底クラス"""
    name: str = Field(..., min_length=1, max_length=100, description="キャラクターの名前")
    age: Optional[int] = Field(None, ge=0, le=1000, description="キャラクターの年齢")
    role: CharacterRole = Field(..., description="キャラクターの役割")
    description: str = Field(..., min_length=1, max_length=2000, description="キャラクターの説明")
    personality: Optional[str] = Field(None, max_length=1000, description="キャラクターの性格")
    background: Optional[str] = Field(None, max_length=2000, description="キャラクターの背景")
    goals: Optional[str] = Field(None, max_length=1000, description="キャラクターの目標")
    relationships: Optional[dict[str, str]] = Field(
        default_factory=dict,
        description="他のキャラクターとの関係性"
    )

class CharacterCreate(CharacterBase):
    """キャラクター作成用のスキーマ"""
    created_by: str = Field(..., description="作成者のID")

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 25,
                "role": "protagonist",
                "description": "主人公の詳細な説明",
                "personality": "勇敢で正義感が強い",
                "background": "幼少期からの背景",
                "goals": "世界の平和を守ること",
                "relationships": {
                    "Mary Smith": "親友",
                    "Dr. Evil": "宿敵"
                },
                "created_by": "user123"
            }
        }

class CharacterUpdate(BaseModel):
    """キャラクター更新用のスキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=1000)
    role: Optional[CharacterRole] = None
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    personality: Optional[str] = Field(None, max_length=1000)
    background: Optional[str] = Field(None, max_length=2000)
    goals: Optional[str] = Field(None, max_length=1000)
    relationships: Optional[dict[str, str]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe Updated",
                "age": 26,
                "description": "更新された主人公の説明",
                "relationships": {
                    "Mary Smith": "親友",
                    "Dr. Evil": "宿敵",
                    "New Character": "同僚"
                }
            }
        }

class CharacterInDB(CharacterBase):
    """データベースに保存されるキャラクターモデル"""
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        orm_mode = True