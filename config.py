import os
import re
import json

# ---------------- 绝对路径处理 ----------------
# 获取 config.py 所在的真实绝对目录，防止相对路径导致的文件找不到
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOM_SUBTYPES_FILE = os.path.join(BASE_DIR, "custom_subtypes.json")
CUSTOM_TAGS_FILE = os.path.join(BASE_DIR, "custom_tags.json")
UUID_FILE = os.path.join(BASE_DIR, "uuid.txt")

# ---------------- 卡牌库读取 ----------------
KNOWN_CARDS = {}

def load_known_cards_from_file(filepath=UUID_FILE):
    global KNOWN_CARDS
    KNOWN_CARDS.clear()
    if not os.path.exists(filepath): return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '——' not in line: continue
                parts = [p.strip() for p in re.split(r'——+', line) if p.strip()]
                if len(parts) >= 3:
                    try:
                        KNOWN_CARDS[int(parts[0])] = {"uuid": parts[1], "name": parts[2]}
                    except ValueError: continue
    except Exception as e:
        print(f"读取卡牌库错误: {e}")

load_known_cards_from_file()

# ---------------- 静态常量 ----------------
RARITIES = {
    4: {"value": "R0", "name": "基础卡 (Common)"},
    0: {"value": "R1", "name": "罕见 (Uncommon)"},
    1: {"value": "R2", "name": "稀有 (Rare)"},
    2: {"value": "R3", "name": "超稀有 (SuperRare)"},
    3: {"value": "R4", "name": "传说 (Legendary)"},
    5: {"value": "Event", "name": "活动卡 (Event)"}
}
FACTIONS = {"Plants": "植物 (Plants)", "Zombies": "僵尸 (Zombies)"}
BASE_IDS = {
    "Base": "植物 (Base)", "BasePlantOneTimeEffect": "植物锦囊 (Plant Trick)",
    "BasePlantEnvironment": "植物环境 (Plant Env)", "BaseZombie": "僵尸 (BaseZombie)",
    "BaseZombieOneTimeEffect": "僵尸锦囊 (Zombie Trick)", "BaseZombieEnvironment": "僵尸环境 (Zombie Env)",
    "BoardAbility": "场景能力 (关卡机制)",
}
COLORS = {
    "Guardian": "守卫 (Guardian)", "Kabloom": "爆花 (Kabloom)", "Mega-Grow": "猛涨 (Mega-Grow)", 
    "Smarty": "聪明 (Smarty)", "Solar": "光鸣 (Solar)", "Hearty": "健壮 (Hearty)", 
    "Brainy": "有脑 (Brainy)", "Sneaky": "狡猾 (Sneaky)", "Crazy": "疯狂 (Crazy)", "Beastly": "猛兽 (Beastly)"
}

# 基础种族字典
SUBTYPES = {
    0: "豌豆 (Peashooter)", 1: "莓果 (Berry)", 2: "豆子 (Bean)", 3: "花朵 (Flower)", 
    4: "蘑菇 (Mushroom)", 5: "坚果 (Nut)", 6: "运动员 (Sports)", 7: "科学家 (Science)", 
    8: "跳舞 (Dancing)", 9: "小鬼 (Imp)", 10: "宠物 (Pet)", 11: "巨尸 (Gargantuar)", 
    12: "海盗 (Pirate)", 13: "松果 (Pinecone)", 15: "胡须 (Mustache)", 16: "派对 (Party)", 
    18: "美食家 (Gourmet)", 19: "历史 (History)", 20: "木桶 (Barrel)", 21: "种子 (Seed)", 
    22: "动物 (Animal)", 23: "仙人掌 (Cactus)", 24: "玉米 (Corn)", 25: "巨龙 (Dragon)", 
    26: "捕蝇草 (Flytrap)", 27: "水果 (Fruit)", 28: "绿叶 (Leafy)", 29: "苔藓 (Moss)", 
    31: "根茎 (Root)", 32: "窝瓜 (Squash)", 33: "树木 (Tree)", 35: "钟表 (Clock)", 
    37: "职业 (Professional)", 39: "怪物 (Monster)", 40: "香蕉 (Banana)", 41: "哑剧 (Mime)",
    42: "休切尔(柴Q)",
}

# 卡牌系列/卡包
SETS = {
    "Gold": "高级包 (Premium/Gold)",
    "Galactic": "银河包 (Galactic)",
    "Colossal": "巨大包 (Colossal)",
    "Triassic": "三叠纪 (Triassic)",
    "Event": "活动卡 (Event)",
    "Token": "衍生物/不可合成 (Token)"
}

