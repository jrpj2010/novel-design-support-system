from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class WorldBase(BaseModel):
    """世界観の基本スキーマ"""
    title: str = Field(..., min_length=1, max_length=200, description="世界観のタイトル")
    description: str = Field(..., min_length=1, description="世界観の詳細な説明")
    time_period: Optional[str] = Field(None, description="物語の時代設定")
    geography: Optional[str] = Field(None, description="地理的な設定")
    culture: Optional[str] = Field(None, description="文化的な背景")
    magic_system: Optional[str] = Field(None, description="魔法システムの説明（ファンタジーの場合）")
    technology_level: Optional[str] = Field(None, description="技術レベルの説明")
    social_structure: Optional[str] = Field(None, description="社会構造の説明")
    rules_and_laws: Optional[str] = Field(None, description="世界のルールや法則")
    
class WorldCreate(WorldBase):
    """世界観作成スキーマ"""
    project_id: int = Field(..., description="関連するプロジェクトのID")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "魔法世界エターナル",
                "description": "魔法と科学が共存する未来世界",
                "time_period": "近未来",
                "geography": "浮遊する都市群",
                "culture": "魔法と科学の融合文化",
                "magic_system": "エーテル魔法システム",
                "technology_level": "高度なAI社会",
                "social_structure": "魔法使いと科学者の階級社会",
                "rules_and_laws": "魔法使用に関する規制法",
                "project_id": 1
            }
        }

class WorldUpdate(WorldBase):
    """世界観更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "魔法世界エターナル - 改訂版",
                "description": "魔法と科学が共存する未来世界の詳細な設定",
                "time_period": "近未来（2250年）",
                "geography": "浮遊する都市群と地上の古代遺跡",
                "culture": "魔法と科学の融合文化、新たな宗教の台頭",
                "magic_system": "改良型エーテル魔法システム",
                "technology_level": "超高度なAI社会",
                "social_structure": "魔法使いと科学者の協調社会",
                "rules_and_laws": "改正魔法規制法",
                "updated_at": "2024-01-01T00:00:00"
            }
        }

class WorldInDB(WorldBase):
    """データベースに保存される世界観スキーマ"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True