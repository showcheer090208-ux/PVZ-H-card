# ui/tab_subtypes.py
"""种族配置标签页 - 移除硬编码样式，由全局主题控制"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QSpinBox, QLineEdit, QPushButton, QScrollArea, 
                               QGridLayout, QCheckBox, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, Signal
import config
from core_utils import signal_blocker


class TabSubtypes(QWidget):
    data_changed = Signal()

    def __init__(self):
        super().__init__()
        self.model = None
        self.logic_checkboxes = {}
        self.display_checkboxes = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # --- 上部分：新增区域 ---
        add_group = QGroupBox("新增自定义种族")
        add_layout = QHBoxLayout()
        self.new_sub_id = QSpinBox()
        self.new_sub_id.setRange(42, 2147483647)
        self.new_sub_name = QLineEdit()
        self.new_sub_name.setPlaceholderText("例如: 机甲 (Mech)")
        btn_add_sub = QPushButton("保存到本地库")
        btn_add_sub.clicked.connect(self.add_custom_subtype)
        
        add_layout.addWidget(self.new_sub_id)
        add_layout.addWidget(self.new_sub_name)
        add_layout.addWidget(btn_add_sub)
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)

        # --- 同步控制开关 ---
        self.sync_subtypes_cb = QCheckBox("保持【底层逻辑种族】自动同步到【UI显示种族】")
        self.sync_subtypes_cb.setChecked(True)
        self.sync_subtypes_cb.stateChanged.connect(self.on_sync_toggled)
        layout.addWidget(self.sync_subtypes_cb)

        # --- 下部分：左右双列列表区域 ---
        lists_layout = QHBoxLayout()
        
        logic_group = QGroupBox("底层逻辑种族 (Components生效，可作为隐藏触发)")
        logic_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logic_scroll = QScrollArea()
        self.logic_scroll.setWidgetResizable(True)
        logic_layout = QVBoxLayout()
        logic_layout.addWidget(self.logic_scroll)
        logic_group.setLayout(logic_layout)
        lists_layout.addWidget(logic_group)

        display_group = QGroupBox("UI显示层种族 (展示给玩家看的标签)")
        display_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.display_scroll = QScrollArea()
        self.display_scroll.setWidgetResizable(True)
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.display_scroll)
        display_group.setLayout(display_layout)
        lists_layout.addWidget(display_group)

        layout.addLayout(lists_layout)
        self.refresh_subtypes_grids()

    def refresh_subtypes_grids(self):
        logic_widget = QWidget()
        logic_grid = QGridLayout(logic_widget)
        display_widget = QWidget()
        display_grid = QGridLayout(display_widget)
        
        self.logic_checkboxes.clear()
        self.display_checkboxes.clear()
        
        # 【修复核心】config.py 已经把基础种族和自定义种族合并在 SUBTYPES 里了
        # 直接使用 config.SUBTYPES 即可，不需要再拼接
        sorted_keys = sorted(config.SUBTYPES.keys())
        
        row, col = 0, 0
        for key in sorted_keys:
            val = config.SUBTYPES[key]
            
            cb_logic = QCheckBox(f"[{key}] {val}")
            cb_logic.stateChanged.connect(lambda state, k=key: self.on_logic_changed(k, state))
            self.logic_checkboxes[key] = cb_logic
            logic_grid.addWidget(cb_logic, row, col)
            
            cb_display = QCheckBox(f"[{key}] {val}")
            cb_display.setEnabled(not self.sync_subtypes_cb.isChecked())
            cb_display.stateChanged.connect(lambda *args: self.data_changed.emit())
            self.display_checkboxes[key] = cb_display
            display_grid.addWidget(cb_display, row, col)
            
            col += 1
            if col > 1: 
                col = 0
                row += 1
                
        self.logic_scroll.setWidget(logic_widget)
        self.display_scroll.setWidget(display_widget)

    def on_logic_changed(self, key, state):
        if self.sync_subtypes_cb.isChecked():
            self.display_checkboxes[key].setChecked(state == Qt.Checked.value)
        self.data_changed.emit()

    def on_sync_toggled(self, state):
        is_sync = state == Qt.Checked.value
        for key, cb in self.display_checkboxes.items():
            cb.setEnabled(not is_sync)
            if is_sync:
                cb.setChecked(self.logic_checkboxes[key].isChecked())
        self.data_changed.emit()

    def add_custom_subtype(self):
        """添加自定义种族"""
        sub_id = self.new_sub_id.value()
        sub_name = self.new_sub_name.text().strip()
        
        if not sub_name:
            QMessageBox.warning(self, "错误", "种族名称不能为空！")
            return
        if sub_id in config.SUBTYPES:
            QMessageBox.warning(self, "错误", f"ID {sub_id} 已经是内置种族，无法覆盖！")
            return
        if sub_id in config.CUSTOM_SUBTYPES:
            result = QMessageBox.question(self, "确认", f"ID {sub_id} 已存在自定义种族，是否覆盖？")
            if result != QMessageBox.Yes:
                return
            
        success, error_msg = config.save_custom_subtype(sub_id, sub_name)
        
        if success:
            self.new_sub_name.clear()
            self.new_sub_id.setValue(sub_id + 1)
            self.refresh_subtypes_grids() 
            QMessageBox.information(self, "成功", f"新种族 [{sub_id}] 已同步至本地库")
        else:
            QMessageBox.critical(self, "保存失败", f"无法写入本地文件：\n{error_msg}")

    def sync_to_model(self, model):
        model.logic_subtypes = [key for key, cb in self.logic_checkboxes.items() if cb.isChecked()]
        model.display_subtypes = [key for key, cb in self.display_checkboxes.items() if cb.isChecked()]
        
    def set_model(self, new_model):
        self.model = new_model
        self.update_ui(self.model)

    def update_ui(self, model):
        with signal_blocker(self, self.sync_subtypes_cb):
            self.sync_subtypes_cb.setChecked(False) 
            for key, cb in self.logic_checkboxes.items():
                cb.setChecked(key in model.logic_subtypes)
            for key, cb in self.display_checkboxes.items():
                cb.setEnabled(True)
                cb.setChecked(key in model.display_subtypes)