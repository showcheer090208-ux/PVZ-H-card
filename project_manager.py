# project_manager.py
import os
import json
from PySide6.QtCore import QSettings

class ProjectManager:
    """幻影引擎 - 全局工程管理器"""
    def __init__(self):
        # 建立专用的工程文件夹，和老旧的 raw data 彻底区分
        self.projects_dir = os.path.join(os.getcwd(), "projects")
        os.makedirs(self.projects_dir, exist_ok=True)
        
        self.current_project_name = None
        self.project_cards = {}  # 结构: { "GUID(str)": {card_data_dict} }
        self.settings = QSettings("ModdingTool", "PhantomEngine_Project")
        
        # 自动加载上次的工程
        self.auto_load_last_project()

    def auto_load_last_project(self):
        last_proj = self.settings.value("last_project", "")
        if last_proj and self.load_project(last_proj):
            return True
        return False

    def get_all_projects(self):
        """扫描 projects 目录下的所有 .phantom 工程"""
        projects = []
        for file in os.listdir(self.projects_dir):
            if file.endswith(".phantom"):
                projects.append(file[:-8]) # 截掉后缀
        return sorted(projects)

    def create_project(self, name):
        """新建一个空白工程"""
        self.current_project_name = name
        self.project_cards = {}
        self.save_current_project()
        return True

    def load_project(self, name):
        """读取工程文件到内存"""
        filepath = os.path.join(self.projects_dir, f"{name}.phantom")
        if not os.path.exists(filepath):
            return False
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.project_cards = json.load(f)
            self.current_project_name = name
            self.settings.setValue("last_project", name)
            return True
        except Exception as e:
            print(f"读取工程失败: {e}")
            return False

    def save_current_project(self):
        """将内存中的所有卡牌落盘保存到 .phantom 文件"""
        if not self.current_project_name:
            return False
            
        filepath = os.path.join(self.projects_dir, f"{self.current_project_name}.phantom")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.project_cards, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def add_or_update_card(self, card_model):
        """从工作台把卡牌保存进工程清单"""
        if not self.current_project_name:
            return False
        
        # 提取这张卡最新的 JSON 字典
        card_dict = card_model.generate_json_dict()
        guid_str = str(card_model.guid)
        
        # 更新到工程内存
        self.project_cards[guid_str] = card_dict[guid_str]
        
        # 自动落盘
        self.save_current_project()
        return True

    def delete_card(self, guid_str):
        """从工程中删除某张卡的修改"""
        if guid_str in self.project_cards:
            del self.project_cards[guid_str]
            self.save_current_project()