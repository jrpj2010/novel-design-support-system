from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
import json
import os
from pydantic import BaseModel, validator
from pathlib import Path

# ルーターの初期化
router = APIRouter()

class CharacterConfig(BaseModel):
    """キャラクター設定を管理するクラス"""
    name: str
    age: Optional[int]
    description: str
    personality: Dict[str, str]
    relationships: Dict[str, str]
    background: str
    attributes: Dict[str, any]

    class Config:
        schema_extra = {
            "example": {
                "name": "主人公",
                "age": 25,
                "description": "物語の主人公",
                "personality": {
                    "性格": "明るい",
                    "特徴": "正義感が強い"
                },
                "relationships": {},
                "background": "幼少期からの背景...",
                "attributes": {}
            }
        }

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('名前は空にできません')
        return v.strip()

def load_character_templates() -> Dict[str, CharacterConfig]:
    """
    キャラクターテンプレートを読み込む
    
    Returns:
        Dict[str, CharacterConfig]: テンプレート名とその設定のマッピング
    """
    template_path = Path(__file__).parent / "templates"
    templates = {}
    
    try:
        if template_path.exists():
            for template_file in template_path.glob("*.json"):
                with open(template_file, "r", encoding="utf-8") as f:
                    template_data = json.load(f)
                    templates[template_file.stem] = CharacterConfig(**template_data)
    except Exception as e:
        print(f"テンプレート読み込みエラー: {str(e)}")
        
    return templates

def validate_character_data(character_data: dict) -> bool:
    """
    キャラクターデータを検証する
    
    Args:
        character_data (dict): 検証するキャラクターデータ
        
    Returns:
        bool: 検証結果
        
    Raises:
        HTTPException: データが無効な場合
    """
    try:
        CharacterConfig(**character_data)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"キャラクターデータが無効です: {str(e)}"
        )

# グローバル変数としてテンプレートを保持
character_templates = load_character_templates()

# 依存性注入用の関数
async def get_character_templates():
    return character_templates

# エンドポイントの例
@router.get("/templates")
async def get_templates(
    templates: Dict[str, CharacterConfig] = Depends(get_character_templates)
):
    """利用可能なキャラクターテンプレートを取得する"""
    return templates

@router.post("/validate")
async def validate_character(character_data: dict):
    """キャラクターデータを検証する"""
    return {"valid": validate_character_data(character_data)}