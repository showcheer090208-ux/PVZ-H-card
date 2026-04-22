# card_model.py
import uuid
import config
from typing import Dict, Any, List
from constants import build_type_str, parse_type_str, ABILITY_COMP_MAP, COMP_ABILITY_MAP
from core_utils import safe_get

class CardModel:
    def __init__(self):
        """完全干净的初始化状态"""
        self.guid = 929802724
        self.prefab_name = str(uuid.uuid4())
        self.base_id = "Base"
        self.faction = "Plants"
        self.color = "Guardian"
        self.rarity_key = 4  
        self.set_name = "Gold"
        self.set_and_rarity_key = "ShowCheer"
        self.crafting_buy = 929802724
        self.crafting_sell = 929802724
        
        self.cost = 1
        self.has_attack = True
        self.has_health = True
        self.attack = 1
        self.health = 1
        
        # UI 杂项标记
        self.ignore_deck_limit = False
        self.is_power = False
        self.is_primary_power = False

        # 【新增】引擎底层类型组件标记
        self.is_trick = False         # Burst (锦囊)
        self.is_surprise = False      # Surprise (僵尸回合隐藏打出)
        self.is_environment = False   # Environment (环境)
        self.is_board_ability = False # BoardAbility (场景能力)

        self.logic_subtypes = []     
        self.display_subtypes = []   
        self.logic_tags = []    
        self.display_tags = []  
        
        self.components_abilities = {}  # 存放独立能力: Strikethrough, Armor 等
        self.triggered_abilities = []   # 【新增】存放组合类能力数组: [{"g":562, "vt":0, "va":0}, ...]
        self.root_special_abilities = []
        self.logic_entities = []

        self.subtype_affinities = []
        self.subtype_affinity_weights = []
        self.tag_affinities = []
        self.tag_affinity_weights = []
        self.card_affinities = []
        self.card_affinity_weights = []

    def _create_counter_component(self, type_name: str, value: int = 0) -> Dict[str, Any]:
        """构建底层计数器结构"""
        return {
            "$type": build_type_str(type_name),
            "$data": {
                "Counters": {
                    "IsPersistent": True,
                    "Counters": [{"SourceId": -1, "Duration": 0, "Value": value}]
                }
            }
        }

    def _generate_board_ability_dict(self) -> Dict[str, Any]:
        """【新增】专门为场景能力输出固定模板，仅保留技能树"""
        components = [
            {"$type": build_type_str("Card"), "$data": {"Guid": self.guid}},
            {"$type": build_type_str("BoardAbility"), "$data": {}},
            {"$type": build_type_str("SunCost"), "$data": {"SunCostValue": {"BaseValue": 0}}},
            {"$type": build_type_str("Rarity"), "$data": {"Value": "R1"}}
        ]
        
        if self.logic_entities:
            components.append({
                "$type": build_type_str("EffectEntitiesDescriptor"),
                "$data": {"entities": self.logic_entities}
            })

        entity_data = {
            "entity": {"components": components},
            "prefabName": "BoardAbilityView",
            "baseId": "BasePlantOneTimeEffect", # 底层引擎写死的壳
            "color": "0",
            "set": "Board",
            "rarity": 0,
            "setAndRarityKey": None,
            "displayHealth": 0,
            "displayAttack": 0,
            "displaySunCost": 0,
            "faction": "All",
            "ignoreDeckLimit": False,
            "isPower": False,
            "isPrimaryPower": False,
            "isFighter": False,
            "isEnv": False,
            "isAquatic": False,
            "isTeamup": False,
            "subtypes": [],
            "tags": [],
            "subtype_affinities": [],
            "subtype_affinity_weights": [],
            "tag_affinities": [],
            "tag_affinity_weights": [],
            "card_affinities": [],
            "card_affinity_weights": [],
            "usable": True,
            "special_abilities": []
        }
        return {str(self.guid): entity_data}

    def generate_json_dict(self) -> Dict[str, Any]:
        """序列化：Model -> JSON Dict"""
        # 【拦截器】如果类型是场景能力，直接短路输出上方写死的纯净模板
        if self.base_id == "BoardAbility":
            return self._generate_board_ability_dict()

        rarity_info = config.RARITIES.get(self.rarity_key, {"value": "R0"})
        components = [
            {"$type": build_type_str("Card"), "$data": {"Guid": self.guid}},
            {"$type": build_type_str("SunCost"), "$data": {"SunCostValue": {"BaseValue": self.cost}}},
            {"$type": build_type_str(self.faction), "$data": {}},
            {"$type": build_type_str("Rarity"), "$data": {"Value": rarity_info["value"]}}
        ]

        if self.has_attack:
            components.insert(1, {"$type": build_type_str("Attack"), "$data": {"AttackValue": {"BaseValue": self.attack}}})
        if self.has_health:
            components.insert(2, {"$type": build_type_str("Health"), "$data": {"MaxHealth": {"BaseValue": self.health}, "CurrentDamage": 0}})

        if self.logic_subtypes:
            components.append({"$type": build_type_str("Subtypes"), "$data": {"subtypes": self.logic_subtypes}})
        if self.logic_tags:
            components.append({"$type": build_type_str("Tags"), "$data": {"tags": self.logic_tags}})

        # 底层引擎组件
        if self.is_trick:
            components.append({"$type": build_type_str("Burst"), "$data": {}})
        if self.is_surprise:
            components.append({"$type": build_type_str("Surprise"), "$data": {}})
        if self.is_board_ability:
            components.append({"$type": build_type_str("BoardAbility"), "$data": {}})
        if self.is_environment:
            components.append({"$type": build_type_str("Environment"), "$data": {}})
        if self.is_power:
            components.append({"$type": build_type_str("Superpower"), "$data": {}})
        if self.is_primary_power:
            components.append({"$type": build_type_str("PrimarySuperpower"), "$data": {}})

        # ================= 核心修改点：处理 GrantedTriggeredAbilities =================
        # 将所有触发类能力合并到一个组件中
        if self.triggered_abilities:
            components.append({
                "$type": build_type_str("GrantedTriggeredAbilities"),
                "$data": {"a": self.triggered_abilities}
            })

        # 动态组装独立特殊能力 (非触发类)
        for ability_key, param_val in self.components_abilities.items():
            if ability_key in ["Multishot", "AttacksInAllLanes", "PlaysFaceDown"]:
                components.append({"$type": build_type_str(ability_key), "$data": {}})
            elif ability_key == "SplashDamage":
                components.append({"$type": build_type_str("SplashDamage"), "$data": {"DamageAmount": param_val}})
            elif ability_key in ["Aquatic", "Truestrike", "Strikethrough", "Deadly", "Frenzy"]:
                components.append(self._create_counter_component(ability_key, 0))
            elif ability_key == "AttackOverride":
                components.append(self._create_counter_component(ability_key, 2))
            elif ability_key == "Untrickable":
                components.append(self._create_counter_component(ability_key, param_val)) 
            elif ability_key == "Armor":
                components.append({"$type": build_type_str("Armor"), "$data": {"ArmorAmount": {"BaseValue": param_val}}})
            elif ability_key == "Teamup":
                components.append(self._create_counter_component("Teamup", 0))
                if param_val is True: 
                    components.append({"$type": build_type_str("CreateInFront"), "$data": {}})

        # 添加 EffectEntitiesDescriptor（必须在所有组件之后）
        if self.logic_entities:
            components.append({
                "$type": build_type_str("EffectEntitiesDescriptor"),
                "$data": {"entities": self.logic_entities}
            })

        # 构建最终外层结构
        entity_data = {
            "entity": {"components": components},
            "prefabName": self.prefab_name,
            "baseId": self.base_id,
            "color": self.color,
            "set": self.set_name,
            "rarity": self.rarity_key,
            "setAndRarityKey": self.set_and_rarity_key,
            "craftingBuy": self.crafting_buy,
            "craftingSell": self.crafting_sell,
            "displaySunCost": self.cost,
            "faction": self.faction,
            "ignoreDeckLimit": self.ignore_deck_limit,
            "isPower": self.is_power,
            "isPrimaryPower": self.is_primary_power,
            "isFighter": "OneTimeEffect" not in self.base_id and "Environment" not in self.base_id,
            "isEnv": "Environment" in self.base_id,
            "isAquatic": "Aquatic" in self.components_abilities,
            "isTeamup": "Teamup" in self.components_abilities,
            "subtypes": self.display_subtypes,
            "tags": self.display_tags,
            "subtype_affinities": self.subtype_affinities,
            "subtype_affinity_weights": self.subtype_affinity_weights,
            "tag_affinities": self.tag_affinities,
            "tag_affinity_weights": self.tag_affinity_weights,
            "card_affinities": self.card_affinities,
            "card_affinity_weights": self.card_affinity_weights,
            "usable": True,
            "special_abilities": self.root_special_abilities
        }

        if self.has_health: entity_data["displayHealth"] = self.health
        if self.has_attack: entity_data["displayAttack"] = self.attack

        return {str(self.guid): entity_data}

    @classmethod
    def from_json(cls, data: dict) -> 'CardModel':
        """反向解析引擎"""
        instance = cls()
        instance.prefab_name = data.get("prefabName", str(uuid.uuid4()))
        instance.base_id = data.get("baseId", "Base")
        instance.color = data.get("color", "Guardian")
        instance.set_name = data.get("set", "Gold")
        instance.rarity_key = data.get("rarity", 4)
        instance.set_and_rarity_key = data.get("setAndRarityKey", "Bloom_Common")
        instance.crafting_buy = data.get("craftingBuy", 50)
        instance.crafting_sell = data.get("craftingSell", 15)
        instance.cost = data.get("displaySunCost", 1)

        instance.faction = data.get("faction", "Plants")
        instance.ignore_deck_limit = data.get("ignoreDeckLimit", False)
        
        instance.is_power = data.get("isPower", False)
        instance.is_primary_power = data.get("isPrimaryPower", False)

        instance.display_subtypes = data.get("subtypes", [])
        instance.display_tags = data.get("tags", [])
        instance.root_special_abilities = data.get("special_abilities", [])

        # Affinities
        instance.subtype_affinities = data.get("subtype_affinities", [])
        instance.subtype_affinity_weights = data.get("subtype_affinity_weights", [])
        instance.tag_affinities = data.get("tag_affinities", [])
        instance.tag_affinity_weights = data.get("tag_affinity_weights", [])
        instance.card_affinities = data.get("card_affinities", [])
        instance.card_affinity_weights = data.get("card_affinity_weights", [])

        instance.has_attack, instance.has_health = False, False
        components = safe_get(data, "entity", "components", default=[])
        
        for comp in components:
            ctype = comp.get("$type", "")
            cdata = comp.get("$data", {})
            comp_name = parse_type_str(ctype)

            if comp_name == "Attack":
                instance.has_attack = True
                instance.attack = safe_get(cdata, "AttackValue", "BaseValue", default=1)
            elif comp_name == "Health":
                instance.has_health = True
                instance.health = safe_get(cdata, "MaxHealth", "BaseValue", default=1)
            elif comp_name == "Subtypes":
                instance.logic_subtypes = cdata.get("subtypes", [])
            elif comp_name == "Tags":
                instance.logic_tags = cdata.get("tags", [])
            elif comp_name == "EffectEntitiesDescriptor":
                instance.logic_entities = cdata.get("entities", [])
                
            elif comp_name == "Burst": instance.is_trick = True
            elif comp_name == "Surprise": instance.is_surprise = True
            elif comp_name == "Environment": instance.is_environment = True
            elif comp_name == "BoardAbility": instance.is_board_ability = True
            elif comp_name == "Superpower": instance.is_power = True
            elif comp_name == "PrimarySuperpower": instance.is_primary_power = True
            
            elif comp_name == "SplashDamage":
                instance.components_abilities["SplashDamage"] = cdata.get("DamageAmount", 1)
            elif comp_name == "Armor":
                instance.components_abilities["Armor"] = safe_get(cdata, "ArmorAmount", "BaseValue", default=1)
            elif comp_name == "Untrickable":
                instance.components_abilities["Untrickable"] = safe_get(cdata, "Counters", "Counters", 0, "Value", default=1)
            elif comp_name == "Teamup":
                instance.components_abilities["Teamup"] = False 
            elif comp_name == "CreateInFront":
                instance.components_abilities["Teamup"] = True
            elif comp_name in COMP_ABILITY_MAP:
                ability_key = COMP_ABILITY_MAP[comp_name]
                if ability_key not in ["SplashDamage", "Armor", "Untrickable", "Teamup"]:
                    instance.components_abilities[ability_key] = True
            elif comp_name == "GrantedTriggeredAbilities":
                # 【核心修改点】直接将整个数组读入模型
                instance.triggered_abilities = cdata.get("a", [])

        # 【智能反推】如果是导入的是原版的场景能力数据，将UI挂载点修改回我们的虚拟基类
        if instance.is_board_ability and instance.base_id == "BasePlantOneTimeEffect" and data.get("set") == "Board":
            instance.base_id = "BoardAbility"

        return instance