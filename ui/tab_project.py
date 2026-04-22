# ui/tab_project.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QListWidget, QPushButton, QInputDialog, QMessageBox, 
                               QSplitter, QListWidgetItem, QLabel)
from PySide6.QtCore import Qt, Signal

class TabProject(QWidget):
    # 当用户双击某张卡，请求主窗口加载它到工作台
    edit_card_requested = Signal(dict)
    
    def __init__(self, project_manager):
        super().__init__()
        self.pm = project_manager
        self._setup_ui()
        self.refresh_project_list()
        self.refresh_card_roster()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # ====== 左侧：工程列表 ======
        proj_group = QGroupBox("📁 本地工程列表 (.phantom)")
        proj_layout = QVBoxLayout(proj_group)
        
        btn_new_proj = QPushButton("➕ 新建 Mod 工程")
        btn_new_proj.clicked.connect(self.create_new_project)
        proj_layout.addWidget(btn_new_proj)

        self.proj_list = QListWidget()
        self.proj_list.itemClicked.connect(self.on_project_selected)
        proj_layout.addWidget(self.proj_list)
        splitter.addWidget(proj_group)

        # ====== 右侧：当前工程的卡牌清单 ======
        roster_group = QGroupBox("📜 当前 Mod 包含的卡牌")
        roster_layout = QVBoxLayout(roster_group)
        
        self.status_label = QLabel("请先选择或新建一个工程")
        self.status_label.setStyleSheet("color: #aaa; font-weight: bold;")
        roster_layout.addWidget(self.status_label)

        self.card_list = QListWidget()
        self.card_list.setAlternatingRowColors(True)
        # 双击卡牌进入工作台
        self.card_list.itemDoubleClicked.connect(self.on_card_double_clicked)
        roster_layout.addWidget(self.card_list)
        
        btn_layout = QHBoxLayout()
        btn_new_card = QPushButton("✨ 在工作台新建一张卡牌")
        btn_new_card.clicked.connect(lambda: self.edit_card_requested.emit({})) # 传空字典代表新建
        
        btn_del_card = QPushButton("🗑️ 从当前 Mod 移除选中卡牌")
        btn_del_card.clicked.connect(self.delete_selected_card)
        
        btn_layout.addWidget(btn_new_card)
        btn_layout.addWidget(btn_del_card)
        roster_layout.addLayout(btn_layout)
        
        splitter.addWidget(roster_group)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        layout.addWidget(splitter)

    def refresh_project_list(self):
        self.proj_list.clear()
        for p in self.pm.get_all_projects():
            item = QListWidgetItem(f"📦 {p}")
            item.setData(Qt.UserRole, p)
            self.proj_list.addItem(item)
            
            # 自动高亮当前加载的工程
            if p == self.pm.current_project_name:
                item.setSelected(True)

    def refresh_card_roster(self):
        self.card_list.clear()
        if not self.pm.current_project_name:
            self.status_label.setText("请先选择或新建一个工程")
            self.card_list.setEnabled(False)
            return

        self.card_list.setEnabled(True)
        self.status_label.setText(f"当前激活工程: {self.pm.current_project_name} (双击卡牌去编辑)")
        
        import config # 用于读取中文译名
        for guid, cdata in self.pm.project_cards.items():
            name = config.KNOWN_CARDS.get(int(guid), {}).get("name", "自定义卡牌")
            item = QListWidgetItem(f"[{guid}] {name} - {cdata.get('prefabName', '')[:10]}...")
            item.setData(Qt.UserRole, guid)
            self.card_list.addItem(item)

    def create_new_project(self):
        name, ok = QInputDialog.getText(self, "新建工程", "请输入新 Mod 工程名称 (如: PVZ_Rebalance):")
        if ok and name.strip():
            self.pm.create_project(name.strip())
            self.refresh_project_list()
            self.refresh_card_roster()

    def on_project_selected(self, item):
        proj_name = item.data(Qt.UserRole)
        self.pm.load_project(proj_name)
        self.refresh_card_roster()

    def on_card_double_clicked(self, item):
        guid = item.data(Qt.UserRole)
        card_data = self.pm.project_cards.get(guid)
        if card_data:
            self.edit_card_requested.emit(card_data)

    def delete_selected_card(self):
        selected = self.card_list.selectedItems()
        if not selected: return
        guid = selected[0].data(Qt.UserRole)
        
        reply = QMessageBox.question(self, "确认移除", f"确定要从当前 Mod 中移除卡牌 {guid} 吗？")
        if reply == QMessageBox.Yes:
            self.pm.delete_card(guid)
            self.refresh_card_roster()