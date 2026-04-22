# theme_preset.py
"""主题预设系统 - 支持多套配色方案，优化文字对比度"""

from typing import Dict, Any

# ================= 主题预设定义 =================

THEMES: Dict[str, Dict[str, Any]] = {
    # 幻影深邃版 (当前默认)
    "PhantomDeep": {
        "name": "🌌 幻影深邃",
        "description": "深色半透明 + 动态极光背景，护眼且炫酷",
        
        # 颜色变量
        "colors": {
            "primary": "#4da8da",
            "primary_hover": "#6bb9e0",
            "primary_bg": "rgba(77, 168, 218, 80)",
            "primary_border": "rgba(77, 168, 218, 60)",
            "primary_border_hover": "#4da8da",
            
            "secondary": "#673AB7",
            "secondary_hover": "#7E57C2",
            "secondary_bg": "rgba(103, 58, 183, 180)",
            
            "bg_dark": "rgba(8, 8, 14, 230)",
            "bg_medium": "rgba(25, 28, 38, 220)",
            "bg_light": "rgba(35, 38, 48, 200)",
            "bg_card": "rgba(30, 33, 43, 180)",
            "bg_group": "rgba(28, 30, 40, 150)",
            "bg_hover": "rgba(77, 168, 218, 40)",
            
            "text_main": "#EAECEE",
            "text_light": "#D5D8DC",
            "text_dim": "#AAB7B8",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF6B6B",
            "text_success": "#6BCB77",
            
            "border_light": "rgba(255, 255, 255, 15)",
            "border_medium": "rgba(255, 255, 255, 25)",
            "border_dark": "rgba(100, 100, 130, 150)",
        },
        
        "glass_effect": True,
        "blur_intensity": 180,
    },
    
    # 炽热熔岩版 (暖色主题)
    "LavaGlow": {
        "name": "🔥 炽热熔岩",
        "description": "暖色调 + 熔岩质感，充满力量感",
        
        "colors": {
            "primary": "#E86A2C",
            "primary_hover": "#F0803C",
            "primary_bg": "rgba(232, 106, 44, 85)",
            "primary_border": "rgba(232, 106, 44, 65)",
            "primary_border_hover": "#E86A2C",
            
            "secondary": "#D32F2F",
            "secondary_hover": "#E53935",
            "secondary_bg": "rgba(211, 47, 47, 180)",
            
            "bg_dark": "rgba(35, 18, 12, 230)",
            "bg_medium": "rgba(50, 28, 20, 220)",
            "bg_light": "rgba(60, 38, 28, 200)",
            "bg_card": "rgba(55, 33, 23, 180)",
            "bg_group": "rgba(48, 28, 18, 150)",
            "bg_hover": "rgba(232, 106, 44, 40)",
            
            "text_main": "#FFE0C0",
            "text_light": "#FFD4A0",
            "text_dim": "#D4A070",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF8A80",
            "text_success": "#A5D6A7",
            
            "border_light": "rgba(255, 160, 80, 18)",
            "border_medium": "rgba(255, 160, 80, 28)",
            "border_dark": "rgba(200, 100, 50, 150)",
        },
        
        "glass_effect": True,
        "blur_intensity": 160,
    },
    
    # 翡翠梦境版 (冷色调绿色主题)
    "EmeraldDream": {
        "name": "🌿 翡翠梦境",
        "description": "自然冷色调 + 柔和质感，舒缓双眼",
        
        "colors": {
            "primary": "#4DB6AC",
            "primary_hover": "#66C9C0",
            "primary_bg": "rgba(77, 182, 172, 85)",
            "primary_border": "rgba(77, 182, 172, 65)",
            "primary_border_hover": "#4DB6AC",
            
            "secondary": "#2E7D32",
            "secondary_hover": "#388E3C",
            "secondary_bg": "rgba(46, 125, 50, 180)",
            
            "bg_dark": "rgba(12, 28, 22, 230)",
            "bg_medium": "rgba(22, 42, 34, 220)",
            "bg_light": "rgba(28, 48, 40, 200)",
            "bg_card": "rgba(24, 42, 34, 180)",
            "bg_group": "rgba(20, 38, 30, 150)",
            "bg_hover": "rgba(77, 182, 172, 40)",
            
            "text_main": "#D0F0E8",
            "text_light": "#E0F8F0",
            "text_dim": "#A0C8B8",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF8A80",
            "text_success": "#C8E6C9",
            
            "border_light": "rgba(100, 200, 180, 18)",
            "border_medium": "rgba(100, 200, 180, 28)",
            "border_dark": "rgba(60, 120, 100, 150)",
        },
        
        "glass_effect": True,
        "blur_intensity": 170,
    },
    
    # 紫色幻梦版
    "PurpleDream": {
        "name": "💜 紫色幻梦",
        "description": "神秘紫色调，优雅且富有想象力",
        
        "colors": {
            "primary": "#B85CE0",
            "primary_hover": "#C96EF0",
            "primary_bg": "rgba(184, 92, 224, 85)",
            "primary_border": "rgba(184, 92, 224, 65)",
            "primary_border_hover": "#B85CE0",
            
            "secondary": "#E91E63",
            "secondary_hover": "#F06292",
            "secondary_bg": "rgba(233, 30, 99, 180)",
            
            "bg_dark": "rgba(22, 12, 28, 230)",
            "bg_medium": "rgba(38, 22, 48, 220)",
            "bg_light": "rgba(48, 32, 58, 200)",
            "bg_card": "rgba(44, 28, 54, 180)",
            "bg_group": "rgba(38, 22, 48, 150)",
            "bg_hover": "rgba(184, 92, 224, 40)",
            
            "text_main": "#F0E0F8",
            "text_light": "#F8ECFC",
            "text_dim": "#C8A8E0",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF80AB",
            "text_success": "#C8E6C9",
            
            "border_light": "rgba(200, 150, 220, 18)",
            "border_medium": "rgba(200, 150, 220, 28)",
            "border_dark": "rgba(120, 80, 140, 150)",
        },
        
        "glass_effect": True,
        "blur_intensity": 175,
    },
    
    # 海洋之心版
    "OceanHeart": {
        "name": "💙 海洋之心",
        "description": "深海蓝色调，冷静且专注",
        
        "colors": {
            "primary": "#0891D1",
            "primary_hover": "#18A1E1",
            "primary_bg": "rgba(8, 145, 209, 85)",
            "primary_border": "rgba(8, 145, 209, 65)",
            "primary_border_hover": "#0891D1",
            
            "secondary": "#00ACC1",
            "secondary_hover": "#26C6DA",
            "secondary_bg": "rgba(0, 172, 193, 180)",
            
            "bg_dark": "rgba(6, 18, 28, 230)",
            "bg_medium": "rgba(16, 32, 48, 220)",
            "bg_light": "rgba(26, 42, 58, 200)",
            "bg_card": "rgba(22, 38, 54, 180)",
            "bg_group": "rgba(18, 34, 48, 150)",
            "bg_hover": "rgba(8, 145, 209, 40)",
            
            "text_main": "#D0E8F8",
            "text_light": "#E0F0FC",
            "text_dim": "#90B8D0",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF8A80",
            "text_success": "#A5D6A7",
            
            "border_light": "rgba(100, 180, 220, 18)",
            "border_medium": "rgba(100, 180, 220, 28)",
            "border_dark": "rgba(60, 100, 130, 150)",
        },
        
        "glass_effect": True,
        "blur_intensity": 165,
    },
    
    # 经典亮色版 (日间模式)
    "ClassicLight": {
        "name": "☀️ 经典亮色",
        "description": "清爽亮色 + 柔和阴影，适合日间使用",
        
        "colors": {
            "primary": "#1976D2",
            "primary_hover": "#2196F3",
            "primary_bg": "rgba(25, 118, 210, 12)",
            "primary_border": "rgba(25, 118, 210, 35)",
            "primary_border_hover": "#1976D2",
            
            "secondary": "#F57C00",
            "secondary_hover": "#FF9800",
            "secondary_bg": "rgba(245, 124, 0, 160)",
            
            "bg_dark": "rgba(245, 245, 250, 230)",
            "bg_medium": "rgba(250, 250, 255, 220)",
            "bg_light": "rgba(252, 252, 255, 200)",
            "bg_card": "rgba(248, 248, 252, 180)",
            "bg_group": "rgba(242, 242, 247, 150)",
            "bg_hover": "rgba(25, 118, 210, 8)",
            
            "text_main": "#1A1A2E",
            "text_light": "#2D2D44",
            "text_dim": "#66667A",
            "text_bright": "#000000",
            "text_warning": "#D32F2F",
            "text_success": "#388E3C",
            
            "border_light": "rgba(0, 0, 0, 10)",
            "border_medium": "rgba(0, 0, 0, 15)",
            "border_dark": "rgba(0, 0, 0, 25)",
        },
        
        "glass_effect": False,
        "blur_intensity": 0,
    },
    
    # 午夜暗影版 (极致对比)
    "MidnightShadow": {
        "name": "🌙 午夜暗影",
        "description": "极致黑色背景 + 高亮霓虹色，顶级对比度",
        
        "colors": {
            "primary": "#00E5FF",
            "primary_hover": "#33EBFF",
            "primary_bg": "rgba(0, 229, 255, 90)",
            "primary_border": "rgba(0, 229, 255, 70)",
            "primary_border_hover": "#00E5FF",
            
            "secondary": "#FF0266",
            "secondary_hover": "#FF4081",
            "secondary_bg": "rgba(255, 2, 102, 180)",
            
            "bg_dark": "rgba(5, 5, 8, 245)",
            "bg_medium": "rgba(12, 12, 18, 235)",
            "bg_light": "rgba(18, 18, 25, 220)",
            "bg_card": "rgba(15, 15, 22, 200)",
            "bg_group": "rgba(10, 10, 15, 170)",
            "bg_hover": "rgba(0, 229, 255, 30)",
            
            "text_main": "#E8E8F0",
            "text_light": "#F0F0F8",
            "text_dim": "#A0A0B0",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF4081",
            "text_success": "#00E676",
            
            "border_light": "rgba(0, 229, 255, 20)",
            "border_medium": "rgba(0, 229, 255, 30)",
            "border_dark": "rgba(0, 229, 255, 10)",
        },
        
        "glass_effect": True,
        "blur_intensity": 200,
    },
    
    # 琥珀金典版 (暖色高对比)
    "AmberGold": {
        "name": "✨ 琥珀金典",
        "description": "琥珀暖金色调，温暖且清晰易读",
        
        "colors": {
            "primary": "#FFB300",
            "primary_hover": "#FFC107",
            "primary_bg": "rgba(255, 179, 0, 85)",
            "primary_border": "rgba(255, 179, 0, 65)",
            "primary_border_hover": "#FFB300",
            
            "secondary": "#FF6D00",
            "secondary_hover": "#FF8F00",
            "secondary_bg": "rgba(255, 109, 0, 180)",
            
            "bg_dark": "rgba(20, 15, 8, 235)",
            "bg_medium": "rgba(30, 22, 14, 225)",
            "bg_light": "rgba(38, 30, 20, 210)",
            "bg_card": "rgba(34, 26, 16, 190)",
            "bg_group": "rgba(28, 20, 12, 160)",
            "bg_hover": "rgba(255, 179, 0, 35)",
            
            "text_main": "#FFF0D0",
            "text_light": "#FFF8E8",
            "text_dim": "#D4B890",
            "text_bright": "#FFFFFF",
            "text_warning": "#FF6B6B",
            "text_success": "#A5D6A7",
            
            "border_light": "rgba(255, 179, 0, 20)",
            "border_medium": "rgba(255, 179, 0, 30)",
            "border_dark": "rgba(200, 120, 0, 100)",
        },
        
        "glass_effect": True,
        "blur_intensity": 160,
    },
}

