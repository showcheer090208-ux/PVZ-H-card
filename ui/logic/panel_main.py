# ui/logic/panel_main.py
"""技能逻辑主面板 - 移除硬编码样式，由全局主题控制"""

import copy
from PySide6.QtWidgets import (QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidgetItem, 
                               QPushButton, QMenu, QMessageBox, QApplication,
                               QSplitter, QGroupBox, QTextEdit, QInputDialog, QTabWidget, QTabBar)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QKeySequence, QShortcut

import logic_library 
import localization 
import logic_presets 
from logic_translator import translate_entities_to_text 
from ui.logic.tree_widget import LogicTreeWidget
from ui.logic.inspector import LogicInspector 
from ui.logic.history import LogicHistoryManager 
from core_utils import signal_blocker


class LogicNodeItem(QTreeWidgetItem):
    """智能逻辑树节点：自我管理数据存储与文本渲染"""
    
    def __init__(self, parent_or_tree, node_id, params, is_disabled=False):
        super().__init__(parent_or_tree)
        self.setData(0, Qt.UserRole, node_id)
        self.setData(1, Qt.UserRole, params)
        self.setData(2, Qt.UserRole, is_disabled)
        self.refresh_text()

    def refresh_text(self):
        """根据自身数据自动渲染界面文本"""
        node_id = self.data(0, Qt.UserRole)
        params = self.data(1, Qt.UserRole)
        is_disabled = self.data(2, Qt.UserRole)
        defn = logic_library.NODE_DEF.get(node_id, {})

        if node_id == "AbilityGroup":
            n_name = "📦 技能组"
        elif node_id == "AdditionalTargetQuery":
            n_name = localization.NODE_NAMES.get("AdditionalTargetQuery", "📦 额外目标条件")
        elif node_id == "FinderPlaceholder":
            n_name = "🔍 查找范围 (Finder)"
        elif node_id == "QueryPlaceholder":
            n_name = "📋 满足条件 (Query)"
        else:
            n_name = localization.NODE_NAMES.get(node_id, node_id)

        if defn.get("allowed_children") or node_id in ["AdditionalTargetQuery", "FinderPlaceholder", "QueryPlaceholder"]:
            n_name += "  🖱️"
            
        self.setText(0, n_name)

        editable_keys = defn.get("editable_params", {}).keys()
        if editable_keys and params:
            param_text = ", ".join([
                f"{localization.PARAM_NAMES.get(k, k)}: {localization.ENUM_NAMES.get(v, v) if isinstance(v, str) else v}" 
                for k, v in params.items() if k in editable_keys
            ])
            self.setText(1, param_text)
        else:
            self.setText(1, "")

        font = self.font(0)
        font.setStrikeOut(bool(is_disabled))
        self.setFont(0, font)
        
        # 【修复】移除硬编码黑色，使用默认颜色（让主题 QSS 控制）
        # 禁用状态仍然使用灰色，启用状态不设置颜色（继承主题）
        if is_disabled:
            self.setForeground(0, Qt.gray)
        else:
            # 清空颜色设置，让父级样式表生效
            self.setData(0, Qt.ForegroundRole, None)
            # 或者
            self.setForeground(0, QBrush())

    def update_param(self, key, value):
        params = self.data(1, Qt.UserRole) or {}
        params[key] = value
        self.setData(1, Qt.UserRole, params)
        self.refresh_text()
    
    def treeWidget(self):
        return super().treeWidget()


