# widgets.py
"""动态背景组件 - 支持主题切换"""

import random
import math  # 新增 math 库以支持正弦波形计算
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient
from theme_preset import get_theme, get_current_theme, set_current_theme


class ArenaBackgroundWidget(QWidget):
    """动态竞技场背景 - 支持主题色同步"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 粒子系统：存储 [x, y, dx, dy, size, alpha]
        self.particles = []
        self.init_particles()
                           
        self.grid_offset_x = 0.0
        self.grid_offset_y = 0.0
        
        # 当前主题标识（用于检测主题切换）
        self.current_theme_key = get_current_theme()
        
        # 初始化主题颜色
        self.update_theme_colors()
        
        # 动画计时器 (代表时间流逝，不再是直接的色相偏差)
        self.time_counter = 0.0 
        self.flow_speed = 0.15  # 流动速度
        
        # 动画计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_bg)
        self.timer.start(16)  # 60 FPS

    def init_particles(self):
        """初始化粒子系统"""
        self.particles = []
        for _ in range(65):
            self.particles.append({
                'x': random.uniform(0, 2500),
                'y': random.uniform(0, 1500),
                'dx': random.uniform(-0.3, 0.3),
                'dy': random.uniform(-1.2, -0.3),
                'size': random.randint(2, 5),
                'alpha': random.randint(30, 80)
            })

    def update_theme_colors(self):
        """从主题系统同步颜色配置"""
        theme = get_theme()
        colors = theme["colors"]
        
        # 提取主题核心颜色
        self.theme_primary = QColor(colors["primary"])
        self.theme_secondary = QColor(colors["secondary"])
        self.theme_bg_dark = QColor(colors["bg_dark"])
        self.theme_text = QColor(colors["text_main"])
        
        # 根据主题类型决定流动速度和网格透明度
        theme_name = theme["name"]
        if "幻影" in theme_name or "深邃" in theme_name:
            self.flow_speed = 0.15
            self.grid_alpha = 15
        elif "熔岩" in theme_name or "炽热" in theme_name:
            self.flow_speed = 0.2
            self.grid_alpha = 20
        elif "翡翠" in theme_name or "梦境" in theme_name:
            self.flow_speed = 0.1
            self.grid_alpha = 12
        elif "海洋" in theme_name:
            self.flow_speed = 0.12
            self.grid_alpha = 15
        elif "紫色" in theme_name or "幻梦" in theme_name:
            self.flow_speed = 0.18
            self.grid_alpha = 18
        else:  # 经典亮色主题
            self.flow_speed = 0.05
            self.grid_alpha = 25
            
        # 获取主色的初始色相 (Base Hue)
        self.base_hue = float(self.theme_primary.hue())
        if self.base_hue < 0:
            self.base_hue = 210  # 默认蓝色
    
    def refresh_theme(self):
        """外部调用：主题切换时刷新颜色"""
        new_theme_key = get_current_theme()
        if new_theme_key != self.current_theme_key:
            self.current_theme_key = new_theme_key
            self.update_theme_colors()
            # 切换主题时不重置时间，保持呼吸动画的连贯性

    def animate_bg(self):
        """动画更新（每帧调用）"""
        self.refresh_theme()
        
        # 时间持续推移 (取模防止数值过大溢出)
        self.time_counter = (self.time_counter + self.flow_speed) % 360
        
        # 网格移动速度
        self.grid_offset_x = (self.grid_offset_x + 0.4) % 60
        self.grid_offset_y = (self.grid_offset_y + 0.4) % 60
        
        # 更新粒子位置
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            
            # 边界循环
            if p['y'] < -50:
                p['y'] = self.height() + 50
                p['x'] = random.uniform(0, max(self.width(), 200))
            if p['x'] < -50:
                p['x'] = self.width() + 50
            if p['x'] > self.width() + 50:
                p['x'] = -50
                
            # 随机微调透明度增加灵动感
            if random.random() < 0.01:
                p['alpha'] = random.randint(30, 90)
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # ================== 【核心算法修改】 ==================
        # 使用数学的正弦波 (sin) 让色相在当前主色的附近往复呼吸，而非绕着整个色环无脑增加。
        # 波幅限定在正负 25 度之内（这样无论是深渊蓝还是熔岩红，都不会变色变脏）。
        # math.radians 将时间计数转换为弧度，乘以4是稍微加快呼吸的频率。
        hue_deviation = math.sin(math.radians(self.time_counter * 4)) * 25
        current_hue = (self.base_hue + hue_deviation) % 360
        
        # 修复 Python 负数取模在某些 Qt 渲染下可能的问题
        if current_hue < 0:
            current_hue += 360
        # ====================================================
            
        # 经典亮色主题使用不同的渐变策略
        if "经典亮色" in get_theme()["name"]:
            color1 = QColor.fromHsv(int(current_hue), 30, 245)
            color2 = QColor.fromHsv(int((current_hue + 40) % 360), 25, 235)
            color3 = QColor.fromHsv(int((current_hue + 80) % 360), 20, 240)
        else:
            color1 = QColor.fromHsv(int(current_hue), 130, 90)
            color2 = QColor.fromHsv(int((current_hue + 45) % 360), 150, 60)
            color3 = QColor.fromHsv(int((current_hue + 80) % 360), 120, 110)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, color1)
        gradient.setColorAt(0.5, color2)
        gradient.setColorAt(1.0, color3)
        painter.fillRect(self.rect(), gradient)
        
        # --- 网格渲染（使用主题主色）---
        grid_color = QColor(self.theme_primary)
        grid_color.setAlpha(self.grid_alpha)
        painter.setPen(QPen(grid_color, 1))
        
        spacing = 60
        # 垂直网格线
        for x in range(0, self.width() + spacing, spacing):
            painter.drawLine(int(x - self.grid_offset_x), 0, 
                           int(x - self.grid_offset_x), self.height())
        # 水平网格线
        for y in range(0, max(self.height(), 1500) + spacing, spacing):
            painter.drawLine(0, int(y - self.grid_offset_y), 
                           self.width(), int(y - self.grid_offset_y))
        
        # --- 粒子渲染（光晕效果）---
        for p in self.particles:
            x, y, size = int(p['x']), int(p['y']), p['size']
            alpha = p['alpha']
            
            # 外层光晕（更大，更透明）
            painter.setPen(Qt.NoPen)
            glow_color = QColor(self.theme_primary)
            glow_color.setAlpha(alpha // 3)
            painter.setBrush(glow_color)
            painter.drawEllipse(x - size, y - size, size * 3, size * 3)
            
            # 内层粒子核心
            core_color = QColor(self.theme_primary)
            core_color.setAlpha(alpha)
            painter.setBrush(core_color)
            painter.drawEllipse(x, y, size, size)
            
            # 经典亮色主题下，粒子增加白色高光
            if "经典亮色" in get_theme()["name"]:
                painter.setBrush(QColor(255, 255, 255, alpha // 2))
                painter.drawEllipse(x - 1, y - 1, size // 2, size // 2)