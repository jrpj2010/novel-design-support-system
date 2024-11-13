from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# キャラクター間の関係性を表す中間テーブル
character_relationships = Table(
    'character_relationships',
    Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('related_character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('relationship_type_id', Integer, ForeignKey('relationships.id'))
)

class Character(Base):
    """キャラクターモデル"""
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(50))
    occupation = Column(String(100))
    physical_description = Column(Text)
    personality = Column(Text)
    background = Column(Text)
    motivation = Column(Text)
    role_in_story = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 関係性の定義
    relationships = relationship(
        'Character',
        secondary=character_relationships,
        primaryjoin=(character_relationships.c.character_id == id),
        secondaryjoin=(character_relationships.c.related_character_id == id),
        backref='related_to'
    )

    def __repr__(self):
        return f"<Character(name='{self.name}', role='{self.role_in_story}')>"

class Relationship(Base):
    """関係性モデル"""
    __tablename__ = 'relationships'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 例: 友人、恋人、家族、敵対者など
    description = Column(Text)
    intensity = Column(Integer)  # 関係性の強さ（1-10など）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Relationship(name='{self.name}', intensity={self.intensity})>"

    @property
    def relationship_strength(self):
        """関係性の強さを文字列で返す"""
        if self.intensity <= 3:
            return "弱い"
        elif self.intensity <= 7:
            return "普通"
        else:
            return "強い"