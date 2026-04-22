# constants.py
"""常量定义模块 - 引用主题系统"""

from typing import Dict
from theme_preset import GLASS_QSS, build_qss_from_theme, get_theme, get_theme_list, set_current_theme, get_current_theme

# ================= 基础命名空间 (原有逻辑保持不变) =================
NAMESPACE_ENGINE = "PvZCards.Engine.Components."
NAMESPACE_QUERY = "PvZCards.Engine.Queries."
ASSEMBLY_SUFFIX = ", EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"


def build_type_str(comp_name: str, is_query: bool = False) -> str:
    """构建组件类型字符串"""
    prefix = NAMESPACE_QUERY if is_query else NAMESPACE_ENGINE
    return f"{prefix}{comp_name}{ASSEMBLY_SUFFIX}"


def parse_type_str(type_str: str) -> str:
    """从类型字符串中解析出组件名"""
    if not type_str:
        return ""
    return type_str.split(',')[0].split('.')[-1]


# ================= 能力组件映射 (原有逻辑) =================
ABILITY_COMP_MAP: Dict[str, str] = {
    "Multishot": "Multishot",
    "AttacksInAllLanes": "AttacksInAllLanes",
    "PlaysFaceDown": "PlaysFaceDown",
    "Aquatic": "Aquatic",
    "Truestrike": "Truestrike",
    "Strikethrough": "Strikethrough",
    "Deadly": "Deadly",
    "Frenzy": "Frenzy",
    "AttackOverride": "AttackOverride",
    "SplashDamage": "SplashDamage",
    "Armor": "Armor",
    "Untrickable": "Untrickable",
    "DoubleStrike": "GrantedTriggeredAbilities",
    "Teamup": "CreateInFront"
}

COMP_ABILITY_MAP: Dict[str, str] = {v: k for k, v in ABILITY_COMP_MAP.items()}


# ================= 重新导出主题相关函数，保持向后兼容 =================
__all__ = [
    # 主题相关
    'GLASS_QSS',
    'build_qss_from_theme',
    'get_theme',
    'get_theme_list',
    'set_current_theme',
    'get_current_theme',
    # 工具函数
    'build_type_str',
    'parse_type_str',
    # 映射表
    'ABILITY_COMP_MAP',
    'COMP_ABILITY_MAP',
    # 常量
    'NAMESPACE_ENGINE',
    'NAMESPACE_QUERY',
    'ASSEMBLY_SUFFIX',
]