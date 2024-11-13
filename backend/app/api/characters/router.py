from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import character_service
from app.schemas import character as character_schemas
from app.core.security import get_current_user

router = APIRouter(
    prefix="/characters",
    tags=["characters"]
)

@router.post("/create", response_model=character_schemas.Character)
async def create_character(
    character: character_schemas.CharacterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    新しいキャラクターを作成する
    """
    try:
        return await character_service.create_character(db, character, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{character_id}", response_model=character_schemas.Character)
async def get_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    指定されたIDのキャラクター情報を取得する
    """
    character = await character_service.get_character(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this character")
    return character

@router.put("/{character_id}", response_model=character_schemas.Character)
async def update_character(
    character_id: int,
    character_update: character_schemas.CharacterUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    指定されたIDのキャラクター情報を更新する
    """
    existing_character = await character_service.get_character(db, character_id)
    if not existing_character:
        raise HTTPException(status_code=404, detail="Character not found")
    if existing_character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this character")
    
    try:
        return await character_service.update_character(db, character_id, character_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{character_id}")
async def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    指定されたIDのキャラクターを削除する
    """
    existing_character = await character_service.get_character(db, character_id)
    if not existing_character:
        raise HTTPException(status_code=404, detail="Character not found")
    if existing_character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this character")
    
    await character_service.delete_character(db, character_id)
    return {"message": "Character successfully deleted"}

@router.get("/list/{novel_id}", response_model=List[character_schemas.Character])
async def list_characters(
    novel_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    指定された小説に関連するすべてのキャラクターを取得する
    """
    try:
        characters = await character_service.get_characters_by_novel(db, novel_id, current_user.id)
        return characters
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))