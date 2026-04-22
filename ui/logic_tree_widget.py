# ui/logic_tree_widget.py
from PySide6.QtWidgets import QTreeWidget, QAbstractItemView
from PySide6.QtCore import Qt
import logic_library 

class LogicTreeWidget(QTreeWidget):
    """带智能嵌套规则校验的拖拽树状图"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
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
        
        if not target_item or not dragged_item:
            event.ignore()
            return

        if target_item == dragged_item or self.is_child_of(target_item, dragged_item):
            event.ignore()
            return

        target_id = target_item.data(0, Qt.UserRole)
        dragged_id = dragged_item.data(0, Qt.UserRole)
        
        can_accept = False
        cat = logic_library.NODE_DEF.get(dragged_id, {}).get("category")

        if target_id == "AbilityGroup":
            if cat in ["Trigger", "Filter", "TargetSelector", "Effect", "Framework"]:
                can_accept = True
        else:
            allowed = logic_library.NODE_DEF.get(target_id, {}).get("allowed_children", [])
            if ("CompositeQuery" in allowed and cat == "CompositeQuery") or \
               ("Query" in allowed and cat == "Query"):
                can_accept = True

        if can_accept: event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        super().dropEvent(event)
        # 拖拽完成后通知主面板刷新数据
        self.window().data_changed.emit()