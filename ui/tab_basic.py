# ui/tab_basic.py
"""基础属性标签页 - 移除硬编码样式，由全局主题控制"""

import uuid
import json
import os
from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QSpinBox, 
                               QComboBox, QPushButton, QHBoxLayout, QCheckBox, 
                               QGroupBox, QVBoxLayout, QScrollArea, QLabel, QGridLayout, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal
import config
from core_utils import signal_blocker

class TabBasic(QWidget):
    data_changed = Signal()
    save_requested = Signal()        # 信号：请求保存到工程
    import_requested = Signal(str, int) # 信号：请求从外部路径导入指定 GUID 的卡牌

    def __init__(self, initial_model=None):
        super().__init__()
        self.root_ability_checkboxes = {} 
        self.model = initial_model
        self._setup_ui()
        if self.model:
            self.update_ui(self.model)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # ================= ⚡ 快速操作栏 =================
        quick_group = QGroupBox("⚡ 快速操作")
        quick_layout = QVBoxLayout(quick_group)
        
        # 1. 保存按钮与提示
        save_btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 保存当前修改到工程 (Ctrl + S)")
        self.btn_save.setMinimumHeight(40)
        self.btn_save.setToolTip("保存后，修改将记录在当前加载的 .phantom 工程文件中")
        self.btn_save.clicked.connect(self.save_requested.emit) # 点击触发保存信号
        
        hint_label = QLabel("💡 提示：在软件任何 Tab 按下 Ctrl + S 均可快速保存")
        hint_label.setStyleSheet("color: #888; font-size: 11px;")
        
        save_btn_layout.addWidget(self.btn_save, 3)
        save_btn_layout.addWidget(hint_label, 2)
        quick_layout.addLayout(save_btn_layout)

        # 2. 从原始 JSON 导入区域
        import_layout = QHBoxLayout()
        import_layout.addWidget(QLabel("从 JSON 导入:"))
        
        self.import_path_edit = QLineEdit()
        self.import_path_edit.setPlaceholderText("选择原始 card_data_1.json...")
        # 自动填入默认路径提高效率
        default_json = os.path.join(os.getcwd(), "data", "card_data_1.json")
        if os.path.exists(default_json):
            self.import_path_edit.setText(default_json)
            
        btn_browse = QPushButton("浏览...")
        btn_browse.clicked.connect(self._browse_import_path)
        
        self.import_guid_spin = QSpinBox()
        self.import_guid_spin.setRange(1, 2147483647)
        self.import_guid_spin.setPrefix("GUID: ")
        
        btn_do_import = QPushButton("⬇️ 导入到工作台")
        btn_do_import.clicked.connect(self._handle_import_click)

        import_layout.addWidget(self.import_path_edit, 3)
        import_layout.addWidget(btn_browse, 1)
        import_layout.addWidget(self.import_guid_spin, 1)
        import_layout.addWidget(btn_do_import, 2)
        quick_layout.addLayout(import_layout)

        main_layout.addWidget(quick_group)

        # ================= 原有属性编辑区 =================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form = QFormLayout(container)

        # 1. 标识与预制体
        guid_group = QGroupBox("标识与预制体")
        guid_form = QFormLayout()
        self.guid_spin = QSpinBox()
        self.guid_spin.setRange(1, 2147483647)
        guid_form.addRow("GUID:", self.guid_spin)
        self.card_name_display = QLineEdit()
        self.card_name_display.setReadOnly(True)
        self.card_name_display.setPlaceholderText("自动读取...")
        guid_form.addRow("本地译名:", self.card_name_display)
        self.prefab_input = QLineEdit()
        guid_form.addRow("Prefab:", self.prefab_input)
        guid_group.setLayout(guid_form)
        form.addRow(guid_group)

        # 2. 卡牌定义
        type_group = QGroupBox("卡牌定义 (分类、系列)")
        type_form = QFormLayout()
        self.faction_combo = QComboBox()
        for key, val in config.FACTIONS.items(): self.faction_combo.addItem(val, key)
        type_form.addRow("阵营 (Faction):", self.faction_combo)
        self.baseid_combo = QComboBox()
        for key, val in config.BASE_IDS.items(): self.baseid_combo.addItem(val, key)
        type_form.addRow("类型 (Base ID):", self.baseid_combo)
        self.color_combo = QComboBox()
        for key, val in config.COLORS.items(): self.color_combo.addItem(val, key)
        type_form.addRow("职业 (Color):", self.color_combo)
        self.rarity_combo = QComboBox()
        for key, info in config.RARITIES.items(): self.rarity_combo.addItem(info["name"], key)
        type_form.addRow("稀有度 (Rarity):", self.rarity_combo)
        self.set_combo = QComboBox()
        for key, val in config.SETS.items(): self.set_combo.addItem(val, key)
        type_form.addRow("系列 (Set):", self.set_combo)
        self.set_rarity_key_input = QLineEdit()
        type_form.addRow("系列/稀有度主键:", self.set_rarity_key_input)
        type_group.setLayout(type_form)
        form.addRow(type_group)

        # 3. 合成与数值
        stats_group = QGroupBox("数值与造价")
        stats_form = QFormLayout()
        craft_layout = QHBoxLayout()
        self.craft_buy_spin = QSpinBox()
        self.craft_buy_spin.setRange(0, 2147483647)
        self.craft_sell_spin = QSpinBox()
        self.craft_sell_spin.setRange(0, 2147483647)
        craft_layout.addWidget(QLabel("买:"))
        craft_layout.addWidget(self.craft_buy_spin)
        craft_layout.addWidget(QLabel("卖:"))
        craft_layout.addWidget(self.craft_sell_spin)
        stats_form.addRow("火花造价:", craft_layout)
        self.cost_spin = QSpinBox()
        self.cost_spin.setRange(0, 2147483647)
        stats_form.addRow("费用:", self.cost_spin)
        attack_layout = QHBoxLayout()
        self.attack_cb = QCheckBox("启用")
        self.attack_spin = QSpinBox()
        self.attack_spin.setRange(0, 2147483647)
        self.attack_cb.toggled.connect(self.attack_spin.setEnabled)
        attack_layout.addWidget(self.attack_cb)
        attack_layout.addWidget(self.attack_spin)
        stats_form.addRow("攻击:", attack_layout)
        health_layout = QHBoxLayout()
        self.health_cb = QCheckBox("启用")
        self.health_spin = QSpinBox()
        self.health_spin.setRange(0, 2147483647)
        self.health_cb.toggled.connect(self.health_spin.setEnabled)
        health_layout.addWidget(self.health_cb)
        health_layout.addWidget(self.health_spin)
        stats_form.addRow("生命:", health_layout)
        stats_group.setLayout(stats_form)
        form.addRow(stats_group)

        # 4. Flags
        flags_group = QGroupBox("核心标记 (Flags)")
        flags_layout = QGridLayout()
        self.flag_ignore_limit = QCheckBox("无视上限")
        self.flag_is_power = QCheckBox("超能力")
        self.flag_is_primary_power = QCheckBox("英雄大招")
        self.flag_is_trick = QCheckBox("锦囊")
        self.flag_is_surprise = QCheckBox("僵尸回合打出")
        self.flag_is_env = QCheckBox("环境")
        self.flag_is_board = QCheckBox("场景能力")
        flags_layout.addWidget(self.flag_ignore_limit, 0, 0)
        flags_layout.addWidget(self.flag_is_power, 0, 1)
        flags_layout.addWidget(self.flag_is_primary_power, 0, 2)
        flags_layout.addWidget(self.flag_is_trick, 1, 0)
        flags_layout.addWidget(self.flag_is_surprise, 1, 1)
        flags_layout.addWidget(self.flag_is_env, 1, 2)
        flags_layout.addWidget(self.flag_is_board, 1, 3)
        flags_group.setLayout(flags_layout)
        form.addRow(flags_group)

        # 5. UI 能力标签
        abilities_group = QGroupBox("UI 能力标签 (special_abilities)")
        abilities_layout = QVBoxLayout()
        for key, note in config.ROOT_ABILITY_PRESETS.items():
            cb = QCheckBox(f"{key} - {note}")
            cb.stateChanged.connect(lambda *args: self.data_changed.emit())
            self.root_ability_checkboxes[key] = cb
            abilities_layout.addWidget(cb)
        abilities_group.setLayout(abilities_layout)
        form.addRow(abilities_group)

        # 6. Affinities
        affinities_group = QGroupBox("AI 倾向性 (Affinities)")
        aff_form = QFormLayout()
        self.sub_aff_input = QLineEdit()
        aff_form.addRow("种族倾向:", self.sub_aff_input)
        self.sub_aff_w_input = QLineEdit()
        aff_form.addRow("种族权重:", self.sub_aff_w_input)
        self.tag_aff_input = QLineEdit()
        aff_form.addRow("标签倾向:", self.tag_aff_input)
        self.tag_aff_w_input = QLineEdit()
        aff_form.addRow("标签权重:", self.tag_aff_w_input)
        self.card_aff_input = QLineEdit()
        aff_form.addRow("卡牌倾向:", self.card_aff_input)
        self.card_aff_w_input = QLineEdit()
        aff_form.addRow("卡牌权重:", self.card_aff_w_input)
        affinities_group.setLayout(aff_form)
        form.addRow(affinities_group)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # 信号绑定
        self.guid_spin.valueChanged.connect(self.refresh_card_name)
        self.baseid_combo.currentIndexChanged.connect(self.on_card_type_changed)
        self.faction_combo.currentIndexChanged.connect(self.on_card_type_changed)
        
        input_widgets = [
            self.guid_spin, self.cost_spin, self.attack_spin, self.health_spin, 
            self.craft_buy_spin, self.craft_sell_spin, self.color_combo, 
            self.rarity_combo, self.set_combo, self.prefab_input, 
            self.set_rarity_key_input, self.sub_aff_input, self.sub_aff_w_input, 
            self.tag_aff_input, self.tag_aff_w_input, self.card_aff_input, 
            self.card_aff_w_input, self.attack_cb, self.health_cb, 
            self.flag_ignore_limit, self.flag_is_power, self.flag_is_primary_power,
            self.flag_is_trick, self.flag_is_surprise, self.flag_is_env, self.flag_is_board
        ]

        for widget in input_widgets:
            if isinstance(widget, (QSpinBox, QComboBox)):
                if isinstance(widget, QComboBox):
                    widget.currentIndexChanged.connect(lambda *args: self.data_changed.emit())
                else:
                    widget.valueChanged.connect(lambda *args: self.data_changed.emit())
            elif isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda *args: self.data_changed.emit())
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(lambda *args: self.data_changed.emit())

    def _browse_import_path(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择原始 JSON 数据池", "", "JSON Files (*.json)")
        if path: self.import_path_edit.setText(path)

    def _handle_import_click(self):
        path = self.import_path_edit.text().strip()
        guid = self.import_guid_spin.value()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "错误", "导入路径不正确！")
            return
        self.import_requested.emit(path, guid)

    def refresh_card_name(self):
        guid = self.guid_spin.value()
        card_info = config.KNOWN_CARDS.get(guid)
        self.card_name_display.setText(card_info["name"] if card_info else "未知/自定义卡牌")
        self.data_changed.emit()

    def on_card_type_changed(self):
        base_id = self.baseid_combo.currentData() or ""
        faction = self.faction_combo.currentData() or ""
        
        is_board_template = (base_id == "BoardAbility")
        is_trick = "OneTimeEffect" in base_id and not is_board_template
        is_env = "Environment" in base_id
        is_fighter = not is_trick and not is_env and not is_board_template
        is_zombie = "Zombies" in faction

        with signal_blocker(self.attack_cb, self.health_cb, self.flag_is_trick, 
                            self.flag_is_surprise, self.flag_is_env, self.flag_is_board):
            self.attack_cb.setChecked(is_fighter)
            self.health_cb.setChecked(is_fighter)
            self.attack_spin.setEnabled(is_fighter)
            self.health_spin.setEnabled(is_fighter)
            self.flag_is_trick.setChecked(is_trick)
            self.flag_is_env.setChecked(is_env)
            self.flag_is_surprise.setChecked(is_zombie and (is_trick or is_env))
            self.flag_is_board.setChecked(is_board_template)
        self.data_changed.emit()

    def _parse_csv_to_list(self, text, as_type=str):
        return [as_type(item.strip()) for item in text.split(',') if item.strip()]

    def sync_to_model(self, model):
        model.guid = self.guid_spin.value()
        model.prefab_name = self.prefab_input.text().strip()
        model.faction = self.faction_combo.currentData() 
        model.base_id = self.baseid_combo.currentData()
        model.color = self.color_combo.currentData()
        model.rarity_key = self.rarity_combo.currentData()
        model.set_name = self.set_combo.currentData()
        model.set_and_rarity_key = self.set_rarity_key_input.text().strip()
        model.crafting_buy = self.craft_buy_spin.value()
        model.crafting_sell = self.craft_sell_spin.value()
        model.cost = self.cost_spin.value()
        model.has_attack = self.attack_cb.isChecked()
        model.attack = self.attack_spin.value()
        model.has_health = self.health_cb.isChecked()
        model.health = self.health_spin.value()
        
        model.ignore_deck_limit = self.flag_ignore_limit.isChecked()
        model.is_power = self.flag_is_power.isChecked()
        model.is_primary_power = self.flag_is_primary_power.isChecked()
        
        model.is_trick = self.flag_is_trick.isChecked()
        model.is_surprise = self.flag_is_surprise.isChecked()
        model.is_environment = self.flag_is_env.isChecked()
        model.is_board_ability = self.flag_is_board.isChecked()

        model.root_special_abilities = [key for key, cb in self.root_ability_checkboxes.items() if cb.isChecked()]
        model.subtype_affinities = self._parse_csv_to_list(self.sub_aff_input.text(), str)
        model.subtype_affinity_weights = self._parse_csv_to_list(self.sub_aff_w_input.text(), float)
        model.tag_affinities = self._parse_csv_to_list(self.tag_aff_input.text(), str)
        model.tag_affinity_weights = self._parse_csv_to_list(self.tag_aff_w_input.text(), float)
        model.card_affinities = self._parse_csv_to_list(self.card_aff_input.text(), int)
        model.card_affinity_weights = self._parse_csv_to_list(self.card_aff_w_input.text(), float)

    def _set_combo_by_data(self, combo, target_data):
        if target_data is None: return
        idx = combo.findData(target_data)
        if idx == -1 and isinstance(target_data, str):
            for i in range(combo.count()):
                if str(combo.itemData(i)).lower() == target_data.lower():
                    idx = i
                    break
        if idx >= 0: combo.setCurrentIndex(idx)

    def set_model(self, new_model):
        self.model = new_model
        self.update_ui(self.model)

    def update_ui(self, model):
        with signal_blocker(self, self.baseid_combo, self.faction_combo, self.attack_cb, self.health_cb, 
                            self.flag_is_trick, self.flag_is_surprise, self.flag_is_env, self.flag_is_board):
            self.guid_spin.setValue(model.guid)
            self.refresh_card_name() 
            self.prefab_input.setText(model.prefab_name)
            
            self._set_combo_by_data(self.faction_combo, model.faction)
            self._set_combo_by_data(self.baseid_combo, model.base_id)
            self._set_combo_by_data(self.color_combo, model.color)
            self._set_combo_by_data(self.rarity_combo, model.rarity_key)
            self._set_combo_by_data(self.set_combo, model.set_name)
            
            self.set_rarity_key_input.setText(model.set_and_rarity_key)
            self.craft_buy_spin.setValue(model.crafting_buy)
            self.craft_sell_spin.setValue(model.crafting_sell)
            self.cost_spin.setValue(model.cost)
            
            self.attack_cb.setChecked(model.has_attack)
            self.attack_spin.setEnabled(model.has_attack)
            self.attack_spin.setValue(model.attack)
            
            self.health_cb.setChecked(model.has_health)
            self.health_spin.setEnabled(model.has_health)
            self.health_spin.setValue(model.health)
            
            self.flag_ignore_limit.setChecked(model.ignore_deck_limit)
            self.flag_is_power.setChecked(model.is_power)
            self.flag_is_primary_power.setChecked(model.is_primary_power)
            
            self.flag_is_trick.setChecked(model.is_trick)
            self.flag_is_surprise.setChecked(model.is_surprise)
            self.flag_is_env.setChecked(model.is_environment)
            self.flag_is_board.setChecked(model.is_board_ability)
            
            for key, cb in self.root_ability_checkboxes.items():
                cb.setChecked(key in model.root_special_abilities)
                
            self.sub_aff_input.setText(", ".join(map(str, model.subtype_affinities)))
            self.sub_aff_w_input.setText(", ".join(map(str, model.subtype_affinity_weights)))
            self.tag_aff_input.setText(", ".join(model.tag_affinities))
            self.tag_aff_w_input.setText(", ".join(map(str, model.tag_affinity_weights)))
            self.card_aff_input.setText(", ".join(map(str, model.card_affinities)))
            self.card_aff_w_input.setText(", ".join(map(str, model.card_affinity_weights)))