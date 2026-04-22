# ui/logic/param_dialog.py
import copy
from PySide6.QtWidgets import QDialog, QFormLayout, QSpinBox, QComboBox, QCheckBox, QDialogButtonBox
import logic_library 
import localization 

class ComponentParamDialog(QDialog):
    def __init__(self, node_id: str, current_params: dict, parent=None):
        super().__init__(parent)
        node_name = localization.NODE_NAMES.get(node_id, node_id)
        self.setWindowTitle(f"编辑参数 - {node_name}")
        self.setMinimumWidth(380)
        self.layout = QFormLayout(self)
        self.widgets = {}
        self.schema = logic_library.NODE_DEF.get(node_id, {}).get("editable_params", {})
        self.current_params = copy.deepcopy(current_params)

        for key, config in self.schema.items():
            display_name = localization.PARAM_NAMES.get(key, key)
            if config["type"] == "int":
                w = QSpinBox()
                w.setRange(config.get("min", -2147483648), config.get("max", 2147483647))
                w.setValue(self.current_params.get(key, 0))
                self.widgets[key] = w
                self.layout.addRow(f"{display_name}:", w)
            elif config["type"] == "enum":
                w = QComboBox()
                for opt in config["options"]: 
                    w.addItem(localization.ENUM_NAMES.get(opt, opt), opt)
                curr_val = self.current_params.get(key, config["options"][0])
                idx = w.findData(curr_val)
                if idx >= 0: 
                    w.setCurrentIndex(idx)
                self.widgets[key] = w
                self.layout.addRow(f"{display_name}:", w)
            elif config["type"] == "bool":
                w = QCheckBox("启用")
                w.setChecked(bool(self.current_params.get(key, False)))
                self.widgets[key] = w
                self.layout.addRow(f"{display_name}:", w)

        if node_id == "PrimaryTargetFilter" and "SelectionType" in self.widgets and "NumTargets" in self.widgets:
            sel_combo = self.widgets["SelectionType"]
            num_spin = self.widgets["NumTargets"]
            def on_sel_change(index):
                text = sel_combo.itemData(index) 
                if text in ["All", "Manual"]: 
                    num_spin.setValue(0)
            sel_combo.currentIndexChanged.connect(on_sel_change)

        self.bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.bbox.accepted.connect(self.accept)
        self.bbox.rejected.connect(self.reject)
        self.layout.addRow(self.bbox)

    def get_values(self):
        for key, w in self.widgets.items():
            if isinstance(w, QSpinBox): self.current_params[key] = w.value()
            elif isinstance(w, QComboBox): self.current_params[key] = w.currentData()
            elif isinstance(w, QCheckBox): self.current_params[key] = w.isChecked()
        return self.current_params