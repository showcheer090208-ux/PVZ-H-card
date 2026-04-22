# ui/tab_abilities.py
"""特殊能力标签页 - 移除硬编码样式，由全局主题控制"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, 
                               QSpinBox, QComboBox, QScrollArea, QLabel, 
                               QGroupBox, QPushButton, QFrame)
from PySide6.QtCore import Signal, Qt
import config
from core_utils import signal_blocker


class AbilityRow(QFrame):
    """动态能力行：包含名称/参数和删除按钮"""
    removed = Signal(object)
    changed = Signal()

    def __init__(self, ability_type, data=None):
        super().__init__()
        self.ability_type = ability_type  # "DoubleStrike", "Overshoot", or "Custom"
        
        # 不再设置内联样式，由全局主题的 AbilityRow 规则控制
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # 1. 标签
        name_map = {"DoubleStrike": "💥 双重攻击", "Overshoot": "🎯 先攻", "Custom": "🧩 自定义能力"}
        self.label = QLabel(name_map.get(ability_type, "未知能力"))
        self.label.setMinimumWidth(100)
        self.label.setStyleSheet("font-weight: bold; border: none;")
        layout.addWidget(self.label)

        # 2. 参数控件
        self.params = data or {"g": 0, "vt": 0, "va": 0}
        self.val_input = None
        self.guid_input = None
        self.vt_input = None

        if ability_type == "Overshoot":
            self.params["g"] = 564
            self.params["vt"] = 1
            self.val_input = QSpinBox()
            self.val_input.setMinimumHeight(28)
            self.val_input.setRange(1, 99)
            self.val_input.setPrefix("伤害: ")
            self.val_input.setValue(self.params.get("va", 2))
            self.val_input.valueChanged.connect(lambda x: self.changed.emit())
            layout.addWidget(self.val_input)
            
        elif ability_type == "DoubleStrike":
            self.params = {"g": 562, "vt": 0, "va": 0}
            layout.addStretch()
            
        elif ability_type == "Custom":
            self.guid_input = QSpinBox()
            self.guid_input.setMinimumHeight(28)
            self.guid_input.setRange(0, 9999)
            self.guid_input.setPrefix("ID: ")
            self.guid_input.setValue(self.params.get("g", 0))
            self.guid_input.valueChanged.connect(lambda x: self.changed.emit())
            
            self.vt_input = QComboBox()
            self.vt_input.setMinimumHeight(28)
            self.vt_input.addItem("固定数值 (0)", 0)
            self.vt_input.addItem("百分比 (1)", 1)
            self.vt_input.addItem("倍数 (2)", 2)
            self.vt_input.setCurrentIndex(self.params.get("vt", 0))
            self.vt_input.currentIndexChanged.connect(lambda x: self.changed.emit())
            
            self.val_input = QSpinBox()
            self.val_input.setMinimumHeight(28)
            self.val_input.setRange(0, 9999)
            self.val_input.setPrefix("数值: ")
            self.val_input.setValue(self.params.get("va", 0))
            self.val_input.valueChanged.connect(lambda x: self.changed.emit())
            
            layout.addWidget(self.guid_input)
            layout.addWidget(self.vt_input)
            layout.addWidget(self.val_input)

        layout.addStretch()

        # 3. 删除按钮 - 移除内联样式
        btn_del = QPushButton("❌")
        btn_del.setFixedSize(28, 28)
        btn_del.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(btn_del)

    def get_data(self):
        """获取当前行的能力数据"""
        if self.ability_type == "Overshoot":
            self.params["va"] = self.val_input.value() if self.val_input else 2
        elif self.ability_type == "Custom":
            if self.guid_input:
                self.params["g"] = self.guid_input.value()
            if self.vt_input:
                self.params["vt"] = self.vt_input.currentData()
            if self.val_input:
                self.params["va"] = self.val_input.value()
        return self.params.copy()


class TabAbilities(QWidget):
    data_changed = Signal()

    def __init__(self):
        super().__init__()
        self.ability_rows = [] 
        self.independent_widgets = {} 
        self.model = None
        self._setup_ui()

    def _on_any_change(self):
        """任何UI改变时触发"""
        if self.model:
            self.sync_to_model(self.model)
        self.data_changed.emit()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setSpacing(25)

        # --- 区域 A: 独立能力 (勾选框形式) ---
        basic_group = QGroupBox("✨ 基础特殊能力 (独立组件)")
        basic_layout = QVBoxLayout(basic_group)
        basic_layout.setContentsMargins(20, 25, 20, 20)
        basic_layout.setSpacing(12)
        
        # 遍历 config.SPECIAL_ABILITIES 创建控件
        for key, info in config.SPECIAL_ABILITIES.items():
            row_layout = QHBoxLayout()
            cb = QCheckBox(info["name"])
            cb.setMinimumWidth(180)
            cb.setMinimumHeight(28)
            row_layout.addWidget(cb)
            
            param_widget = None
            if info["type"] == "int":
                param_widget = QSpinBox()
                param_widget.setMinimumHeight(28)
                param_widget.setRange(1, 99)
                param_widget.setValue(info["default"])
                param_widget.setPrefix(f"{info['label']}: ")
                param_widget.setEnabled(False)
                row_layout.addWidget(param_widget)
            elif info["type"] in ["combo", "teamup_combo"]:
                param_widget = QComboBox()
                param_widget.setMinimumHeight(28)
                for opt_name, opt_val in info["options"].items():
                    param_widget.addItem(opt_name, opt_val)
                param_widget.setEnabled(False)
                row_layout.addWidget(param_widget)
                
            row_layout.addStretch()
            basic_layout.addLayout(row_layout)
            
            if param_widget:
                cb.toggled.connect(param_widget.setEnabled)
                cb.toggled.connect(lambda checked: self._on_any_change())
                if isinstance(param_widget, QSpinBox):
                    param_widget.valueChanged.connect(lambda x: self._on_any_change())
                elif isinstance(param_widget, QComboBox):
                    param_widget.currentIndexChanged.connect(lambda x: self._on_any_change())
            else:
                cb.stateChanged.connect(lambda state: self._on_any_change())
                
            self.independent_widgets[key] = {"cb": cb, "param": param_widget, "type": info["type"]}
        
        self.main_layout.addWidget(basic_group)

        # --- 区域 B: 赋予触发类能力 (动态列表) ---
        triggered_group = QGroupBox("⚡ 赋予触发类能力 (GrantedTriggeredAbilities)")
        self.triggered_layout = QVBoxLayout(triggered_group)
        self.triggered_layout.setContentsMargins(20, 25, 20, 20)
        self.triggered_layout.setSpacing(15)
        
        # 添加控制栏
        add_ctrl_layout = QHBoxLayout()
        add_ctrl_layout.setSpacing(15)
        
        self.ability_selector = QComboBox()
        self.ability_selector.setMinimumHeight(32)
        self.ability_selector.addItem("💥 双重攻击 (ID:562)", "DoubleStrike")
        self.ability_selector.addItem("🎯 先攻 (ID:564)", "Overshoot")
        self.ability_selector.addItem("🧩 自定义能力代码", "Custom")
        self.ability_selector.setMinimumWidth(220)
        add_ctrl_layout.addWidget(self.ability_selector)
        
        btn_add = QPushButton("➕ 添加至列表")
        btn_add.setMinimumHeight(32)
        # 移除内联样式，由全局主题控制
        btn_add.clicked.connect(lambda: self.add_ability_row())
        add_ctrl_layout.addWidget(btn_add)
        add_ctrl_layout.addStretch()
        
        self.triggered_layout.addLayout(add_ctrl_layout)
        
        # 分隔线 - 移除内联样式
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        self.triggered_layout.addWidget(line)

        # 存放动态行的容器
        self.rows_container = QVBoxLayout()
        self.rows_container.setSpacing(10)
        self.triggered_layout.addLayout(self.rows_container)
        self.triggered_layout.addStretch()
        
        self.main_layout.addWidget(triggered_group)
        self.main_layout.addStretch()
        
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def add_ability_row(self, data=None, ability_type=None):
        """添加新的能力行"""
        if ability_type is None:
            ability_type = self.ability_selector.currentData()
            
        row = AbilityRow(ability_type, data)
        row.removed.connect(self.remove_row)
        row.changed.connect(self._on_any_change)  
        self.rows_container.addWidget(row)
        self.ability_rows.append(row)
        self._on_any_change()

    def remove_row(self, row):
        """删除能力行"""
        self.rows_container.removeWidget(row)
        if row in self.ability_rows:
            self.ability_rows.remove(row)
        row.deleteLater()
        self._on_any_change()

    def clear_all_rows(self):
        """清空所有动态行"""
        for row in self.ability_rows[:]:
            self.remove_row(row)

    def sync_to_model(self, model):
        """将UI数据同步到Model"""
        if not model:
            return
            
        # 1. 同步触发类能力列表
        model.triggered_abilities = [row.get_data() for row in self.ability_rows]
        
        # 2. 同步独立能力字典
        abilities_data = {}
        for key, widgets in self.independent_widgets.items():
            if widgets["cb"].isChecked():
                val = True
                if widgets["type"] == "int":
                    val = widgets["param"].value()
                elif widgets["type"] in ["combo", "teamup_combo"]:
                    val = widgets["param"].currentData()
                abilities_data[key] = val
        model.components_abilities = abilities_data

    def set_model(self, new_model):
        """设置模型并更新UI"""
        self.model = new_model
        self.update_ui(self.model)
        
    def update_ui(self, model):
        """从Model更新UI"""
        if not model:
            return
            
        with signal_blocker(self):
            # 更新独立能力部分
            for key, widgets in self.independent_widgets.items():
                if key in model.components_abilities:
                    widgets["cb"].setChecked(True)
                    val = model.components_abilities[key]
                    if widgets["type"] == "int" and widgets["param"]:
                        widgets["param"].setValue(int(val))
                    elif widgets["type"] in ["combo", "teamup_combo"] and widgets["param"]:
                        idx = widgets["param"].findData(val)
                        if idx >= 0:
                            widgets["param"].setCurrentIndex(idx)
                else:
                    widgets["cb"].setChecked(False)
            
            # 更新触发类能力部分
            self.clear_all_rows()
            for item in model.triggered_abilities:
                g = item.get("g", 0)
                atype = "Custom"
                if g == 562:
                    atype = "DoubleStrike"
                elif g == 564:
                    atype = "Overshoot"
                
                row = AbilityRow(atype, item)
                row.removed.connect(self.remove_row)
                row.changed.connect(self._on_any_change)
                self.rows_container.addWidget(row)
                self.ability_rows.append(row)