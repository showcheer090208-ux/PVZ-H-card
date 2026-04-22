# ui/tab_export.py
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                               QLineEdit, QPushButton, QMessageBox, QLabel)
from PySide6.QtCore import QSettings
from bundle_packer import update_bundle_with_card_data

class TabExport(QWidget):
    def __init__(self, project_manager):
        super().__init__()
        self.pm = project_manager # 直接传入工程管理器
        self.settings = QSettings("ModdingTool", "PvZHeroesEditor_IO")
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 封包车间
        export_group = QGroupBox("📦 幻影引擎打包车间")
        export_layout = QVBoxLayout(export_group)
        export_layout.setContentsMargins(30, 40, 30, 40)
        export_layout.setSpacing(25)

        info = QLabel("🚀 将当前工程中的所有修改，一次性编译并注入游戏底包中。")
        info.setStyleSheet("color: #aaa; font-size: 14px;")
        export_layout.addWidget(info)

        # In & Out
        b_src_layout = QHBoxLayout()
        b_src_layout.addWidget(QLabel("游戏原版 AB 包 (In): "))
        self.bundle_src_input = QLineEdit()
        self.bundle_src_input.setMinimumHeight(35)
        b_src_layout.addWidget(self.bundle_src_input)
        export_layout.addLayout(b_src_layout)

        b_out_layout = QHBoxLayout()
        b_out_layout.addWidget(QLabel("生成的 Mod AB 包 (Out):"))
        self.bundle_out_input = QLineEdit()
        self.bundle_out_input.setMinimumHeight(35)
        b_out_layout.addWidget(self.bundle_out_input)
        export_layout.addLayout(b_out_layout)

        # 终极按钮
        btn_pack_bundle = QPushButton("💎 编译当前工程并生成 Mod (.assets)")
        btn_pack_bundle.setMinimumHeight(45)
        btn_pack_bundle.setStyleSheet("font-size: 16px; font-weight: bold;")
        btn_pack_bundle.clicked.connect(self.pack_to_bundle)
        export_layout.addWidget(btn_pack_bundle)

        main_layout.addWidget(export_group)
        main_layout.addStretch()

    def _load_settings(self):
        base_dir = os.getcwd()
        self.bundle_src_input.setText(self.settings.value("bundle_src_path", os.path.join(base_dir, "data", "card_data_1")))
        self.bundle_out_input.setText(self.settings.value("bundle_out_path", os.path.join(base_dir, "out", "card_data_1")))

    def _save_settings(self):
        self.settings.setValue("bundle_src_path", self.bundle_src_input.text().strip())
        self.settings.setValue("bundle_out_path", self.bundle_out_input.text().strip())

    def pack_to_bundle(self):
        self._save_settings()
        
        if not self.pm.current_project_name:
            QMessageBox.warning(self, "警告", "当前没有加载任何工程！请先去【工程大厅】新建或读取工程。")
            return
            
        if not self.pm.project_cards:
            QMessageBox.warning(self, "警告", "当前工程是空的！没有任何卡牌可以打包。")
            return

        bundle_src = self.bundle_src_input.text().strip()
        bundle_out = self.bundle_out_input.text().strip()

        if not bundle_src or not bundle_out:
            QMessageBox.warning(self, "路径缺失", "请先填写原包和导出路径！")
            return

        try:
            # 奇迹发生的地方：直接把整个工程的几十张卡字典塞给 packer
            success, msg = update_bundle_with_card_data(
                bundle_in_path=bundle_src, 
                bundle_out_path=bundle_out, 
                modded_card_dict=self.pm.project_cards,
                target_asset_name="cards"
            )

            if success:
                QMessageBox.information(self, "🎉 编译成功", f"工程 [{self.pm.current_project_name}] 编译完毕！\n{msg}")
            else:
                QMessageBox.critical(self, "💥 编译失败", msg)
        except Exception as e:
            QMessageBox.critical(self, "💥 打包异常", f"发生错误：\n{str(e)}")