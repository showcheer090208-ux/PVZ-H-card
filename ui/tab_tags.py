# ui/tab_tags.py
"""标签配置标签页 - 移除硬编码样式，由全局主题控制"""

import re
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QLineEdit, 
                               QListWidget, QAbstractItemView, QCheckBox, 
                               QListWidgetItem, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal
import config
from core_utils import signal_blocker


class TabTags(QWidget):
    data_changed = Signal()

    def __init__(self):
        super().__init__()
        self.model = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.sync_tags_cb = QCheckBox("保持【逻辑标签】自动同步到【显示标签】")
        self.sync_tags_cb.setChecked(True)
        self.sync_tags_cb.stateChanged.connect(self.on_sync_tags_toggled)
        layout.addWidget(self.sync_tags_cb)

        # 移除内联样式，由全局主题控制
        logic_group = QGroupBox("底层逻辑标签 (实际生效，例如: destroy)")
        logic_layout = QVBoxLayout()
        self.logic_tag_input = QLineEdit()
        self.logic_tag_input.setPlaceholderText("输入标签后按回车添加...")
        self.logic_tag_input.returnPressed.connect(self.add_logic_tag)
        logic_layout.addWidget(self.logic_tag_input)
        
        self.logic_tag_list = QListWidget()
        self.logic_tag_list.itemChanged.connect(self.on_logic_tag_changed)
        logic_layout.addWidget(self.logic_tag_list)
        logic_group.setLayout(logic_layout)
        layout.addWidget(logic_group)

        display_group = QGroupBox("UI显示标签 (仅作展示)")
        display_layout = QVBoxLayout()
        self.display_tag_input = QLineEdit()
        self.display_tag_input.setPlaceholderText("输入标签后按回车添加...")
        self.display_tag_input.returnPressed.connect(self.add_display_tag)
        self.display_tag_input.setEnabled(False) 
        display_layout.addWidget(self.display_tag_input)
        
        self.display_tag_list = QListWidget()
        self.display_tag_list.itemChanged.connect(self.on_display_tag_changed)
        display_layout.addWidget(self.display_tag_list)
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        btn_delete = QPushButton("删除选中的标签")
        btn_delete.clicked.connect(self.delete_selected_tag)
        layout.addWidget(btn_delete)

    def _get_raw_text(self, text):
        """从带序号的文本中提取原始内容"""
        return re.sub(r'^\d+\.\s*', '', text)

    def _renumber_list(self, list_widget):
        """重新编号列表项"""
        list_widget.blockSignals(True)
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            raw_text = self._get_raw_text(item.text())
            item.setText(f"{i + 1}. {raw_text}")
        list_widget.blockSignals(False)

    def create_editable_item(self, text):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def add_logic_tag(self):
        text = self.logic_tag_input.text().strip()
        if text:
            self.logic_tag_list.addItem(self.create_editable_item(text))
            self.logic_tag_input.clear()
            if self.sync_tags_cb.isChecked():
                self.display_tag_list.addItem(self.create_editable_item(text))
            self._renumber_list(self.logic_tag_list)
            self._renumber_list(self.display_tag_list)
            self.data_changed.emit()

    def add_display_tag(self):
        text = self.display_tag_input.text().strip()
        if text:
            self.display_tag_list.addItem(self.create_editable_item(text))
            self.display_tag_input.clear()
            self._renumber_list(self.display_tag_list)
            self.data_changed.emit()

    def on_logic_tag_changed(self, item):
        self._renumber_list(self.logic_tag_list)
        self.data_changed.emit()

    def on_display_tag_changed(self, item):
        self._renumber_list(self.display_tag_list)
        self.data_changed.emit()

    def delete_selected_tag(self):
        """删除选中的标签"""
        # 删除逻辑标签
        for item in self.logic_tag_list.selectedItems():
            row = self.logic_tag_list.row(item)
            self.logic_tag_list.takeItem(row)
            if self.sync_tags_cb.isChecked():
                raw_text = self._get_raw_text(item.text())
                for i in range(self.display_tag_list.count()):
                    if self._get_raw_text(self.display_tag_list.item(i).text()) == raw_text:
                        self.display_tag_list.takeItem(i)
                        break

        # 删除显示标签
        for item in self.display_tag_list.selectedItems():
            self.display_tag_list.takeItem(self.display_tag_list.row(item))
            
        self._renumber_list(self.logic_tag_list)
        self._renumber_list(self.display_tag_list)
        self.data_changed.emit()

    def on_sync_tags_toggled(self, state):
        is_sync = state == Qt.Checked.value
        self.display_tag_input.setEnabled(not is_sync)
        if is_sync:
            self.display_tag_list.clear()
            for i in range(self.logic_tag_list.count()):
                raw_text = self._get_raw_text(self.logic_tag_list.item(i).text())
                self.display_tag_list.addItem(self.create_editable_item(raw_text))
            self._renumber_list(self.display_tag_list)
        self.data_changed.emit()

    def sync_to_model(self, model):
        model.logic_tags = [self._get_raw_text(self.logic_tag_list.item(i).text()) for i in range(self.logic_tag_list.count())]
        model.display_tags = [self._get_raw_text(self.display_tag_list.item(i).text()) for i in range(self.display_tag_list.count())]

    def set_model(self, new_model):
        self.model = new_model
        self.update_ui(self.model)

    def update_ui(self, model):
        with signal_blocker(self, self.sync_tags_cb, self.logic_tag_list, self.display_tag_list):
            self.sync_tags_cb.setChecked(False)
            self.logic_tag_list.clear()
            for tag in model.logic_tags:
                self.logic_tag_list.addItem(self.create_editable_item(tag))
                
            self.display_tag_list.clear()
            for tag in model.display_tags:
                self.display_tag_list.addItem(self.create_editable_item(tag))
                
            self._renumber_list(self.logic_tag_list)
            self._renumber_list(self.display_tag_list)
            self.display_tag_input.setEnabled(True)