class LogicNodeAdapter:
    """节点逻辑适配器"""
    
    @staticmethod
    def to_entity_data(node_id, item, parse_func, defn):
        data = copy.deepcopy(item.data(1, Qt.UserRole)) if item.data(1, Qt.UserRole) else {}
        
        if node_id in ["PrimaryTargetFilter", "SecondaryTargetFilter"]:
            main_query, add_query = None, None
            for i in range(item.childCount()):
                child_item = item.child(i)
                if child_item.data(2, Qt.UserRole):
                    continue
                c_id = child_item.data(0, Qt.UserRole)
                if c_id == "AdditionalTargetQuery":
                    if child_item.childCount() > 0:
                        add_query = parse_func(child_item.child(0))
                else:
                    if main_query is None:
                        main_query = parse_func(child_item)
            data["Query"] = main_query
            data["AdditionalTargetQuery"] = add_query
            return data

        if node_id == "QueryEntityCondition":
            for i in range(item.childCount()):
                child_item = item.child(i)
                if child_item.data(2, Qt.UserRole):
                    continue
                c_id = child_item.data(0, Qt.UserRole)
                if c_id == "FinderPlaceholder" and child_item.childCount() > 0:
                    data["Finder"] = parse_func(child_item.child(0))
                elif c_id == "QueryPlaceholder" and child_item.childCount() > 0:
                    data["Query"] = parse_func(child_item.child(0))
            return data

        child_prop = defn.get("child_prop")
        if child_prop:
            child_data = [res for i in range(item.childCount()) if (res := parse_func(item.child(i)))]
            data[child_prop] = child_data if defn.get("is_list") else (child_data[0] if child_data else None)
        return data

    @staticmethod
    def extract_build_data(node_id, cdata, defn):
        params, children = {}, []
        if node_id in ["PrimaryTargetFilter", "SecondaryTargetFilter"]:
            for k, v in cdata.items():
                if k == "Query":
                    if v:
                        children.append(("main", v))
                elif k == "AdditionalTargetQuery":
                    if v:
                        children.append(("additional", v))
                else:
                    params[k] = v
            if params.get("AdditionalTargetType") == "Query" and not any(t == "additional" for t, _ in children):
                children.append(("additional", None))
            return params, children

        if node_id == "QueryEntityCondition":
            for k, v in cdata.items():
                if k == "Finder":
                    if v:
                        children.append(("finder", v))
                elif k == "Query":
                    if v:
                        children.append(("query", v))
                else:
                    params[k] = v
            return params, children

        child_prop = defn.get("child_prop")
        for k, v in cdata.items():
            if k == child_prop:
                children_list = v if isinstance(v, list) else [v]
                for c in children_list:
                    if c:
                        children.append(("normal", c))
            else:
                params[k] = v
        return params, children

    @staticmethod
    def build_special_children(child_item, children_data, build_func):
        for child_type, child_comp in children_data:
            if child_type == "additional":
                add_folder = LogicNodeItem(child_item, "AdditionalTargetQuery", {}, False)
                if child_comp:
                    build_func(add_folder, child_comp)
            elif child_type in ["finder", "query"]:
                placeholder_id = "FinderPlaceholder" if child_type == "finder" else "QueryPlaceholder"
                placeholder_item = LogicNodeItem(child_item, placeholder_id, {}, False)
                if child_comp:
                    build_func(placeholder_item, child_comp)
            else:
                if child_comp:
                    build_func(child_item, child_comp)

    @staticmethod
    def to_snapshot_dict(node_id, item, parse_dict_func):
        if node_id == "QueryEntityCondition":
            finder_data, query_data = None, None
            for i in range(item.childCount()):
                child = item.child(i)
                child_id = child.data(0, Qt.UserRole)
                if child_id == "FinderPlaceholder" and child.childCount() > 0:
                    finder_data = parse_dict_func(child.child(0))
                elif child_id == "QueryPlaceholder" and child.childCount() > 0:
                    query_data = parse_dict_func(child.child(0))
            return {
                "node_id": node_id,
                "params": copy.deepcopy(item.data(1, Qt.UserRole)) if item.data(1, Qt.UserRole) else {},
                "disabled": item.data(2, Qt.UserRole) or False,
                "finder": finder_data, "query": query_data
            }

        if node_id == "EffectValueDescriptor":
            params = copy.deepcopy(item.data(1, Qt.UserRole)) if item.data(1, Qt.UserRole) else {}
            mapping_type = params.get("MappingType", "DamageToHeal")
            dest_to_source_map = {"HealAmount": "DamageAmount"} if mapping_type == "DamageToHeal" else {"DamageAmount": "HealAmount"}
            return {
                "node_id": node_id, "params": {"DestToSourceMap": dest_to_source_map},
                "disabled": item.data(2, Qt.UserRole) or False, "children": []
            }

        return {
            "node_id": node_id,
            "params": copy.deepcopy(item.data(1, Qt.UserRole)) if item.data(1, Qt.UserRole) else {},
            "disabled": item.data(2, Qt.UserRole) or False,
            "children": [parse_dict_func(item.child(i)) for i in range(item.childCount())]
        }

    @staticmethod
    def restore_snapshot_children(node_id, child_item, data_dict, restore_func):
        if node_id == "QueryEntityCondition":
            finder_item = LogicNodeItem(child_item, "FinderPlaceholder", {}, False)
            if data_dict.get("finder"):
                restore_func(finder_item, data_dict["finder"])
            query_item = LogicNodeItem(child_item, "QueryPlaceholder", {}, False)
            if data_dict.get("query"):
                restore_func(query_item, data_dict["query"])
            return
        
        for sub in data_dict.get("children", []):
            restore_func(child_item, sub)


