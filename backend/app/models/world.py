from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional

from .base import Base

class World(Base):
    """世界観全体を表すモデル"""
    __tablename__ = 'worlds'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    elements = relationship("WorldElement", back_populates="world", cascade="all, delete-orphan")
    
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def add_element(self, element: "WorldElement") -> None:
        """世界要素を追加するメソッド"""
        self.elements.append(element)

    def remove_element(self, element: "WorldElement") -> None:
        """世界要素を削除するメソッド"""
        self.elements.remove(element)

    def get_elements_by_category(self, category: str) -> List["WorldElement"]:
        """カテゴリーによる世界要素の取得"""
        return [element for element in self.elements if element.category == category]


class WorldElement(Base):
    """世界の構成要素を表すモデル"""
    __tablename__ = 'world_elements'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)  # 地理、文化、歴史など
    details = Column(Text)
    world_id = Column(Integer, ForeignKey('worlds.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    world = relationship("World", back_populates="elements")

    def __init__(self, name: str, category: str, description: Optional[str] = None, 
                 details: Optional[str] = None):
        self.name = name
        self.category = category
        self.description = description
        self.details = details

    def update(self, name: Optional[str] = None, category: Optional[str] = None,
              description: Optional[str] = None, details: Optional[str] = None) -> None:
        """要素の情報を更新するメソッド"""
        if name:
            self.name = name
        if category:
            self.category = category
        if description:
            self.description = description
        if details:
            self.details = details
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """要素の情報を辞書形式で返すメソッド"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'details': self.details,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }