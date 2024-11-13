from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from typing import List

from .database import Base

class NovelStatus(enum.Enum):
    """小説の状態を表す列挙型"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Novel(Base):
    """小説モデル"""
    __tablename__ = "novels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(NovelStatus), default=NovelStatus.DRAFT)
    genre = Column(String(100))
    target_word_count = Column(Integer)
    current_word_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")
    author = relationship("User", back_populates="novels")

    def update_word_count(self):
        """小説全体の単語数を更新"""
        total = sum(chapter.current_word_count for chapter in self.chapters)
        self.current_word_count = total

class Chapter(Base):
    """章モデル"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    description = Column(Text)
    current_word_count = Column(Integer, default=0)
    target_word_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    novel = relationship("Novel", back_populates="chapters")
    scenes = relationship("Scene", back_populates="chapter", cascade="all, delete-orphan")

    def update_word_count(self):
        """章の単語数を更新"""
        total = sum(scene.word_count for scene in self.scenes)
        self.current_word_count = total

class Scene(Base):
    """シーンモデル"""
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    order = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)
    pov_character = Column(String(255))  # POVキャラクター
    location = Column(String(255))  # シーンの舞台
    time_period = Column(String(255))  # シーンの時間設定
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    chapter = relationship("Chapter", back_populates="scenes")

    def calculate_word_count(self):
        """シーンの単語数を計算"""
        if self.content:
            self.word_count = len(self.content.split())
        else:
            self.word_count = 0