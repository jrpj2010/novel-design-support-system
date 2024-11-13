from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.services.novel_service import NovelService
from app.schemas.novel import (
    Novel,
    NovelCreate,
    NovelUpdate,
    NovelTemplate,
    Message
)
from app.core.dependencies import get_novel_service

router = APIRouter(
    prefix="/novels",
    tags=["novels"]
)

class NovelController:
    def __init__(self, novel_service: NovelService = Depends(get_novel_service)):
        self.novel_service = novel_service

    async def create_novel(self, novel_data: NovelCreate) -> Novel:
        """
        新しい小説を作成する
        
        Args:
            novel_data: 作成する小説のデータ
            
        Returns:
            作成された小説のデータ
            
        Raises:
            HTTPException: 作成に失敗した場合
        """
        try:
            return await self.novel_service.create_novel(novel_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_novel(self, novel_id: str) -> Novel:
        """
        指定されたIDの小説を取得する
        
        Args:
            novel_id: 取得する小説のID
            
        Returns:
            小説のデータ
            
        Raises:
            HTTPException: 小説が見つからない場合
        """
        novel = await self.novel_service.get_novel(novel_id)
        if not novel:
            raise HTTPException(status_code=404, detail="Novel not found")
        return novel

    async def update_novel(self, novel_id: str, novel_data: NovelUpdate) -> Novel:
        """
        指定されたIDの小説を更新する
        
        Args:
            novel_id: 更新する小説のID
            novel_data: 更新データ
            
        Returns:
            更新された小説のデータ
            
        Raises:
            HTTPException: 更新に失敗した場合
        """
        try:
            novel = await self.novel_service.update_novel(novel_id, novel_data)
            if not novel:
                raise HTTPException(status_code=404, detail="Novel not found")
            return novel
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_novel(self, novel_id: str) -> Message:
        """
        指定されたIDの小説を削除する
        
        Args:
            novel_id: 削除する小説のID
            
        Returns:
            削除結果のメッセージ
            
        Raises:
            HTTPException: 削除に失敗した場合
        """
        try:
            result = await self.novel_service.delete_novel(novel_id)
            if not result:
                raise HTTPException(status_code=404, detail="Novel not found")
            return Message(message="Novel successfully deleted")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_templates(self) -> List[NovelTemplate]:
        """
        利用可能な小説テンプレートの一覧を取得する
        
        Returns:
            テンプレートのリスト
            
        Raises:
            HTTPException: テンプレート取得に失敗した場合
        """
        try:
            return await self.novel_service.get_templates()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# ルートの定義
novel_controller = NovelController()

@router.post("/create", response_model=Novel)
async def create_novel(novel_data: NovelCreate, controller: NovelController = Depends()):
    return await controller.create_novel(novel_data)

@router.get("/{novel_id}", response_model=Novel)
async def get_novel(novel_id: str, controller: NovelController = Depends()):
    return await controller.get_novel(novel_id)

@router.put("/{novel_id}", response_model=Novel)
async def update_novel(novel_id: str, novel_data: NovelUpdate, controller: NovelController = Depends()):
    return await controller.update_novel(novel_id, novel_data)

@router.delete("/{novel_id}", response_model=Message)
async def delete_novel(novel_id: str, controller: NovelController = Depends()):
    return await controller.delete_novel(novel_id)

@router.get("/templates", response_model=List[NovelTemplate])
async def get_templates(controller: NovelController = Depends()):
    return await controller.get_templates()