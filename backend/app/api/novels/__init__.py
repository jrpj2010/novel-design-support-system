from fastapi import APIRouter
from typing import Dict, List, Optional
import yaml
import os
from pathlib import Path

from app.core.novel_engine import NovelEngine
from app.core.markdown_processor import MarkdownProcessor

# APIルーターの初期化
router = APIRouter()

class NovelConfig:
    """小説設定を管理するクラス"""
    
    def __init__(self):
        self.templates_path = Path("app/templates/novels")
        self.config: Dict = {}
        self.engine: Optional[NovelEngine] = None
        self.markdown_processor: Optional[MarkdownProcessor] = None

    def load_config(self, config_path: str) -> Dict:
        """設定ファイルを読み込む"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            return self.config
        except Exception as e:
            raise Exception(f"Failed to load novel config: {str(e)}")

    def initialize_engine(self) -> None:
        """NovelEngineの初期化"""
        self.engine = NovelEngine(self.config)
        self.markdown_processor = MarkdownProcessor()

def load_novel_templates() -> List[Dict]:
    """
    小説テンプレートを読み込む
    Returns:
        List[Dict]: テンプレート情報のリスト
    """
    template_path = Path("app/templates/novels")
    templates = []
    
    try:
        for template_file in template_path.glob("*.yaml"):
            with open(template_file, 'r', encoding='utf-8') as f:
                template_data = yaml.safe_load(f)
                templates.append(template_data)
        return templates
    except Exception as e:
        raise Exception(f"Failed to load novel templates: {str(e)}")

def validate_novel_structure(novel_data: Dict) -> bool:
    """
    小説構造を検証する
    Args:
        novel_data (Dict): 検証する小説データ
    Returns:
        bool: 検証結果
    """
    required_fields = [
        "title",
        "author",
        "chapters",
        "characters",
        "plot",
        "world_building"
    ]
    
    return all(field in novel_data for field in required_fields)

def initialize_novel_system() -> NovelConfig:
    """
    小説システムを初期化する
    Returns:
        NovelConfig: 初期化された小説設定オブジェクト
    """
    try:
        novel_config = NovelConfig()
        novel_config.load_config("app/config/novel_system.yaml")
        novel_config.initialize_engine()
        
        # テンプレートの読み込みを確認
        load_novel_templates()
        
        return novel_config
    except Exception as e:
        raise Exception(f"Failed to initialize novel system: {str(e)}")

# エンドポイントのインポート
from .endpoints import plots, characters, chapters, world_building

# ルーターにエンドポイントを登録
router.include_router(plots.router, prefix="/plots", tags=["plots"])
router.include_router(characters.router, prefix="/characters", tags=["characters"])
router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
router.include_router(world_building.router, prefix="/world-building", tags=["world-building"])