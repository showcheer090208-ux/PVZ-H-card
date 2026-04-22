# ui_main.py
import json
import html
import re
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTextEdit, QGroupBox, QStackedWidget, QSplitter, 
                               QApplication, QListWidget, QListWidgetItem, QMenuBar, QMenu, QPushButton)
from PySide6.QtCore import Qt, QSettings, QObject, QEvent, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QIcon, QAction

from card_model import CardModel
from ui.tab_basic import TabBasic
from ui.tab_subtypes import TabSubtypes
from ui.tab_tags import TabTags
from ui.tab_abilities import TabAbilities
from ui.logic.panel_main import PanelLogic
from ui.tab_export import TabExport
from ui.tab_theme import TabTheme  # 新增主题设置页
from project_manager import ProjectManager
from ui.tab_project import TabProject

# 导入背景与主题系统
from widgets import ArenaBackgroundWidget
from constants import GLASS_QSS, get_theme_list, get_current_theme, set_current_theme, build_qss_from_theme


class FastScrollFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            if QApplication.keyboardModifiers() & Qt.ControlModifier:
                scroll_area = None
                if hasattr(obj, 'verticalScrollBar'):
                    scroll_area = obj
                elif hasattr(obj, 'parent') and hasattr(obj.parent(), 'verticalScrollBar'):
                    scroll_area = obj.parent()
                    
                if scroll_area:
                    vbar = scroll_area.verticalScrollBar()
                    delta = event.angleDelta().y()
                    if delta != 0:
                        step = vbar.singleStep() * 10 
                        if delta > 0:
                            vbar.setValue(vbar.value() - step)
                        else:
                            vbar.setValue(vbar.value() + step)
                        return True
        return super().eventFilter(obj, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PvZ Heroes Modding Tool - 幻影引擎 v1.1")
        self.resize(1400, 900)
        self.model = CardModel()
        self.pm = ProjectManager()
        
        # 初始化设置
        self.settings = QSettings("ModdingTool", "PvZHeroesEditor")
        
        # 加载保存的主题
        saved_theme = self.settings.value("theme", "PhantomDeep")
        set_current_theme(saved_theme)
        
        # 应用主题样式
        self.apply_theme()

        # ================= 侧边栏状态管理 =================
        self.is_sidebar_pinned = False
        self.sidebar_delay_timer = QTimer(self)
        self.sidebar_delay_timer.setSingleShot(True)
        self.sidebar_delay_timer.timeout.connect(self._do_collapse)
        
        self._setup_ui()

        # ================= 读取窗口状态记忆 =================
        geometry = self.settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)
            
        splitter_state = self.settings.value("splitterSizes_v3")
        if splitter_state:
            self.splitter.restoreState(splitter_state)

        self.update_json_preview()
    
    def apply_theme(self):
        """应用当前主题样式"""
        qss = build_qss_from_theme()
        self.setStyleSheet(qss)
        if hasattr(self, 'settings'):
            self.settings.setValue("theme", get_current_theme())
    
    def switch_theme(self, theme_name):
        """切换主题"""
        if set_current_theme(theme_name):
            self.apply_theme()
            for i in range(self.stacked_widget.count()):
                widget = self.stacked_widget.widget(i)
                if hasattr(widget, "refresh_theme_display"):
                    widget.refresh_theme_display()
                    
    def handle_external_import(self, path, guid):
        """处理来自 Basic 页的外部导入请求"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            guid_str = str(guid)
            if guid_str not in data:
                QMessageBox.warning(self, "未找到", f"在文件中找不到 GUID: {guid_str}")
                return
            
            # 将外部数据字典直接喂给加载器
            self.load_card_to_workbench(data[guid_str])
            # 同步更新一下 GUID
            self.model.guid = guid
            self.tab_basic.update_ui(self.model)
            
            QMessageBox.information(self, "成功", f"卡牌 {guid_str} 已成功导入工作台！")
        except Exception as e:
            QMessageBox.critical(self, "导入失败", f"解析异常: {e}")

    def _setup_ui(self):
        self.bg_widget = ArenaBackgroundWidget(self)
        self.setCentralWidget(self.bg_widget)
        
        main_layout = QHBoxLayout(self.bg_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================== 【回归】操作加速逻辑 ==================
        # 创建全局滚动过滤器实例
        self.fast_scroll_filter = FastScrollFilter(self)
        # =========================================================

        # ---------------- 灵动侧边栏 (Sidebar Container) ----------------
        self.sidebar_container = QWidget()
        self.sidebar_container.setFixedWidth(45)
        self.sidebar_container.setObjectName("SidebarContainer")
        sidebar_vbox = QVBoxLayout(self.sidebar_container)
        sidebar_vbox.setContentsMargins(0, 5, 0, 0)
        sidebar_vbox.setSpacing(5)

        # 侧边栏固定按钮
        self.pin_btn = QPushButton("📌")
        self.pin_btn.setCheckable(True)
        self.pin_btn.setFixedSize(45, 30)
        self.pin_btn.setStyleSheet("background: transparent; border: none; font-size: 16px;")
        self.pin_btn.clicked.connect(self.toggle_sidebar_pin)
        sidebar_vbox.addWidget(self.pin_btn, 0, Qt.AlignHCenter)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setMouseTracking(True)
        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sidebar.setStyleSheet("background: transparent; border: none;")
        # 【应用加速】侧边栏
        self.sidebar.installEventFilter(self.fast_scroll_filter)
        sidebar_vbox.addWidget(self.sidebar)

        main_layout.addWidget(self.sidebar_container)

        # 侧边栏整体动画控制器
        self.sidebar_anim = QPropertyAnimation(self.sidebar_container, b"minimumWidth")
        self.sidebar_anim.setDuration(300)
        self.sidebar_anim.setEasingCurve(QEasingCurve.OutQuint)

        self.sidebar_container.installEventFilter(self)

        # ---------------- 右侧主工作区 (Splitter) ----------------
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        self.stacked_widget = QStackedWidget()
        self.splitter.addWidget(self.stacked_widget)
        
        # ================= 页面注册 =================
        self.tab_project = TabProject(self.pm) # 【新增】大厅页
        self.tab_project.edit_card_requested.connect(self.load_card_to_workbench) # 绑定双击事件
        
        self.tab_basic = TabBasic(self.model)
        # ================= 接住 Basic 页的新信号 =================
        # 1. 接住保存信号
        self.tab_basic.save_requested.connect(self.sync_data_to_model)
        
        # 2. 接住导入信号
        self.tab_basic.import_requested.connect(self.handle_external_import)
        # =========================================================
        self.tab_subtypes = TabSubtypes()
        self.tab_tags = TabTags()
        self.tab_abilities = TabAbilities()
        self.tab_logic = PanelLogic()
        self.tab_export = TabExport(self.pm)
        self.tab_theme = TabTheme(self)
        
        self._register_tab("🏠", "工程大厅", self.tab_project)
        self._register_tab("📋", "基础属性", self.tab_basic)
        self._register_tab("🧬", "种族配置", self.tab_subtypes)
        self._register_tab("🏷️", "标签配置", self.tab_tags)
        self._register_tab("✨", "特殊能力", self.tab_abilities)
        self._register_tab("🛠️", "技能逻辑", self.tab_logic)
        self._register_tab("💾", "封包导出", self.tab_export)
        self._register_tab("🎨", "主题设置", self.tab_theme)

        self.sidebar.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        # ================= JSON 预览区 (无换行 + HTML高亮) =================
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        self.json_preview = QTextEdit()
        self.json_preview.setReadOnly(True)
        self.json_preview.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.json_preview.setStyleSheet("""
            QTextEdit { 
                background-color: #1e1e1e; 
                border: 1px solid #333333;
                border-radius: 6px;
            }
        """)
        # 【应用加速】JSON 预览区（单独配置）
        self.json_preview.installEventFilter(self.fast_scroll_filter)
        # 额外：确保预览区的滚动条视口也捕获 Ctrl+滚轮
        if hasattr(self.json_preview, 'viewport'):
            self.json_preview.viewport().installEventFilter(self.fast_scroll_filter)
        
        preview_layout.addWidget(self.json_preview)
        self.splitter.addWidget(preview_container)

        # 初始化分配比例 (防挤压)
        self.splitter.setSizes([900, 500])
        
        # 批量连接所有数据 Tab 的信号到同步函数
        tabs_with_data = [self.tab_basic, self.tab_subtypes, self.tab_tags, 
                        self.tab_abilities, self.tab_logic]
        for tab in tabs_with_data:
            if hasattr(tab, "data_changed"):
                tab.data_changed.connect(self.sync_data_to_model)

        # ================== 【核心】为所有数据面板挂载加速 ==================
        from PySide6.QtWidgets import QScrollArea
        
        for i in range(self.stacked_widget.count()):
            tab_widget = self.stacked_widget.widget(i)
            # 尝试在 Tab 内部寻找 ScrollArea
            if hasattr(tab_widget, "findChild"):
                scroll_areas = tab_widget.findChildren(QScrollArea)
                for scroll_area in scroll_areas:
                    if scroll_area and hasattr(scroll_area, 'viewport'):
                        scroll_area.viewport().installEventFilter(self.fast_scroll_filter)
            # 同时给 Tab 本身也挂一个
            tab_widget.installEventFilter(self.fast_scroll_filter)
        # =================================================================

        self._setup_shortcuts()
        
        

    def toggle_sidebar_pin(self):
        """侧边栏图钉功能"""
        self.is_sidebar_pinned = self.pin_btn.isChecked()
        self.pin_btn.setText("📍" if self.is_sidebar_pinned else "📌")

    def _setup_shortcuts(self):
        from PySide6.QtGui import QShortcut, QKeySequence
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.sync_data_to_model)
        
        export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_shortcut.activated.connect(self.quick_export)

    def quick_export(self):
        if hasattr(self.tab_export, 'export_card'):
            self.tab_export.export_card()

    def _register_tab(self, icon, full_name, widget_instance):
        item = QListWidgetItem(f"{icon}  {full_name}")
        self.sidebar.addItem(item)
        self.stacked_widget.addWidget(widget_instance)

    # ---------------- 侧边栏平滑动画逻辑 ----------------
    def eventFilter(self, obj, event):
        if obj == self.sidebar_container:
            if event.type() == QEvent.Enter:
                self.sidebar_delay_timer.stop()
                self.sidebar_anim.setDuration(300)
                self.sidebar_anim.setEasingCurve(QEasingCurve.OutQuint)
                self.sidebar_anim.setEndValue(180)
                self.sidebar_anim.start()
            elif event.type() == QEvent.Leave:
                if not self.is_sidebar_pinned:
                    self.sidebar_delay_timer.start(500) # 延迟500ms缩回
        return super().eventFilter(obj, event)

    def _do_collapse(self):
        """真正的缩回动作"""
        self.sidebar_anim.setDuration(600)
        self.sidebar_anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.sidebar_anim.setEndValue(45)
        self.sidebar_anim.start()

    def closeEvent(self, event):
        if hasattr(self, 'settings'):
            self.settings.setValue("windowGeometry", self.saveGeometry())
            if hasattr(self, 'splitter'):
                self.settings.setValue("splitterSizes_v3", self.splitter.saveState())
        super().closeEvent(event)

    def sync_data_to_model(self):
        """Ctrl+S 的新逻辑：不仅同步 UI，还要保存到工程"""
        if getattr(self, '_is_syncing', False):
            return
        self._is_syncing = True
        try:
            for i in range(self.stacked_widget.count()):
                widget = self.stacked_widget.widget(i)
                if hasattr(widget, "sync_to_model") and widget not in [self.tab_theme, self.tab_project]:
                    widget.sync_to_model(self.model)
            
            self.update_json_preview()
            
            # 【核心修改】将修改后的单卡模型，扔进工程大厅保存落盘
            if self.pm.current_project_name:
                self.pm.add_or_update_card(self.model)
                self.tab_project.refresh_card_roster() # 刷新大厅列表
                
                # 在窗口标题上给个反馈
                self.setWindowTitle(f"PvZ Heroes 幻影引擎 v2.0 - [已保存至 {self.pm.current_project_name}]")
        finally:
            self._is_syncing = False

    def load_card_to_workbench(self, card_data_dict):
        """【新增】从大厅双击卡牌，或者新建卡牌，加载进工作台"""
        if not card_data_dict:
            # 传的是空字典，说明是要新建卡牌
            self.model = CardModel()
        else:
            # 传的是工程里保存的字典，解析它
            self.model = CardModel.from_json(card_data_dict)
            
        # 刷新所有 UI
        try:
            for i in range(self.stacked_widget.count()):
                widget = self.stacked_widget.widget(i)
                if hasattr(widget, "set_model"):
                    widget.set_model(self.model)
        finally:
            self.update_json_preview()
            
        # 自动跳转到“基础属性”页
        self.sidebar.setCurrentRow(1)

    def update_json_preview(self):
        """更新JSON预览区 (使用HTML高亮注入)"""
        data_dict = self.model.generate_json_dict()
        html_str = self._generate_highlighted_json(data_dict)
        
        v_bar = self.json_preview.verticalScrollBar()
        h_bar = self.json_preview.horizontalScrollBar()
        v_val = v_bar.value()
        h_val = h_bar.value()
        
        self.json_preview.setHtml(html_str)
        v_bar.setValue(v_val)
        h_bar.setValue(h_val)

    def _generate_highlighted_json(self, data_dict):
        """将 Dict 转为带有 VSCode 主题颜色的纯净 HTML 结构，免疫全局 QSS 污染"""
        json_str = json.dumps(data_dict, indent=4, ensure_ascii=False)
        lines = json_str.split('\n')
        html_lines = []
        
        for line in lines:
            line = html.escape(line)
            # 高亮 键 (Key)
            line = re.sub(r'^(\s*)(&quot;.*?&quot;)(:)', r'\1<span style="color:#ce9178;">\2</span>\3', line)
            # 高亮 字符串值
            line = re.sub(r'(: \s*)(&quot;.*?&quot;)(,?)$', r'\1<span style="color:#9cdcfe;">\2</span>\3', line)
            line = re.sub(r'^(\s*)(&quot;.*?&quot;)(,?)$', r'\1<span style="color:#9cdcfe;">\2</span>\3', line)
            # 高亮 数字与布尔/Null
            line = re.sub(r'(: \s*)([0-9\.\-]+)(,?)$', r'\1<span style="color:#b5cea8;">\2</span>\3', line)
            line = re.sub(r'(: \s*)(true|false|null)(,?)$', r'\1<span style="color:#569cd6;">\2</span>\3', line)
            line = re.sub(r'^(\s*)([0-9\.\-]+)(,?)$', r'\1<span style="color:#b5cea8;">\2</span>\3', line)
            line = re.sub(r'^(\s*)(true|false|null)(,?)$', r'\1<span style="color:#569cd6;">\2</span>\3', line)
            
            html_lines.append(line)
            
        body = "\n".join(html_lines)
        return f'<pre style="font-family: Consolas, Monaco, monospace; font-size: 13px; line-height: 1.4;">{body}</pre>'

    def refresh_all_ui(self, new_model):
        """接收到导入的 Model，并绑定到所有面板上"""
        self.model = new_model
        try:
            for i in range(self.stacked_widget.count()):
                widget = self.stacked_widget.widget(i)
                if hasattr(widget, "set_model"):
                    widget.set_model(self.model)
        except Exception as e:
            print(f"UI 刷新异常: {e}")
        finally:
            self.update_json_preview()