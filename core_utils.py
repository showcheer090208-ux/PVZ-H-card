# core_utils.py
from typing import Any
from contextlib import contextmanager

@contextmanager
def signal_blocker(*widgets):
    """
    上下文管理器：安全地阻塞和恢复 UI 组件的信号，防止互相触发陷入死循环。
    用法: 
        with signal_blocker(self.cb_attack, self.cb_health):
            self.cb_attack.setChecked(True)
    """
    for widget in widgets:
        if widget is not None:
            widget.blockSignals(True)
    try:
        yield
    finally:
        for widget in widgets:
            if widget is not None:
                widget.blockSignals(False)

def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """
    深层字典的安全提取器。
    用法: val = safe_get(data, 'Counters', 'Counters', 0, 'Value', default=1)
    """
    val = data
    try:
        for key in keys:
            val = val[key]
        return val if val is not None else default
    except (KeyError, IndexError, TypeError):
        return default