# ---------------- 特殊能力 (Abilities) 配置 ----------------
# 格式: { "能力键值": {"name": "显示名称", "type": "类型", ...附加参数} }
SPECIAL_ABILITIES = {
    "Multishot": {
        "name": "🎯 攻击三线 (Multishot)",
        "type": "bool"
    },
    "AttacksInAllLanes": {
        "name": "🌊 攻击全线 (AttacksInAllLanes)",
        "type": "bool"
    },
    "SplashDamage": {
        "name": "💥 溅射伤害 (Splash Damage)",
        "type": "int",
        "default": 1,
        "label": "伤害值"
    },
    "Aquatic": {
        "name": "🐠 两栖 (Aquatic)",
        "type": "bool"
    },
    "Teamup": {
        "name": "🤝 组队 (Team-up)",
        "type": "teamup_combo",
        "options": {"默认 (可被覆盖)": False, "召唤在前排 (CreateInFront)": True}
    },
    "Truestrike": {
        "name": "⚡ 必中/防被格挡 (Truestrike)",
        "type": "bool"
    },
    "Strikethrough": {
        "name": "🗡️ 穿透 (Strikethrough)",
        "type": "bool"
    },
    "Armor": {
        "name": "🛡️ 装甲 (Armor)",
        "type": "int",
        "default": 1,
        "label": "护甲值"
    },
    "Untrickable": {
        "name": "🚫 锦囊免疫 (Untrickable)",
        "type": "combo",
        "options": {"免疫植物锦囊": 1, "免疫僵尸锦囊": 2}
    },
    "AttackOverride": {
        "name": "❤️ 血量攻击 (AttackOverride)",
        "type": "bool"
    },
    "Deadly": {
        "name": "☠️ 致命 (Deadly)",
        "type": "bool"
    },
    "PlaysFaceDown": {
        "name": "🪦 墓碑 (Gravestone)",
        "type": "bool"
    },
    "Frenzy": {
        "name": "🔥 狂热 (Frenzy)",
        "type": "bool"
    },
}
# ---------------- 根目录特殊能力预设 (Root Special Abilities Presets) ----------------
# 格式: { "能力标识符": "中文描述/批注" }
ROOT_ABILITY_PRESETS = {
    "Ambush": "克制英雄",
    "Armor": "装甲",
    "AttackOverride": "血量攻击",
    "Deadly": "致命",
    "Frenzy": "狂热",
    "Overshoot": "先攻",
    "Repeater": "双重攻击",
    "Strikethrough": "穿透",
    "Truestrike": "必中",
    "Unique": "特殊",
    "Untrickable": "锦囊免疫"
}

# ---------------- 种族与标签的存取逻辑 ----------------

def load_custom_subtypes():
    """加载用户自定义的种族"""
    if os.path.exists(CUSTOM_SUBTYPES_FILE):
        try:
            with open(CUSTOM_SUBTYPES_FILE, 'r', encoding='utf-8') as f:
                customs = json.load(f)
                for k, v in customs.items():
                    SUBTYPES[int(k)] = v
        except Exception as e:
            print(f"读取自定义种族错误: {e}")

def save_custom_subtype(subtype_id, subtype_name):
    """保存用户自定义种族并写入本地 JSON"""
    SUBTYPES[subtype_id] = subtype_name
    customs = {}
    if os.path.exists(CUSTOM_SUBTYPES_FILE):
        try:
            with open(CUSTOM_SUBTYPES_FILE, 'r', encoding='utf-8') as f:
                customs = json.load(f)
        except Exception:
            pass
    
    customs[str(subtype_id)] = subtype_name
    
    try:
        with open(CUSTOM_SUBTYPES_FILE, 'w', encoding='utf-8') as f:
            json.dump(customs, f, indent=4, ensure_ascii=False)
        return True, ""
    except PermissionError:
        return False, "文件被占用！请检查 custom_subtypes.json 是否被其他软件(如VSCode)打开。"
    except Exception as e:
        return False, str(e)


# 全局变量缓存本地读取的标签
SAVED_LOGIC_TAGS = []
SAVED_DISPLAY_TAGS = []

def load_custom_tags():
    """加载用户上次保存的标签"""
    global SAVED_LOGIC_TAGS, SAVED_DISPLAY_TAGS
    if os.path.exists(CUSTOM_TAGS_FILE):
        try:
            with open(CUSTOM_TAGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                SAVED_LOGIC_TAGS = data.get("logic_tags", [])
                SAVED_DISPLAY_TAGS = data.get("display_tags", [])
        except Exception as e:
            print(f"读取自定义标签错误: {e}")

def save_tags_to_local(logic_tags, display_tags):
    """将当前的标签列表保存到本地"""
    global SAVED_LOGIC_TAGS, SAVED_DISPLAY_TAGS
    SAVED_LOGIC_TAGS = logic_tags
    SAVED_DISPLAY_TAGS = display_tags
    try:
        data = {"logic_tags": logic_tags, "display_tags": display_tags}
        with open(CUSTOM_TAGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True, ""
    except PermissionError:
        return False, "文件被占用！请检查 custom_tags.json 是否被其他软件打开。"
    except Exception as e:
        return False, str(e)

# ---------------- 初始化执行区域 ----------------
# 只要项目启动导入此 config.py，自动读取所有本地库数据
load_custom_subtypes()
load_custom_tags()