# ui/logic/history.py
import json
from PySide6.QtWidgets import QApplication, QMessageBox

class LogicHistoryManager:
    def __init__(self, panel, tree):
        self.panel = panel 
        self.tree = tree # 【修改】绑定到具体的树，而不是全局
        self.history_stack = []
        self.redo_stack = []
        self.is_undoing = False

    def save_snapshot(self):
        if self.is_undoing: return
        root = self.tree.invisibleRootItem()
        entities = [self.panel._parse_node_to_dict(root.child(i)) for i in range(root.childCount())]
        
        if self.history_stack and self.history_stack[-1] == entities: return
        self.history_stack.append(entities)
        
        if len(self.history_stack) > 50: self.history_stack.pop(0)
        self.redo_stack.clear()
        self.panel._update_toolbar_buttons()

    def clear(self):
        self.history_stack.clear()
        self.redo_stack.clear()
        self.is_undoing = False
        self.panel._update_toolbar_buttons()

    def undo(self):
        if len(self.history_stack) > 1:
            self.is_undoing = True
            self.redo_stack.append(self.history_stack.pop())
            self.panel._restore_from_snapshot(self.tree, self.history_stack[-1])
            self.is_undoing = False
            self.panel._update_toolbar_buttons()
            self.panel._on_tree_changed(self.tree)

    def redo(self):
        if self.redo_stack:
            self.is_undoing = True
            state = self.redo_stack.pop()
            self.history_stack.append(state)
            self.panel._restore_from_snapshot(self.tree, state)
            self.is_undoing = False
            self.panel._update_toolbar_buttons()
            self.panel._on_tree_changed(self.tree)

    def copy_nodes(self):
        selected = self.tree.selectedItems()
        if not selected: return
        
        top_items = [item for item in selected if not any(self.tree.is_child_of(item, other) for other in selected if other != item)]
        pack = {"source": "PvZ_Logic_Editor", "nodes": [self.panel._parse_node_to_dict(i) for i in top_items]}
        QApplication.clipboard().setText(json.dumps(pack, ensure_ascii=False))

    def paste_nodes(self):
        text = QApplication.clipboard().text()
        if not text: return
        try:
            pack = json.loads(text)
            if pack.get("source") != "PvZ_Logic_Editor": return
        except Exception: 
            return

        selected = self.tree.selectedItems()
        target_item = selected[0] if selected else None
        pasted = 0
        
        for node_dict in pack.get("nodes", []):
            if node_dict["node_id"] == "AbilityGroup" or not target_item:
                root = self.tree.invisibleRootItem()
                self.panel._restore_node_dict(root, node_dict)
                pasted += 1
            else:
                if self.panel._can_insert(target_item, node_dict["node_id"]):
                    self.panel._restore_node_dict(target_item, node_dict)
                    pasted += 1
                
        if pasted > 0:
            if target_item:
                target_item.setExpanded(True)
            self.panel._on_tree_changed(self.tree)
        else:
            QMessageBox.warning(self.panel, "失败", "当前选中的节点位置不合法，无法粘贴。")