# ui/logic/tree_widget.py
from PySide6.QtWidgets import QTreeWidget, QAbstractItemView
from PySide6.QtCore import Qt, Signal
import logic_library 

class LogicTreeWidget(QTreeWidget):
    """带智能拖拽规则判定和独立信号的树状图"""
    # 【架构优化】新增自定义信号，避免越权调用 self.window() 导致的崩溃
    hierarchy_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setStyleSheet("QTreeWidget::item { height: 32px; }")

    def is_child_of(self, child, parent):
        while child:
            if child == parent: return True
            child = child.parent()
        return False

    def dragMoveEvent(self, event):
        target_item = self.itemAt(event.pos())
        dragged_item = self.currentItem()
        if not target_item or not dragged_item or target_item == dragged_item or self.is_child_of(target_item, dragged_item):
            event.ignore()
            return

        child_node_id = dragged_item.data(0, Qt.UserRole)
        cat = logic_library.NODE_DEF.get(child_node_id, {}).get("category")
        target_id = target_item.data(0, Qt.UserRole)
        
        can_accept = False
        # 同步更新白名单
        if target_id == "AbilityGroup":
            can_accept = cat in ["Trigger", "Filter", "TargetSelector", "Effect", "Framework", "ComplexEffect"]
        else:
            allowed = logic_library.NODE_DEF.get(target_id, {}).get("allowed_children", [])
            # 采用更通用的判定：分类在列表里，或者具体的节点ID在列表里
            can_accept = cat in allowed or child_node_id in allowed

        if can_accept: 
            event.accept()
        else: 
            event.ignore()

    def dropEvent(self, event):
        super().dropEvent(event)
        # 抛出自己的信号，由 PanelLogic 接收
        self.hierarchy_changed.emit()