# 当前激活的主题
_current_theme = "PhantomDeep"


def get_current_theme() -> str:
    """获取当前主题名称"""
    return _current_theme


def set_current_theme(theme_name: str) -> bool:
    """设置当前主题"""
    global _current_theme
    if theme_name in THEMES:
        _current_theme = theme_name
        return True
    return False


def get_theme(theme_name: str = None) -> Dict[str, Any]:
    """获取主题配置"""
    name = theme_name or _current_theme
    return THEMES.get(name, THEMES["PhantomDeep"])


def get_theme_list() -> list:
    """获取所有主题列表"""
    return [(key, THEMES[key]["name"]) for key in THEMES.keys()]


def build_qss_from_theme(theme_name: str = None) -> str:
    """根据主题生成 QSS 样式表"""
    theme = get_theme(theme_name)
    c = theme["colors"]
    glass = theme["glass_effect"]
    
    # 根据玻璃态效果决定背景透明度
    if glass:
        bg_intensity = theme["blur_intensity"]
        bg_input = f"rgba(20, 20, 30, {bg_intensity})"
        bg_card = c["bg_card"]
        bg_group = c["bg_group"]
        bg_hover = c["bg_hover"]
    else:
        bg_input = c["bg_medium"]
        bg_card = c["bg_light"]
        bg_group = c["bg_light"]
        bg_hover = c["bg_hover"]
    
    qss = f"""
/* ================= 主题: {theme["name"]} ================= */
/* 描述: {theme["description"]} */

QWidget {{
    color: {c["text_main"]};
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    background: transparent;
}}

/* 强制清除所有容器的背景干扰 */
QScrollArea, QStackedWidget, QTabWidget, QTabBar::tab {{
    background: transparent;
    border: none;
}}

/* 输入框、下拉框、调节框 - 增强对比度 */
QTextEdit, QLineEdit, QComboBox, QSpinBox, QTextBrowser {{
    background-color: {c["bg_medium"]} !important;
    color: {c["text_bright"]} !important;
    border: 1px solid {c["primary_border"]};
    border-radius: 4px;
    padding: 5px;
    font-weight: 500;
}}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 2px solid {c["primary"]};
    background-color: {c["bg_light"]} !important;
}}

/* 列表与树状图 - 增强选中对比 */
QListWidget, QTreeWidget {{
    background-color: {c["bg_dark"]} !important;
    border: 1px solid {c["primary_border"]};
    outline: none;
}}

QListWidget::item, QTreeWidget::item {{ 
    height: 35px; 
    padding: 0 10px;
    border-bottom: 1px solid {c["border_light"]};
}}

QListWidget::item:selected, QTreeWidget::item:selected {{ 
    background-color: {c["primary_bg"]}; 
    color: {c["text_bright"]};
    font-weight: bold;
}}

QListWidget::item:hover, QTreeWidget::item:hover {{
    background-color: {c["bg_hover"]};
}}

/* 灵动侧边栏专属样式 */
QListWidget#Sidebar {{
    background-color: {c["bg_dark"]} !important;
    border: none;
    border-right: 1px solid {c["border_medium"]};
}}

QListWidget#Sidebar::item:selected {{
    background-color: {c["primary_bg"]};
    border-left: 3px solid {c["primary"]};
}}

/* 分割线 */
QSplitter::handle {{
    background: transparent;
    width: 20px;
}}

/* 面板组样式 - 增强标题对比 */
QGroupBox {{
    color: {c["primary"]};
    font-weight: bold;
    border: 1px solid {c["primary_border"]};
    border-radius: 8px;
    margin-top: 15px;
    background-color: {bg_group};
    font-size: 13px;
}}

QGroupBox::title {{ 
    subcontrol-origin: margin; 
    left: 15px; 
    padding: 0 8px; 
    background-color: {bg_group};
}}

/* 按钮 - 增强悬停反馈 */
QPushButton {{
    background-color: {c["bg_medium"]};
    color: {c["text_bright"]};
    border: 1px solid {c["border_dark"]};
    border-radius: 4px;
    padding: 8px 15px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {c["primary"]};
    border-color: {c["text_bright"]};
}}

QPushButton:pressed {{
    background-color: {c["primary_hover"]};
}}

/* 滚动条 */
QScrollBar:vertical {{ width: 6px; background: transparent; }}
QScrollBar::handle:vertical {{ background: {c["primary_bg"]}; border-radius: 3px; }}
QScrollBar::handle:vertical:hover {{ background: {c["primary"]}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0px; }}

/* CheckBox 样式 - 增强可读性 */
QCheckBox {{
    color: {c["text_main"]};
    spacing: 8px;
    font-weight: 500;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1px solid {c["primary_border"]};
    background-color: {c["bg_medium"]};
}}

QCheckBox::indicator:checked {{
    background-color: {c["primary"]};
    border-color: {c["primary"]};
}}

/* AbilityRow 卡片样式 */
AbilityRow {{
    background-color: {bg_card};
    border: 1px solid {c["primary_border"]};
    border-radius: 6px;
}}
AbilityRow:hover {{
    background-color: {bg_hover};
    border: 1px solid {c["primary"]};
}}

/* 标签页样式 - 增强选中标识 */
QTabWidget::pane {{
    border: 1px solid {c["primary_border"]};
    background: transparent;
}}

QTabBar::tab {{
    padding: 8px 16px;
    margin-right: 4px;
    background-color: {c["bg_medium"]};
    border-radius: 4px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {c["primary"]};
    color: {c["text_bright"]};
}}

QTabBar::tab:hover:!selected {{
    background-color: {c["primary_hover"]};
    color: {c["text_bright"]};
}}

/* JSON 预览区 - 等宽字体 */
QTextEdit {{
    background-color: {c["bg_dark"]} !important;
    border: none;
    font-family: "Consolas", "Monaco", "Cascadia Code", monospace;
    font-size: 12px;
    color: {c["text_light"]};
}}

/* 下拉框弹出菜单 */
QComboBox QAbstractItemView {{
    background-color: {c["bg_medium"]};
    color: {c["text_main"]};
    border: 1px solid {c["primary_border"]};
    selection-background-color: {c["primary_bg"]};
    selection-color: {c["text_bright"]};
}}

/* 提示框 */
QToolTip {{
    background-color: {c["bg_dark"]};
    color: {c["text_bright"]};
    border: 1px solid {c["primary"]};
    border-radius: 4px;
    padding: 4px 8px;
}}
"""
    return qss


# 保持向后兼容 - 导出默认 QSS
GLASS_QSS = build_qss_from_theme("PhantomDeep")