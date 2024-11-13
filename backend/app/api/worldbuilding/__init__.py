from fastapi import APIRouter, Depends
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

# Core world engine importを想定
from app.core.world_engine import WorldEngine
from app.core.auth import get_current_user
from app.core.models import User

router = APIRouter(
    prefix="/worldbuilding",
    tags=["worldbuilding"],
    responses={404: {"description": "Not found"}},
)

class WorldConfig(BaseModel):
    """世界観設定を管理するためのモデル"""
    id: Optional[int]
    title: str
    description: str
    rules: Dict[str, str]
    physical_laws: Dict[str, str]
    magic_system: Optional[Dict[str, str]]
    technology_level: str
    cultural_systems: List[Dict[str, str]]
    historical_events: List[Dict[str, str]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class WorldConfigCreate(BaseModel):
    """世界観設定作成用のモデル"""
    title: str
    description: str
    rules: Dict[str, str]
    physical_laws: Dict[str, str]
    magic_system: Optional[Dict[str, str]]
    technology_level: str
    cultural_systems: List[Dict[str, str]]
    historical_events: List[Dict[str, str]]

@router.get("/configs/", response_model=List[WorldConfig])
async def get_world_configs(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    ユーザーの世界観設定一覧を取得
    """
    world_engine = WorldEngine()
    return await world_engine.get_user_world_configs(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.post("/configs/", response_model=WorldConfig)
async def create_world_config(
    config: WorldConfigCreate,
    current_user: User = Depends(get_current_user)
):
    """
    新しい世界観設定を作成
    """
    world_engine = WorldEngine()
    return await world_engine.create_world_config(
        user_id=current_user.id,
        config=config
    )

@router.get("/configs/{config_id}", response_model=WorldConfig)
async def get_world_config(
    config_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    特定の世界観設定を取得
    """
    world_engine = WorldEngine()
    return await world_engine.get_world_config(
        user_id=current_user.id,
        config_id=config_id
    )

@router.put("/configs/{config_id}", response_model=WorldConfig)
async def update_world_config(
    config_id: int,
    config: WorldConfigCreate,
    current_user: User = Depends(get_current_user)
):
    """
    世界観設定を更新
    """
    world_engine = WorldEngine()
    return await world_engine.update_world_config(
        user_id=current_user.id,
        config_id=config_id,
        config=config
    )

@router.delete("/configs/{config_id}")
async def delete_world_config(
    config_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    世界観設定を削除
    """
    world_engine = WorldEngine()
    return await world_engine.delete_world_config(
        user_id=current_user.id,
        config_id=config_id
    )