class PanelLogic(QWidget):
    data_changed = Signal()

    def __init__(self):
        super().__init__()
        self.model = None
        self._setup_ui()
        self._populate_palette()
        self._setup_shortcuts()

    def _populate_palette(self):
        self.palette_tree.clear()
        
        # 预设根节点
        preset_root = QTreeWidgetItem(self.palette_tree, ["⭐ 我的自定义预设"])
        preset_root.setData(0, Qt.UserRole, "Category")
        for p_name in logic_presets.USER_PRESETS.keys():
            item = QTreeWidgetItem(preset_root, [p_name])
            item.setData(0, Qt.UserRole, "Preset")
            item.setData(1, Qt.UserRole, p_name)

        # 分类定义
        cats = {
            "Trigger": "🟢 触发器", 
            "Filter": "🟡 过滤器", 
            "TargetSelector": "🟠 目标选取", 
            "CompositeQuery": "🔗 复合逻辑门", 
            "Query": "🔵 原子条件", 
            "Effect": "🔴 基础执行",
            "ComplexEffect": "🟥 复合执行 (需条件)" 
        }
        cat_items = {k: QTreeWidgetItem(self.palette_tree, [v]) for k, v in cats.items()}
        for item in cat_items.values():
            item.setData(0, Qt.UserRole, "Category")

        # 子分类
        sub_categories = {
            "Query": {
                "🧍 实体与阵营": ["FighterQuery", "IsAliveQuery", "SameFactionQuery", "HasZombiesComponent", "HasPlantsComponent", "HasPlayerComponent", "TargetableInPlayFighterQuery", "TrickQuery", "IsActiveQuery"],
                "🗺️ 地形与位置": ["InLaneQuery", "InSameLaneQuery", "SameLaneAsTargetQuery", "AdjacentLaneQuery", "InAdjacentLaneQuery", "InLaneAdjacentToLaneQuery", "OnTerrainQuery", "OpenLaneQuery", "HasWaterTerrainComponent", "HasHighgroundTerrainComponent", "HasEnvironmentComponent", "HasLaneComponent", "InEnvironmentQuery", "BehindSameLaneQuery", "LastLaneOfSelfQuery", "InUnopposedLaneQuery", "InOneTimeEffectZoneQuery", "LaneOfIndexQuery"],
                "🖐️ 手牌与卡牌": ["InHandQuery", "DrawnCardQuery", "CardGuidQuery", "SubsetQuery", "SubtypeQuery"],
                "📊 数值与状态": ["AttackComparisonQuery", "HealthComparisonQuery", "DamageTakenComparisonQuery", "SunCostComparisonQuery", "SunCostPlusNComparisonQuery", "TurnCountQuery", "BlockMeterValueQuery", "SunCounterComparisonQuery"],
                "🎯 对象与指针": ["SelfQuery", "SourceQuery", "TargetQuery", "TargetCardGuidQuery", "OriginalTargetCardGuidQuery"],
            },
            "Effect": {
                "⚔️ 伤害与消灭": ["DamageEffect", "DestroyCardEffect"],
                "❤️ 治疗与增益": ["HealEffect", "BuffEffect", "SetStatEffect", "CopyStatsEffect", "TargetAttackMultiplier", "TargetHealthMultiplier", "HeroHealthMultiplier"],
                "🃏 卡牌与生成": ["DrawCardEffect", "CreateCardEffect", "CreateCardInDeckEffect", "CopyCardEffectDescriptor", "CreateCardFromSubsetEffectDescriptor", "TransformIntoCardFromSubsetEffectDescriptor"],
                "🏃 移动与控制": ["MoveCardToLanesEffectDescriptor", "ReturnToHandEffect", "SlowEffect", "MixedUpGravediggerEffectDescriptor", "TurnIntoGravestoneEffectDescriptor"],
                "☀️ 费用与阳光": ["GainSunEffect", "ModifySunCostEffect", "SunGainedMultiplier"],
                "✨ 能力赋予": ["GrantAbilityEffect", "GrantTriggeredAbilityEffectDescriptor", "ExtraAttackEffect"],
            },
            "Trigger": {
                "🃏 打出与离场": ["PlayTrigger", "DiscardFromPlayTrigger", "EnterBoardTrigger", "DestroyCardTrigger", "ReturnToHandTrigger"],
                "⚔️ 战斗阶段": ["CombatEndTrigger", "LaneCombatStartTrigger", "LaneCombatEndTrigger", "DamageTrigger", "ExtraAttackTrigger"],
                "⏳ 回合阶段": ["TurnStartTrigger", "RevealTrigger", "RevealPhaseEndTrigger", "SurprisePhaseStartTrigger"],
                "✨ 状态改变": ["BuffTrigger", "HealTrigger", "SlowedTrigger", "MoveTrigger", "DrawCardTrigger", "DrawCardFromSubsetTrigger"]
            }
        }

        sub_cat_items = {}
        for main_cat, sub_dict in sub_categories.items():
            if main_cat not in cat_items:
                continue
            for sub_name in sub_dict.keys():
                sub_item = QTreeWidgetItem(cat_items[main_cat], [f"📁 {sub_name}"])
                sub_item.setData(0, Qt.UserRole, "Category")
                sub_cat_items[f"{main_cat}_{sub_name}"] = sub_item

        # 填充节点
        for node_id, defn in logic_library.NODE_DEF.items():
            main_cat = defn.get("category")
            if main_cat not in cat_items:
                continue

            target_parent = cat_items[main_cat]
            
            if main_cat in sub_categories:
                found_sub = False
                for sub_name, node_list in sub_categories[main_cat].items():
                    if node_id in node_list:
                        target_parent = sub_cat_items[f"{main_cat}_{sub_name}"]
                        found_sub = True
                        break
                if not found_sub:
                    other_key = f"{main_cat}_其他未分类"
                    if other_key not in sub_cat_items:
                        sub_item = QTreeWidgetItem(cat_items[main_cat], ["📁 其他通用节点"])
                        sub_item.setData(0, Qt.UserRole, "Category")
                        sub_cat_items[other_key] = sub_item
                    target_parent = sub_cat_items[other_key]

            child = QTreeWidgetItem(target_parent, [localization.NODE_NAMES.get(node_id, node_id)])
            child.setData(0, Qt.UserRole, node_id)

        for item in cat_items.values():
            item.setExpanded(True)
        preset_root.setExpanded(True)

    def filter_palette(self, text=""):
        search_text = text.lower().strip()
        root = self.palette_tree.invisibleRootItem()

        def match_item(item):
            matches = search_text in item.text(0).lower()
            child_match = False
            for i in range(item.childCount()):
                if match_item(item.child(i)):
                    child_match = True
                    
            should_show = matches or child_match
            item.setHidden(not should_show)
            
            if search_text:
                if child_match:
                    item.setExpanded(True)
            else:
                if item.data(0, Qt.UserRole) == "Category" and item.parent() == root:
                    item.setExpanded(True)
                elif item.data(0, Qt.UserRole) == "Category" and item.parent() != root:
                    item.setExpanded(False)

            return should_show

        for i in range(root.childCount()):
            match_item(root.child(i))

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 工具栏
        toolbar = QHBoxLayout()
        
        self.btn_toggle_left = QPushButton("隐藏组件库")
        self.btn_toggle_left.setCheckable(True)
        self.btn_toggle_left.clicked.connect(self.toggle_left_panel)
        
        self.btn_toggle_right = QPushButton("隐藏检查器")
        self.btn_toggle_right.setCheckable(True)
        self.btn_toggle_right.clicked.connect(self.toggle_right_panel)

        btn_add_group = QPushButton("➕ 新建技能组")
        btn_add_group.clicked.connect(self.add_ability_group)
        
        btn_expand = QPushButton("📂 全部展开")
        btn_expand.clicked.connect(lambda: self.get_current_tree().expandAll() if self.get_current_tree() else None)
        btn_collapse = QPushButton("📁 全部折叠")
        btn_collapse.clicked.connect(lambda: self.get_current_tree().collapseAll() if self.get_current_tree() else None)
        
        self.btn_undo = QPushButton("↩️ 撤销")
        self.btn_undo.clicked.connect(self.undo)
        self.btn_undo.setEnabled(False)
        
        self.btn_redo = QPushButton("↪️ 重做")
        self.btn_redo.clicked.connect(self.redo)
        self.btn_redo.setEnabled(False)

        toolbar.addWidget(self.btn_toggle_left)
        toolbar.addWidget(btn_add_group)
        toolbar.addWidget(btn_expand)
        toolbar.addWidget(btn_collapse)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_undo)
        toolbar.addWidget(self.btn_redo)
        toolbar.addWidget(self.btn_toggle_right)
        main_layout.addLayout(toolbar)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # 左：组件库
        self.palette_group = QGroupBox("🎨 组件库 (右键管理预设)")
        palette_layout = QVBoxLayout(self.palette_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索组件 (支持中文/拼音)...")
        self.search_input.textChanged.connect(self.filter_palette)
        palette_layout.addWidget(self.search_input)

        self.palette_tree = LogicTreeWidget() 
        self.palette_tree.setDragDropMode(LogicTreeWidget.NoDragDrop) 
        self.palette_tree.itemDoubleClicked.connect(self.add_from_palette)
        self.palette_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.palette_tree.customContextMenuRequested.connect(self.show_palette_menu)
        
        palette_layout.addWidget(self.palette_tree)
        self.splitter.addWidget(self.palette_group)

        # 中：工作区
        outline_group = QGroupBox("🌳 工作区 (右键更换/禁用)")
        outline_layout = QVBoxLayout(outline_group)
        
        self.workspace_tabs = QTabWidget()
        self.workspace_tabs.setTabsClosable(True)
        self.workspace_tabs.tabCloseRequested.connect(self.close_sandbox_tab)
        
        self.tab_states = {} 
        self.card_tree = self._create_tree_widget()
        
        self.workspace_tabs.addTab(self.card_tree, "🃏 当前卡牌技能")
        self.workspace_tabs.tabBar().setTabButton(0, QTabBar.RightSide, None) 
        
        self.tab_states[self.card_tree] = {
            'type': 'card',
            'history': LogicHistoryManager(self, self.card_tree)
        }
        
        outline_layout.addWidget(self.workspace_tabs)
        self.splitter.addWidget(outline_group)

        # 右：检查器
        self.right_widget = QWidget()
        right_layout = QVBoxLayout(self.right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_splitter = QSplitter(Qt.Vertical)
        
        self.inspector = LogicInspector()
        self.inspector.param_updated.connect(self._on_param_updated)
        self.right_splitter.addWidget(self.inspector)

        desc_group = QGroupBox("📝 技能自然语言描述")
        desc_layout = QVBoxLayout(desc_group)
        self.desc_preview = QTextEdit()
        self.desc_preview.setReadOnly(True)
        # 移除内联样式，由全局主题控制
        desc_layout.addWidget(self.desc_preview)
        self.right_splitter.addWidget(desc_group)
        
        self.right_splitter.setStretchFactor(0, 3)
        self.right_splitter.setStretchFactor(1, 1)
        right_layout.addWidget(self.right_splitter)
        self.splitter.addWidget(self.right_widget)

        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 4)
        self.splitter.setStretchFactor(2, 3)

        self.workspace_tabs.currentChanged.connect(self.on_tab_changed)

    def toggle_left_panel(self):
        is_hidden = self.btn_toggle_left.isChecked()
        self.palette_group.setVisible(not is_hidden)
        self.btn_toggle_left.setText("显示组件库" if is_hidden else "隐藏组件库")

    def toggle_right_panel(self):
        is_hidden = self.btn_toggle_right.isChecked()
        self.right_widget.setVisible(not is_hidden)
        self.btn_toggle_right.setText("显示检查器" if is_hidden else "隐藏检查器")

    def _create_tree_widget(self):
        tree = LogicTreeWidget()
        tree.customContextMenuRequested.connect(self.show_context_menu)
        tree.hierarchy_changed.connect(lambda: self._on_tree_changed(tree))
        tree.itemSelectionChanged.connect(self.on_outline_selected)
        return tree

    def get_current_tree(self):
        return self.workspace_tabs.currentWidget()

    def get_current_history(self):
        tree = self.get_current_tree()
        state = self.tab_states.get(tree)
        return state['history'] if state else None

    def on_tab_changed(self, index):
        self._update_toolbar_buttons()
        self.on_outline_selected() 
        self._update_desc_preview() 

    def close_sandbox_tab(self, index):
        if index == 0:
            return 
        tree = self.workspace_tabs.widget(index)
        self.workspace_tabs.removeTab(index)
        if tree in self.tab_states:
            del self.tab_states[tree]
        tree.deleteLater()

    def _on_tree_changed(self, tree):
        state = self.tab_states.get(tree)
        if not state:
            return
        
        state['history'].save_snapshot()
        
        if tree == self.get_current_tree():
            self._update_desc_preview()
            
        if state['type'] == 'card':
            self.data_changed.emit()
        elif state['type'] == 'preset':
            self._auto_save_preset(tree, state['preset_name'])

    def _update_toolbar_buttons(self):
        h = self.get_current_history()
        if h:
            self.btn_undo.setEnabled(len(h.history_stack) > 1)
            self.btn_redo.setEnabled(len(h.redo_stack) > 0)
        else:
            self.btn_undo.setEnabled(False)
            self.btn_redo.setEnabled(False)

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+C"), self, lambda: self.get_current_history().copy_nodes() if self.get_current_history() else None)
        QShortcut(QKeySequence("Ctrl+V"), self, lambda: self.get_current_history().paste_nodes() if self.get_current_history() else None)
        QShortcut(QKeySequence("Delete"), self, self.delete_selected)
        QShortcut(QKeySequence("Ctrl+Z"), self, self.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self, self.redo)

    def undo(self):
        h = self.get_current_history()
        if h:
            h.undo()

    def redo(self):
        h = self.get_current_history()
        if h:
            h.redo()

    def _on_param_updated(self, item, key, value):
        if not isinstance(item, LogicNodeItem):
            print(f"警告：节点 {item.data(0, Qt.UserRole)} 不是 LogicNodeItem 类型")
            return
        
        item.update_param(key, value)

        node_id = item.data(0, Qt.UserRole)
        if node_id in ["PrimaryTargetFilter", "SecondaryTargetFilter"] and key == "AdditionalTargetType":
            add_node = None
            for i in range(item.childCount()):
                if item.child(i).data(0, Qt.UserRole) == "AdditionalTargetQuery":
                    add_node = item.child(i)
                    break

            if value == "Query" and not add_node:
                LogicNodeItem(item, "AdditionalTargetQuery", {}, False)
                item.setExpanded(True)
            elif value != "Query" and add_node:
                item.removeChild(add_node)

        self._on_tree_changed(item.treeWidget())

    def show_palette_menu(self, pos):
        item = self.palette_tree.itemAt(pos)
        if not item or item.data(0, Qt.UserRole) != "Preset":
            return
        menu = QMenu(self)
        menu.addAction("✏️ 在沙箱中打开/编辑此预设", lambda: self.open_preset_sandbox(item.data(1, Qt.UserRole)))
        menu.addAction("🗑️ 删除此预设", lambda: self.delete_preset(item.data(1, Qt.UserRole)))
        menu.exec_(self.palette_tree.mapToGlobal(pos))

    def open_preset_sandbox(self, preset_name):
        for i in range(self.workspace_tabs.count()):
            tree = self.workspace_tabs.widget(i)
            state = self.tab_states.get(tree)
            if state and state.get('type') == 'preset' and state.get('preset_name') == preset_name:
                self.workspace_tabs.setCurrentIndex(i)
                return

        new_tree = self._create_tree_widget()
        idx = self.workspace_tabs.addTab(new_tree, f"📦 预设: {preset_name}")
        self.workspace_tabs.setCurrentIndex(idx)
        
        self.tab_states[new_tree] = {
            'type': 'preset',
            'preset_name': preset_name,
            'history': LogicHistoryManager(self, new_tree)
        }
        
        p_data = logic_presets.USER_PRESETS.get(preset_name)
        if p_data:
            self._restore_node_dict(new_tree.invisibleRootItem(), p_data)
            new_tree.expandAll()
            
        self.tab_states[new_tree]['history'].save_snapshot()

    def _auto_save_preset(self, tree, preset_name):
        root = tree.invisibleRootItem()
        if root.childCount() > 0:
            p_data = self._parse_node_to_dict(root.child(0))
            logic_presets.USER_PRESETS[preset_name] = p_data
            logic_presets._write_to_local()

    def delete_preset(self, preset_name):
        reply = QMessageBox.question(self, "确认删除", f"确定要删除预设 '{preset_name}' 吗？")
        if reply == QMessageBox.Yes:
            if preset_name in logic_presets.USER_PRESETS:
                del logic_presets.USER_PRESETS[preset_name]
                logic_presets._write_to_local()
                self._populate_palette()
                
                for i in range(self.workspace_tabs.count() - 1, 0, -1):
                    tree = self.workspace_tabs.widget(i)
                    state = self.tab_states.get(tree)
                    if state and state.get('type') == 'preset' and state.get('preset_name') == preset_name:
                        self.close_sandbox_tab(i)

    def add_from_palette(self, item, column):
        role = item.data(0, Qt.UserRole)
        if role == "Category":
            return
        
        tree = self.get_current_tree()
        selected = tree.selectedItems()
        
        if role == "Preset":
            p_data = logic_presets.USER_PRESETS.get(item.data(1, Qt.UserRole))
            if not p_data:
                return
            
            if p_data["node_id"] == "AbilityGroup":
                self._restore_node_dict(tree.invisibleRootItem(), p_data)
                tree.expandAll()
                self._on_tree_changed(tree)
                return

            if not selected:
                QMessageBox.warning(self, "提示", "请在工作区中选中要插入的父节点。")
                return
                
            curr = selected[0]
            while curr:
                if self._can_insert(curr, p_data["node_id"]):
                    self._restore_node_dict(curr, p_data)
                    curr.setExpanded(True)
                    self._on_tree_changed(tree)
                    return
                curr = curr.parent()
            QMessageBox.warning(self, "提示", "当前选中的位置无法插入该预设，请检查嵌套规则。")
            
        else:
            if not selected:
                QMessageBox.warning(self, "提示", "请在工作区中选中要插入的父节点。")
                return
            curr = selected[0]
            while curr:
                if self._can_insert(curr, role):
                    self.add_component(curr, role)
                    return
                curr = curr.parent()
            QMessageBox.warning(self, "提示", "当前选中的位置无法插入该组件，请检查嵌套规则。")

    def show_context_menu(self, pos):
        tree = self.get_current_tree()
        selected = tree.selectedItems()
        if not selected:
            return
        item = selected[0]
        node_id = item.data(0, Qt.UserRole)
        is_disabled = item.data(2, Qt.UserRole)
        
        menu = QMenu(self)
        if node_id == "AbilityGroup":
            menu.addAction("⭐ 保存整个技能组为预设", lambda: self.save_to_preset(item))
        elif node_id in logic_library.NODE_DEF:
            menu.addAction("恢复启用" if is_disabled else "🚫 禁用此节点 (不导出)", lambda: self.toggle_disable_nodes())
            menu.addAction("⭐ 保存为本地预设", lambda: self.save_to_preset(item))
            menu.addSeparator()
            
            replace_menu = menu.addMenu("🔄 更换为同类节点...")
            cat = logic_library.NODE_DEF[node_id].get("category")
            for nid, defn in logic_library.NODE_DEF.items():
                if nid != node_id and defn.get("category") == cat:
                    replace_menu.addAction(localization.NODE_NAMES.get(nid, nid), lambda target_nid=nid: self.replace_node(item, target_nid))
            if replace_menu.isEmpty():
                replace_menu.setEnabled(False)
            
        if not menu.isEmpty():
            menu.exec_(tree.mapToGlobal(pos))

    def _can_insert(self, parent_item, child_node_id):
        target_id = parent_item.data(0, Qt.UserRole)
        cat = logic_library.NODE_DEF.get(child_node_id, {}).get("category")
        
        if child_node_id in ["OncePerGameCondition", "OncePerTurnCondition", "PersistsAfterTransform"]:
            return target_id == "AbilityGroup"
        
        if target_id in ["FinderPlaceholder", "QueryPlaceholder"]:
            return cat in ["CompositeQuery", "Query"]
        
        if target_id == "AbilityGroup":
            return cat in ["Trigger", "Filter", "TargetSelector", "Effect", "Framework", "ComplexEffect"]
            
        allowed = logic_library.NODE_DEF.get(target_id, {}).get("allowed_children", [])
        return cat in allowed or child_node_id in allowed

    def replace_node(self, item, new_node_id):
        old_params = item.data(1, Qt.UserRole)
        new_defn = logic_library.NODE_DEF[new_node_id]
        new_params = copy.deepcopy(new_defn.get("default_data", {}))
        for k, v in old_params.items():
            if k in new_defn.get("editable_params", {}):
                new_params[k] = v
        
        item.setData(0, Qt.UserRole, new_node_id)
        item.setData(1, Qt.UserRole, new_params)
        item.refresh_text()
        
        self.inspector.load_node(item)
        self._on_tree_changed(item.treeWidget())

    def toggle_disable_nodes(self):
        tree = self.get_current_tree()
        for item in tree.selectedItems():
            new_state = not (item.data(2, Qt.UserRole) or False)
            item.setData(2, Qt.UserRole, new_state)
            item.refresh_text()
            
            def refresh_children(parent_item):
                for i in range(parent_item.childCount()):
                    child = parent_item.child(i)
                    child.setData(2, Qt.UserRole, new_state)
                    child.refresh_text()
                    refresh_children(child)
            refresh_children(item)
            
        self._on_tree_changed(tree)

    def save_to_preset(self, item):
        name, ok = QInputDialog.getText(self, "保存预设", "起个名字：")
        if ok and name.strip():
            d = self._parse_node_to_dict(item)
            logic_presets.save_preset(name.strip(), d)
            self._populate_palette()

    def add_ability_group(self):
        tree = self.get_current_tree()
        group_item = LogicNodeItem(tree, "AbilityGroup", {}, False)
        self.add_component(group_item, "EffectEntityGrouping")
        tree.expandAll()
        tree.setCurrentItem(group_item)
        self._on_tree_changed(tree)

    def add_component(self, parent_item, node_id):
        defn = logic_library.NODE_DEF[node_id]
        params = copy.deepcopy(defn.get("default_data", {}))
        
        child = LogicNodeItem(parent_item, node_id, params, False)
        
        if node_id == "QueryEntityCondition":
            LogicNodeItem(child, "FinderPlaceholder", {}, False)
            LogicNodeItem(child, "QueryPlaceholder", {}, False)
        
        if node_id == "MoveCardToLanesEffectDescriptor":
            ability_group = parent_item
            while ability_group and ability_group.data(0, Qt.UserRole) != "AbilityGroup":
                ability_group = ability_group.parent()
            
            if ability_group:
                secondary_params = copy.deepcopy(logic_library.NODE_DEF["SecondaryTargetFilter"].get("default_data", {}))
                secondary_item = LogicNodeItem(ability_group, "SecondaryTargetFilter", secondary_params, False)
                
                lane_query_defn = logic_library.NODE_DEF.get("HasLaneComponent")
                if lane_query_defn:
                    LogicNodeItem(secondary_item, "HasLaneComponent", {}, False)
                    secondary_item.setExpanded(True)
        
        parent_item.setExpanded(True)
        tree = parent_item.treeWidget()
        if tree:
            tree.setCurrentItem(child)
            self._on_tree_changed(tree)

    def delete_selected(self):
        tree = self.get_current_tree()
        root = tree.invisibleRootItem()
        for item in tree.selectedItems():
            if item.data(0, Qt.UserRole) != "EffectEntityGrouping":
                (item.parent() or root).removeChild(item)
        self._on_tree_changed(tree)

    def on_outline_selected(self):
        if not hasattr(self, 'inspector'):
            return
            
        self.inspector.clear()
        tree = self.get_current_tree()
        if not tree:
            return
        
        selected = tree.selectedItems()
        if not selected:
            self.inspector.title.setText("请在工作区中选择一个节点")
            return
            
        item = selected[0]
        self.inspector.load_node(item)

    def set_model(self, new_model):
        self.model = new_model
        while self.workspace_tabs.count() > 1:
            self.close_sandbox_tab(1)
        self.workspace_tabs.setCurrentIndex(0)
        self.update_ui(self.model)

    def _parse_tree_to_entities(self, tree):
        logic_entities = []
        root = tree.invisibleRootItem()
        
        def parse_node(item):
            if item.data(2, Qt.UserRole):
                return None
            node_id = item.data(0, Qt.UserRole)
            
            if node_id == "AdditionalTargetQuery":
                return parse_node(item.child(0)) if item.childCount() > 0 else None
                
            defn = logic_library.NODE_DEF.get(node_id)
            if not defn:
                return None
            
            data = LogicNodeAdapter.to_entity_data(node_id, item, parse_node, defn)
            return {"$type": f"{defn['type']}, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null", "$data": data}
            
        for i in range(root.childCount()):
            top_item = root.child(i)
            if top_item.data(2, Qt.UserRole):
                continue
            
            if top_item.data(0, Qt.UserRole) == "AbilityGroup":
                components = [res for j in range(top_item.childCount()) if (res := parse_node(top_item.child(j)))]
                logic_entities.append({"components": components})
            else:
                res = parse_node(top_item)
                if res:
                    logic_entities.append({"components": [res]})
                    
        return logic_entities

    def sync_to_model(self, model):
        model.logic_entities = self._parse_tree_to_entities(self.card_tree)

    def _update_desc_preview(self):
        tree = self.get_current_tree()
        if not tree:
            return
        entities = self._parse_tree_to_entities(tree)
        try:
            self.desc_preview.setText(translate_entities_to_text(entities))
        except Exception as e:
            self.desc_preview.setText(f"翻译生成失败: {e}")

    def update_ui(self, model):
        try:
            with signal_blocker(self, self.card_tree):
                self.card_tree.clear()
                if self.get_current_tree() == self.card_tree:
                    self.inspector.clear()
                    self.inspector.title.setText("请在工作区中选择一个节点")
                    
                for entity in model.logic_entities:
                    group_item = LogicNodeItem(self.card_tree, "AbilityGroup", {}, False)
                    for comp_dict in entity.get("components", []):
                        self._build_tree_node(group_item, comp_dict)
                self.card_tree.expandAll()
                
            self.tab_states[self.card_tree]['history'].clear()
            self.tab_states[self.card_tree]['history'].save_snapshot()
            
            if self.get_current_tree() == self.card_tree:
                self._update_desc_preview()
                
        except Exception as e:
            print(f"PanelLogic 解析异常: {e}")

    def _build_tree_node(self, parent_item, comp_dict):
        full_type = comp_dict.get("$type", "")
        cdata = comp_dict.get("$data", {})
        
        node_id = None
        for nid, defn in logic_library.NODE_DEF.items():
            if defn["type"] in full_type:
                if "HasComponentQuery" in full_type:
                    if defn.get("default_data", {}).get("ComponentType", "") == cdata.get("ComponentType", ""):
                        node_id = nid
                        break
                else:
                    node_id = nid
                    break
        
        if not node_id:
            return
        defn = logic_library.NODE_DEF[node_id]
        
        params, children = LogicNodeAdapter.extract_build_data(node_id, cdata, defn)
        
        child = LogicNodeItem(parent_item, node_id, params, False)
        LogicNodeAdapter.build_special_children(child, children, self._build_tree_node)

    def _parse_node_to_dict(self, item):
        node_id = item.data(0, Qt.UserRole)
        return LogicNodeAdapter.to_snapshot_dict(node_id, item, self._parse_node_to_dict)

    def _restore_node_dict(self, parent_item, data_dict):
        node_id = data_dict["node_id"]
        params = data_dict.get("params", {})
        is_disabled = data_dict.get("disabled", False)
        
        child = LogicNodeItem(parent_item, node_id, params, is_disabled)
        LogicNodeAdapter.restore_snapshot_children(node_id, child, data_dict, self._restore_node_dict)