from typing import Dict, List, Optional
from datetime import datetime
import logging
from pydantic import BaseModel

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlotElement(BaseModel):
    """プロット要素を表現するモデル"""
    id: str
    title: str
    description: str
    order: int
    chapter_id: Optional[str]
    created_at: datetime
    updated_at: datetime

class StoryStructure(BaseModel):
    """物語の構造を表現するモデル"""
    plot_elements: List[PlotElement]
    chapters: List[Dict]
    characters: List[Dict]
    world_building: Dict
    timeline: List[Dict]

class NovelEngine:
    """小説処理エンジンのメインクラス"""

    def __init__(self):
        self.structure: Optional[StoryStructure] = None
        self.consistency_rules = []
        self.validation_errors = []

    async def create_structure(self, 
                             plot_elements: List[Dict],
                             chapters: List[Dict],
                             characters: List[Dict],
                             world_building: Dict,
                             timeline: List[Dict]) -> StoryStructure:
        """
        小説の基本構造を作成する
        
        Args:
            plot_elements: プロット要素のリスト
            chapters: チャプター情報のリスト
            characters: キャラクター情報のリスト
            world_building: 世界観設定の辞書
            timeline: タイムライン情報のリスト
        
        Returns:
            StoryStructure: 作成された物語構造
        """
        try:
            self.structure = StoryStructure(
                plot_elements=[PlotElement(**elem) for elem in plot_elements],
                chapters=chapters,
                characters=characters,
                world_building=world_building,
                timeline=timeline
            )
            logger.info("Story structure created successfully")
            return self.structure
        except Exception as e:
            logger.error(f"Error creating story structure: {str(e)}")
            raise

    async def validate_plot(self) -> bool:
        """
        プロットの整合性を検証する
        
        Returns:
            bool: 検証結果（True: 有効, False: 無効）
        """
        if not self.structure:
            raise ValueError("Story structure has not been created")

        self.validation_errors = []
        
        # プロット要素の順序チェック
        plot_orders = [elem.order for elem in self.structure.plot_elements]
        if len(plot_orders) != len(set(plot_orders)):
            self.validation_errors.append("Duplicate plot element orders found")

        # チャプターとプロット要素の関連チェック
        chapter_ids = {chapter['id'] for chapter in self.structure.chapters}
        for elem in self.structure.plot_elements:
            if elem.chapter_id and elem.chapter_id not in chapter_ids:
                self.validation_errors.append(
                    f"Plot element {elem.id} references non-existent chapter"
                )

        return len(self.validation_errors) == 0

    async def analyze_consistency(self) -> Dict:
        """
        物語全体の整合性を分析する
        
        Returns:
            Dict: 分析結果を含む辞書
        """
        if not self.structure:
            raise ValueError("Story structure has not been created")

        analysis_result = {
            "character_consistency": self._check_character_consistency(),
            "timeline_consistency": self._check_timeline_consistency(),
            "world_building_consistency": self._check_world_building_consistency(),
            "plot_flow": self._analyze_plot_flow(),
            "timestamp": datetime.now().isoformat()
        }

        logger.info("Consistency analysis completed")
        return analysis_result

    def _check_character_consistency(self) -> Dict:
        """キャラクターの整合性をチェック"""
        issues = []
        character_names = {char['name'] for char in self.structure.characters}
        
        for chapter in self.structure.chapters:
            if 'characters' in chapter:
                for char_name in chapter['characters']:
                    if char_name not in character_names:
                        issues.append(f"Unknown character '{char_name}' in chapter {chapter['id']}")

        return {"status": len(issues) == 0, "issues": issues}

    def _check_timeline_consistency(self) -> Dict:
        """タイムラインの整合性をチェック"""
        issues = []
        events = sorted(self.structure.timeline, key=lambda x: x['date'])
        
        for i in range(len(events) - 1):
            if events[i]['date'] > events[i + 1]['date']:
                issues.append(f"Timeline inconsistency between events {events[i]['id']} and {events[i + 1]['id']}")

        return {"status": len(issues) == 0, "issues": issues}

    def _check_world_building_consistency(self) -> Dict:
        """世界観設定の整合性をチェック"""
        issues = []
        rules = self.structure.world_building.get('rules', [])
        
        for chapter in self.structure.chapters:
            for rule in rules:
                if not self._validate_world_rule(chapter, rule):
                    issues.append(f"World building rule '{rule['name']}' violated in chapter {chapter['id']}")

        return {"status": len(issues) == 0, "issues": issues}

    def _analyze_plot_flow(self) -> Dict:
        """プロットの流れを分析"""
        plot_elements = sorted(self.structure.plot_elements, key=lambda x: x.order)
        flow_analysis = {
            "plot_points": len(plot_elements),
            "gaps": [],
            "potential_issues": []
        }

        for i in range(len(plot_elements) - 1):
            if plot_elements[i + 1].order - plot_elements[i].order > 1:
                flow_analysis["gaps"].append(f"Gap between elements {plot_elements[i].id} and {plot_elements[i + 1].id}")

        return flow_analysis

    def _validate_world_rule(self, chapter: Dict, rule: Dict) -> bool:
        """世界観ルールの検証"""
        # 実装は世界観ルールの具体的な形式に依存
        return True