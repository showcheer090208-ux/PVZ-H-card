import os
import json
import copy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRESETS_FILE = os.path.join(BASE_DIR, "custom_presets.json")

USER_PRESETS = {}

def load_presets():
    global USER_PRESETS
    USER_PRESETS.clear()
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
                USER_PRESETS = json.load(f)
        except Exception as e:
            print(f"读取本地预设失败: {e}")

# 【修复】直接接收并保存完整的节点字典树
def save_preset(name, node_dict):
    USER_PRESETS[name] = copy.deepcopy(node_dict)
    _write_to_local()

def _write_to_local():
    try:
        with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(USER_PRESETS, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"写入预设失败: {e}")

load_presets()