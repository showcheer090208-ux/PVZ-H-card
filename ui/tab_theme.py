# ui/tab_theme.py
"""主题设置页面 - 允许用户切换和预览主题"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                               QListWidget, QListWidgetItem, QLabel, QTextEdit,
                               QPushButton, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QColor, QPalette

from constants import get_theme_list, get_theme, set_current_theme, build_qss_from_theme
from theme_preset import GLASS_QSS


class ThemePreviewCard(QFrame):
    """主题预览卡片"""
    
    def __init__(self, theme_key: str, theme_data: dict, parent=None):
        super().__init__(parent)
        self.theme_key = theme_key
        self.theme_data = theme_data
        self.setup_ui()
        self.apply_preview_style()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 主题名称
        self.name_label = QLabel(self.theme_data["name"])
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        layout.addWidget(self.name_label)
        
        # 主题描述
        self.desc_label = QLabel(self.theme_data["description"])
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.desc_label)
        
        # 颜色预览条
        colors_widget = QWidget()
        colors_layout = QHBoxLayout(colors_widget)
        colors_layout.setContentsMargins(0, 10, 0, 10)
        colors_layout.setSpacing(5)
        
        colors = self.theme_data["colors"]
        preview_colors = [
            (colors["primary"], "主色"),
            (colors["secondary"], "辅色"),
            (colors["text_main"], "文字"),
            (colors["bg_dark"], "背景"),
        ]
        
        for color, name in preview_colors:
            color_block = QLabel()
            color_block.setFixedSize(40, 25)
            # 提取实际颜色值（处理rgba格式）
            if color.startswith("rgba"):
                # 从 rgba(r,g,b,a) 提取 rgb 部分用于显示
                import re
                match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+)', color)
                if match:
                    hex_color = f"#{int(match.group(1)):02x}{int(match.group(2)):02x}{int(match.group(3)):02x}"
                    color_block.setStyleSheet(f"background-color: {hex_color}; border-radius: 3px;")
                else:
                    color_block.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
            else:
                color_block.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
            color_block.setToolTip(name)
            colors_layout.addWidget(color_block)
        
        colors_layout.addStretch()
        layout.addWidget(colors_widget)
        
        # 应用按钮
        self.apply_btn = QPushButton("🎨 应用此主题")
        self.apply_btn.setFixedHeight(32)
        layout.addWidget(self.apply_btn)
    
    def apply_preview_style(self):
        """应用预览卡片样式"""
        self.setStyleSheet("""
            ThemePreviewCard {
                background-color: rgba(30, 30, 40, 150);
                border: 1px solid rgba(77, 168, 218, 40);
                border-radius: 8px;
            }
            ThemePreviewCard:hover {
                border: 1px solid #4da8da;
                background-color: rgba(77, 168, 218, 20);
            }
        """)


class TabTheme(QWidget):
    """主题设置标签页"""
    
    theme_changed = Signal(str)  # 主题切换信号
    
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 顶部说明
        info_group = QGroupBox("🎨 主题设置")
        info_layout = QVBoxLayout(info_group)
        
        info_label = QLabel(
            "选择你喜欢的界面主题。所有颜色、透明度、边框样式都会实时切换。\n"
            "部分主题支持玻璃态效果，提供更现代的视觉体验。"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #aaa; padding: 10px;")
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        
        # 当前主题指示
        current_group = QGroupBox("📌 当前主题")
        current_layout = QHBoxLayout(current_group)
        
        self.current_theme_label = QLabel()
        self.current_theme_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        current_layout.addWidget(self.current_theme_label)
        current_layout.addStretch()
        
        layout.addWidget(current_group)
        
        # 主题预览网格
        theme_group = QGroupBox("✨ 可选主题")
        theme_layout = QVBoxLayout(theme_group)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll.setWidget(scroll_content)
        theme_layout.addWidget(scroll)
        
        layout.addWidget(theme_group)
        
        # 底部按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.reset_btn = QPushButton("🔄 重置为默认主题")
        self.reset_btn.clicked.connect(self.reset_to_default)
        btn_layout.addWidget(self.reset_btn)
        
        layout.addLayout(btn_layout)
        
        # 加载主题列表
        self.load_themes()
        self.update_current_theme_display()
    
    def load_themes(self):
        """加载所有主题到网格"""
        # 清除现有内容
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        themes = get_theme_list()
        row, col = 0, 0
        max_cols = 2  # 每行2个卡片
        
        for theme_key, theme_name in themes:
            theme_data = get_theme(theme_key)
            card = ThemePreviewCard(theme_key, theme_data)
            card.apply_btn.clicked.connect(lambda checked, tk=theme_key: self.apply_theme(tk))
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def apply_theme(self, theme_key: str):
        """应用选中的主题"""
        if self.main_window:
            self.main_window.switch_theme(theme_key)
            self.update_current_theme_display()
            # 发出信号
            self.theme_changed.emit(theme_key)
    
    def update_current_theme_display(self):
        """更新当前主题显示"""
        from constants import get_current_theme, get_theme
        current_key = get_current_theme()
        theme_data = get_theme(current_key)
        self.current_theme_label.setText(f"当前主题：{theme_data['name']} — {theme_data['description']}")
    
    def refresh_theme_display(self):
        """刷新主题显示（从主窗口调用）"""
        self.update_current_theme_display()
        # 重新加载主题列表以更新按钮状态
        self.load_themes()
    
    def reset_to_default(self):
        """重置为默认主题"""
        self.apply_theme("PhantomDeep")