from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.world import World, WorldElement
from app.schemas.world import (
    WorldCreate,
    WorldUpdate,
    WorldResponse,
    WorldElementResponse
)
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/worlds",
    tags=["worldbuilding"]
)

@router.post("/create", response_model=WorldResponse)
async def create_world(
    world: WorldCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    新しい世界観設定を作成するエンドポイント
    """
    try:
        db_world = World(
            title=world.title,
            description=world.description,
            rules=world.rules,
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        db.add(db_world)
        db.commit()
        db.refresh(db_world)
        return db_world
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"世界観の作成中にエラーが発生しました: {str(e)}"
        )

@router.get("/{world_id}", response_model=WorldResponse)
async def get_world(
    world_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    指定されたIDの世界観設定を取得するエンドポイント
    """
    world = db.query(World).filter(
        World.id == world_id,
        World.created_by == current_user.id
    ).first()
    
    if not world:
        raise HTTPException(
            status_code=404,
            detail="指定された世界観が見つかりません"
        )
    
    return world

@router.put("/{world_id}", response_model=WorldResponse)
async def update_world(
    world_id: int,
    world_update: WorldUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    指定されたIDの世界観設定を更新するエンドポイント
    """
    world = db.query(World).filter(
        World.id == world_id,
        World.created_by == current_user.id
    ).first()
    
    if not world:
        raise HTTPException(
            status_code=404,
            detail="指定された世界観が見つかりません"
        )
    
    try:
        for key, value in world_update.dict(exclude_unset=True).items():
            setattr(world, key, value)
        
        world.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(world)
        return world
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"世界観の更新中にエラーが発生しました: {str(e)}"
        )

@router.get("/elements/{world_id}", response_model=List[WorldElementResponse])
async def get_world_elements(
    world_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    指定された世界観に関連する要素を取得するエンドポイント
    """
    world = db.query(World).filter(
        World.id == world_id,
        World.created_by == current_user.id
    ).first()
    
    if not world:
        raise HTTPException(
            status_code=404,
            detail="指定された世界観が見つかりません"
        )
    
    elements = db.query(WorldElement).filter(
        WorldElement.world_id == world_id
    ).all()
    
    return elements
