from typing import Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel

class Character(BaseModel):
    """キャラクターを表すPydanticモデル"""
    id: str
    name: str
    age: Optional[int]
    gender: Optional[str]
    personality: Optional[Dict[str, float]]
    background: Optional[str]
    appearance: Optional[Dict[str, str]]
    skills: Optional[List[str]]
    relationships: Optional[Dict[str, Dict[str, float]]]
    created_at: datetime
    updated_at: datetime

class CharacterEngine:
    """キャラクター管理エンジンクラス"""

    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self.relationship_types = {
            "friendship": (0.0, 1.0),
            "rivalry": (-1.0, 1.0),
            "romance": (0.0, 1.0),
            "family": (0.0, 1.0),
            "mentor": (0.0, 1.0)
        }

    async def create_character(
        self,
        name: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        personality: Optional[Dict[str, float]] = None,
        background: Optional[str] = None,
        appearance: Optional[Dict[str, str]] = None,
        skills: Optional[List[str]] = None
    ) -> Character:
        """
        新しいキャラクターを作成する

        Args:
            name: キャラクターの名前
            age: キャラクターの年齢
            gender: キャラクターの性別
            personality: パーソナリティ特性の辞書
            background: 経歴
            appearance: 外見の特徴
            skills: スキルのリスト

        Returns:
            作成されたCharacterオブジェクト
        """
        from uuid import uuid4
        
        character_id = str(uuid4())
        now = datetime.utcnow()
        
        character = Character(
            id=character_id,
            name=name,
            age=age,
            gender=gender,
            personality=personality or {},
            background=background,
            appearance=appearance or {},
            skills=skills or [],
            relationships={},
            created_at=now,
            updated_at=now
        )
        
        self.characters[character_id] = character
        return character

    async def analyze_relationships(
        self,
        character_id: str,
        target_character_id: Optional[str] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        キャラクター間の関係性を分析する

        Args:
            character_id: 分析対象のキャラクターID
            target_character_id: 特定の相手キャラクターID（省略可）

        Returns:
            関係性分析の結果
        """
        if character_id not in self.characters:
            raise ValueError(f"Character with ID {character_id} not found")

        character = self.characters[character_id]
        relationships = character.relationships or {}

        if target_character_id:
            if target_character_id not in self.characters:
                raise ValueError(f"Target character with ID {target_character_id} not found")
            
            # 特定のキャラクターとの関係性のみを返す
            return {
                target_character_id: relationships.get(target_character_id, 
                    {k: 0.0 for k in self.relationship_types.keys()})
            }

        # すべてのキャラクターとの関係性を分析
        analysis_results = {}
        for other_id, other_char in self.characters.items():
            if other_id == character_id:
                continue

            # 既存の関係性を取得するか、デフォルト値を設定
            current_relationship = relationships.get(other_id, 
                {k: 0.0 for k in self.relationship_types.keys()})
            
            # 関係性の相互参照を考慮した分析
            other_relationship = other_char.relationships.get(character_id, {})
            
            # 双方向の関係性を平均化して分析
            analyzed_relationship = {}
            for rel_type in self.relationship_types:
                val1 = current_relationship.get(rel_type, 0.0)
                val2 = other_relationship.get(rel_type, 0.0)
                analyzed_relationship[rel_type] = (val1 + val2) / 2

            analysis_results[other_id] = analyzed_relationship

        return analysis_results

    def update_relationship(
        self,
        character_id: str,
        target_character_id: str,
        relationship_type: str,
        value: float
    ) -> None:
        """
        キャラクター間の関係性を更新する

        Args:
            character_id: キャラクターID
            target_character_id: 対象キャラクターID
            relationship_type: 関係性の種類
            value: 関係性の値
        """
        if relationship_type not in self.relationship_types:
            raise ValueError(f"Invalid relationship type: {relationship_type}")

        min_val, max_val = self.relationship_types[relationship_type]
        if not min_val <= value <= max_val:
            raise ValueError(f"Value must be between {min_val} and {max_val}")

        character = self.characters[character_id]
        if character.relationships is None:
            character.relationships = {}
        
        if target_character_id not in character.relationships:
            character.relationships[target_character_id] = {}
            
        character.relationships[target_character_id][relationship_type] = value
        character.updated_at = datetime.utcnow()