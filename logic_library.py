import copy

# 定义所有的技能组件节点 (纯底层结构，不含 UI 显示名)
NODE_DEF = {
    # ==================== Framework 基础框架 ====================
    "EffectEntityGrouping": {
        "type": "PvZCards.Engine.Components.EffectEntityGrouping",
        "default_data": {"AbilityGroupId": 0},
        "editable_params": {"AbilityGroupId": {"type": "int", "min": 0, "max": 2147483647}},
        "category": "Framework"
    },

    # ==================== Trigger 触发器 ====================
    "PlayTrigger": {
        "type": "PvZCards.Engine.Components.PlayTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "DiscardFromPlayTrigger": {
        "type": "PvZCards.Engine.Components.DiscardFromPlayTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "BuffTrigger": {
        "type": "PvZCards.Engine.Components.BuffTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "CombatEndTrigger": {
        "type": "PvZCards.Engine.Components.CombatEndTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "DamageTrigger": {
        "type": "PvZCards.Engine.Components.DamageTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "DestroyCardTrigger": {
        "type": "PvZCards.Engine.Components.DestroyCardTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "DrawCardTrigger": {
        "type": "PvZCards.Engine.Components.DrawCardTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "DrawCardFromSubsetTrigger": {
        "type": "PvZCards.Engine.Components.DrawCardFromSubsetTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "EnterBoardTrigger": {
        "type": "PvZCards.Engine.Components.EnterBoardTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "ExtraAttackTrigger": {
        "type": "PvZCards.Engine.Components.ExtraAttackTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "HealTrigger": {
        "type": "PvZCards.Engine.Components.HealTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "LaneCombatEndTrigger": {
        "type": "PvZCards.Engine.Components.LaneCombatEndTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "LaneCombatStartTrigger": {
        "type": "PvZCards.Engine.Components.LaneCombatStartTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "MoveTrigger": {
        "type": "PvZCards.Engine.Components.MoveTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "ReturnToHandTrigger": {
        "type": "PvZCards.Engine.Components.ReturnToHandTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "RevealPhaseEndTrigger": {
        "type": "PvZCards.Engine.Components.RevealPhaseEndTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "RevealTrigger": {
        "type": "PvZCards.Engine.Components.RevealTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "SlowedTrigger": {
        "type": "PvZCards.Engine.Components.SlowedTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "SurprisePhaseStartTrigger": {
        "type": "PvZCards.Engine.Components.SurprisePhaseStartTrigger",
        "default_data": {},
        "category": "Trigger"
    },
    "TurnStartTrigger": {
        "type": "PvZCards.Engine.Components.TurnStartTrigger",
        "default_data": {},
        "category": "Trigger"
    },

    # ==================== Filter 过滤器 ====================
    "TriggerTargetFilter": {
        "type": "PvZCards.Engine.Components.TriggerTargetFilter",
        "default_data": {},
        "child_prop": "Query",
        "is_list": False,
        "category": "Filter",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "TriggerSourceFilter": {
        "type": "PvZCards.Engine.Components.TriggerSourceFilter",
        "default_data": {},
        "child_prop": "Query",
        "is_list": False,
        "category": "Filter",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "QueryEntityCondition": {
        "type": "PvZCards.Engine.Components.QueryEntityCondition",
        "default_data": {
            "ConditionEvaluationType": "All"
        },
        "editable_params": {
            "ConditionEvaluationType": {"type": "enum", "options": ["All", "Any"]}
        },
        "category": "Filter"
    },
    "SelfEntityFilter": {
        "type": "PvZCards.Engine.Components.SelfEntityFilter",
        "default_data": {},
        "child_prop": "Query",
        "is_list": False,
        "category": "Filter",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "PlayerInfoCondition": {
        "type": "PvZCards.Engine.Components.PlayerInfoCondition",
        "default_data": {
            "Faction": "Plants"
        },
        "editable_params": {
            "Faction": {"type": "enum", "options": ["Plants", "Zombies"]}
        },
        "child_prop": "Query",
        "is_list": False,
        "category": "Filter",
        "allowed_children": ["CompositeQuery", "Query"]
    },

    # ==================== TargetSelector 目标选取 ====================
    "PrimaryTargetFilter": {
        "type": "PvZCards.Engine.Components.PrimaryTargetFilter",
        "default_data": {
            "SelectionType": "All",
            "NumTargets": 0,
            "TargetScopeType": "All",
            "TargetScopeSortValue": "None",
            "TargetScopeSortMethod": "None",
            "AdditionalTargetType": "None",
            "AdditionalTargetQuery": None,
            "OnlyApplyEffectsOnAdditionalTargets": False
        },
        "editable_params": {
            "SelectionType": {"type": "enum", "options": ["Manual", "Random", "All"]},
            "NumTargets": {"type": "int", "min": 0, "max": 2147483647},
            "TargetScopeType": {"type": "enum", "options": ["All", "Sorted"]},
            "TargetScopeSortValue": {"type": "enum", "options": ["None", "Attack", "Health"]},
            "TargetScopeSortMethod": {"type": "enum", "options": ["None", "Lowest", "Highest"]},
            "AdditionalTargetType": {"type": "enum", "options": ["None", "Query"]},
            "OnlyApplyEffectsOnAdditionalTargets": {"type": "bool"}
        },
        "child_prop": "Query",
        "is_list": False,
        "category": "TargetSelector",
        "allowed_children": ["CompositeQuery", "Query", "AdditionalTargetQuery"]
    },
    "SecondaryTargetFilter": {
        "type": "PvZCards.Engine.Components.SecondaryTargetFilter",
        "default_data": {
            "SelectionType": "All",
            "NumTargets": 0,
            "TargetScopeType": "All",
            "TargetScopeSortValue": "None",
            "TargetScopeSortMethod": "None",
            "AdditionalTargetType": "None",
            "AdditionalTargetQuery": None,
            "OnlyApplyEffectsOnAdditionalTargets": False
        },
        "editable_params": {
            "SelectionType": {"type": "enum", "options": ["Manual", "Random", "All"]},
            "NumTargets": {"type": "int", "min": 0, "max": 2147483647},
            "TargetScopeType": {"type": "enum", "options": ["All", "Sorted"]},
            "TargetScopeSortValue": {"type": "enum", "options": ["None", "Attack", "Health"]},
            "TargetScopeSortMethod": {"type": "enum", "options": ["None", "Lowest", "Highest"]},
            "AdditionalTargetType": {"type": "enum", "options": ["None", "Query"]},
            "OnlyApplyEffectsOnAdditionalTargets": {"type": "bool"}
        },
        "child_prop": "Query",
        "is_list": False,
        "category": "TargetSelector",
        "allowed_children": ["CompositeQuery", "Query", "AdditionalTargetQuery"]
    },

    # ==================== Condition 限制配置 ====================
    "OncePerGameCondition": {
        "type": "PvZCards.Engine.Components.OncePerGameCondition",
        "default_data": {},
        "category": "Condition"
    },
    "OncePerTurnCondition": {
        "type": "PvZCards.Engine.Components.OncePerTurnCondition",
        "default_data": {},
        "category": "Condition"
    },
    "PersistsAfterTransform": {
        "type": "PvZCards.Engine.Components.PersistsAfterTransform",
        "default_data": {},
        "category": "Condition"
    },

    # ==================== CompositeQuery 复合查询 ====================
    "CompositeAllQuery": {
        "type": "PvZCards.Engine.Queries.CompositeAllQuery",
        "default_data": {},
        "child_prop": "queries",
        "is_list": True,
        "category": "CompositeQuery",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "CompositeAnyQuery": {
        "type": "PvZCards.Engine.Queries.CompositeAnyQuery",
        "default_data": {},
        "child_prop": "queries",
        "is_list": True,
        "category": "CompositeQuery",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "NotQuery": {
        "type": "PvZCards.Engine.Queries.NotQuery",
        "default_data": {},
        "child_prop": "Query",
        "is_list": False,
        "category": "CompositeQuery",
        "allowed_children": ["CompositeQuery", "Query"]
    },

    # ==================== Query 原子查询 ====================
    # ---------- 无参数 ----------
    "AlwaysMatchesQuery": {
        "type": "PvZCards.Engine.Queries.AlwaysMatchesQuery",
        "default_data": {},
        "category": "Query"
    },
    "BehindSameLaneQuery": {
        "type": "PvZCards.Engine.Queries.BehindSameLaneQuery",
        "default_data": {},
        "category": "Query"
    },
    "DrawnCardQuery": {
        "type": "PvZCards.Engine.Queries.DrawnCardQuery",
        "default_data": {},
        "category": "Query"
    },
    "FighterQuery": {
        "type": "PvZCards.Engine.Queries.FighterQuery",
        "default_data": {},
        "category": "Query"
    },
    "InEnvironmentQuery": {
        "type": "PvZCards.Engine.Queries.InEnvironmentQuery",
        "default_data": {},
        "category": "Query"
    },
    "InHandQuery": {
        "type": "PvZCards.Engine.Queries.InHandQuery",
        "default_data": {},
        "category": "Query"
    },
    "InLaneQuery": {
        "type": "PvZCards.Engine.Queries.InLaneQuery",
        "default_data": {},
        "category": "Query"
    },
    "InOneTimeEffectZoneQuery": {
        "type": "PvZCards.Engine.Queries.InOneTimeEffectZoneQuery",
        "default_data": {},
        "category": "Query"
    },
    "InUnopposedLaneQuery": {
        "type": "PvZCards.Engine.Queries.InUnopposedLaneQuery",
        "default_data": {},
        "category": "Query"
    },
    "IsActiveQuery": {
        "type": "PvZCards.Engine.Queries.IsActiveQuery",
        "default_data": {},
        "category": "Query"
    },
    "IsAliveQuery": {
        "type": "PvZCards.Engine.Queries.IsAliveQuery",
        "default_data": {},
        "category": "Query"
    },
    "LastLaneOfSelfQuery": {
        "type": "PvZCards.Engine.Queries.LastLaneOfSelfQuery",
        "default_data": {},
        "category": "Query"
    },
    "OriginalTargetCardGuidQuery": {
        "type": "PvZCards.Engine.Queries.OriginalTargetCardGuidQuery",
        "default_data": {},
        "category": "Query"
    },
    "SameFactionQuery": {
        "type": "PvZCards.Engine.Queries.SameFactionQuery",
        "default_data": {},
        "category": "Query"
    },
    "SameLaneAsTargetQuery": {
        "type": "PvZCards.Engine.Queries.SameLaneAsTargetQuery",
        "default_data": {},
        "category": "Query"
    },
    "SameLaneQuery": {
        "type": "PvZCards.Engine.Queries.SameLaneQuery",
        "default_data": {},
        "category": "Query"
    },
    "SelfQuery": {
        "type": "PvZCards.Engine.Queries.SelfQuery",
        "default_data": {},
        "category": "Query"
    },
    "SourceQuery": {
        "type": "PvZCards.Engine.Queries.SourceQuery",
        "default_data": {},
        "category": "Query"
    },
    "SpringboardedOnSelfQuery": {
        "type": "PvZCards.Engine.Queries.SpringboardedOnSelfQuery",
        "default_data": {},
        "category": "Query"
    },
    "TargetCardGuidQuery": {
        "type": "PvZCards.Engine.Queries.TargetCardGuidQuery",
        "default_data": {},
        "category": "Query"
    },
    "TargetQuery": {
        "type": "PvZCards.Engine.Queries.TargetQuery",
        "default_data": {},
        "category": "Query"
    },
    "TargetableInPlayFighterQuery": {
        "type": "PvZCards.Engine.Queries.TargetableInPlayFighterQuery",
        "default_data": {},
        "category": "Query"
    },
    "TrickQuery": {
        "type": "PvZCards.Engine.Queries.TrickQuery",
        "default_data": {},
        "category": "Query"
    },
    "WasInSameLaneAsSelfQuery": {
        "type": "PvZCards.Engine.Queries.WasInSameLaneAsSelfQuery",
        "default_data": {},
        "category": "Query"
    },
    "WillTriggerEffectsQuery": {
        "type": "PvZCards.Engine.Queries.WillTriggerEffectsQuery",
        "default_data": {},
        "category": "Query"
    },
    "WillTriggerOnDeathEffectsQuery": {
        "type": "PvZCards.Engine.Queries.WillTriggerOnDeathEffectsQuery",
        "default_data": {},
        "category": "Query"
    },

    # ---------- 单参数 ----------
    "AdjacentLaneQuery": {
        "type": "PvZCards.Engine.Queries.AdjacentLaneQuery",
        "default_data": {"Side": "Either", "OriginEntityType": "Self"},
        "editable_params": {
            "Side": {"type": "enum", "options": ["Either", "ToTheLeft", "ToTheRight"]},
            "OriginEntityType": {"type": "enum", "options": ["Self", "Source", "Target"]}
        },
        "category": "Query"
    },
    "CardGuidQuery": {
        "type": "PvZCards.Engine.Queries.CardGuidQuery",
        "default_data": {"Guid": 0},
        "editable_params": {"Guid": {"type": "int", "min": 0, "max": 2147483647}},
        "category": "Query"
    },
    "InAdjacentLaneQuery": {
        "type": "PvZCards.Engine.Queries.InAdjacentLaneQuery",
        "default_data": {"Side": "Either"},
        "editable_params": {"Side": {"type": "enum", "options": ["Either", "ToTheLeft", "ToTheRight"]}},
        "category": "Query"
    },
    "InLaneAdjacentToLaneQuery": {
        "type": "PvZCards.Engine.Queries.InLaneAdjacentToLaneQuery",
        "default_data": {"Side": "Either"},
        "editable_params": {"Side": {"type": "enum", "options": ["Either", "ToTheLeft", "ToTheRight"]}},
        "category": "Query"
    },
    "InLaneSameAsLaneQuery": {
        "type": "PvZCards.Engine.Queries.InLaneSameAsLaneQuery",
        "default_data": {},
        "category": "Query"
    },
    "InSameLaneQuery": {
        "type": "PvZCards.Engine.Queries.InSameLaneQuery",
        "default_data": {"OriginEntityType": "Self"},
        "editable_params": {"OriginEntityType": {"type": "enum", "options": ["Self", "Source", "Target"]}},
        "category": "Query"
    },
    "LaneOfIndexQuery": {
        "type": "PvZCards.Engine.Queries.LaneOfIndexQuery",
        "default_data": {"LaneIndex": 0},
        "editable_params": {"LaneIndex": {"type": "int", "min": 0, "max": 2147483647}}, 
        "category": "Query"
    },
    "QueryMultiplier": {
        "type": "PvZCards.Engine.Components.QueryMultiplier",
        "default_data": {
            "Divider": 1
        },
        "editable_params": {
            "Divider": {"type": "int", "min": 1, "max": 2147483647}
        },
        "child_prop": "Query",
        "is_list": False,
        "category": "Query",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "SubsetQuery": {
        "type": "PvZCards.Engine.Queries.SubsetQuery",
        "default_data": {"Subset": ""},
        "editable_params": {"Subset": {"type": "string"}},
        "category": "Query"
    },
    "SubtypeQuery": {
        "type": "PvZCards.Engine.Queries.SubtypeQuery",
        "default_data": {"Subtype": 0},
        "editable_params": {"Subtype": {"type": "int", "min": 0, "max": 2147483647}},
        "category": "Query"
    },

    # ---------- 比较运算符 ----------
    "AttackComparisonQuery": {
        "type": "PvZCards.Engine.Queries.AttackComparisonQuery",
        "default_data": {"ComparisonOperator": "LessOrEqual", "AttackValue": 0},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "AttackValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "BlockMeterValueQuery": {
        "type": "PvZCards.Engine.Queries.BlockMeterValueQuery",
        "default_data": {"ComparisonOperator": "GreaterOrEqual", "BlockMeterValue": 10},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "BlockMeterValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "DamageTakenComparisonQuery": {
        "type": "PvZCards.Engine.Queries.DamageTakenComparisonQuery",
        "default_data": {"ComparisonOperator": "GreaterOrEqual", "DamageTakenValue": 1},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "DamageTakenValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "HealthComparisonQuery": {
        "type": "PvZCards.Engine.Queries.HealthComparisonQuery",
        "default_data": {
            "ComparisonOperator": "LessOrEqual",
            "HealthValue": 1
        },
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "HealthValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "SunCostComparisonQuery": {
        "type": "PvZCards.Engine.Queries.SunCostComparisonQuery",
        "default_data": {"ComparisonOperator": "LessOrEqual", "SunCost": 3},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "SunCost": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "SunCostPlusNComparisonQuery": {
        "type": "PvZCards.Engine.Queries.SunCostPlusNComparisonQuery",
        "default_data": {"ComparisonOperator": "Equal", "AdditionalCost": 1},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "AdditionalCost": {"type": "int", "min": -2147483648, "max": 2147483647}
        },
        "category": "Query"
    },
    "SunCounterComparisonQuery": {
        "type": "PvZCards.Engine.Queries.SunCounterComparisonQuery",
        "default_data": {"ComparisonOperator": "GreaterOrEqual", "SunCounterValue": 6},
        "editable_params": {
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]},
            "SunCounterValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Query"
    },
    "TurnCountQuery": {
        "type": "PvZCards.Engine.Queries.TurnCountQuery",
        "default_data": {"TurnCount": 1, "ComparisonOperator": "GreaterOrEqual"},
        "editable_params": {
            "TurnCount": {"type": "int", "min": 0, "max": 2147483647},
            "ComparisonOperator": {"type": "enum", "options": ["LessOrEqual", "Equal", "GreaterOrEqual"]}
        },
        "category": "Query"
    },

    # ---------- 组件类型 ----------
    "HasComponentQuery": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": ""},
        "editable_params": {"ComponentType": {"type": "component_picker"}},
        "category": "Query"
    },
    "LacksComponentQuery": {
        "type": "PvZCards.Engine.Queries.LacksComponentQuery",
        "default_data": {
            "ComponentType": "PvZCards.Engine.Components.FaceDown, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"
        },
        "editable_params": {"ComponentType": {"type": "component_picker"}},
        "category": "Query"
    },
    "OnTerrainQuery": {
        "type": "PvZCards.Engine.Queries.OnTerrainQuery",
        "default_data": {
            "TerrainType": "PvZCards.Engine.Components.GrassTerrain"
        },
        "editable_params": {"TerrainType": {"type": "terrain_picker"}},
        "category": "Query"
    },
    "OpenLaneQuery": {
        "type": "PvZCards.Engine.Queries.OpenLaneQuery",
        "default_data": {
            "PlayerFactionType": "PvZCards.Engine.Components.Plants",
            "IsForTeamupCard": False
        },
        "editable_params": {
            "PlayerFactionType": {"type": "enum", "options": ["PvZCards.Engine.Components.Plants, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null", "PvZCards.Engine.Components.Zombies, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"]},
            "IsForTeamupCard": {"type": "bool"}
        },
        "category": "Query"
    },

    # ---------- 预定义快捷方式 ----------
    "HasZombiesComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Zombies, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasPlantsComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Plants, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasPlayerComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Player, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasLaneComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Lane, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasFaceDownComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.FaceDown, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasEnvironmentComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Environment, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasWaterTerrainComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.WaterTerrain, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasHighgroundTerrainComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.HighgroundTerrain, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasUnhealableComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Unhealable, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },
    "HasSuperpowerComponent": {
        "type": "PvZCards.Engine.Queries.HasComponentQuery",
        "default_data": {"ComponentType": "PvZCards.Engine.Components.Superpower, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"},
        "category": "Query"
    },

    # ==================== Effect 效果 ====================
    # ---------- 无参数 ----------
    "CopyStatsEffect": {
        "type": "PvZCards.Engine.Components.CopyStatsEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "DestroyCardEffect": {
        "type": "PvZCards.Engine.Components.DestroyCardEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "ExtraAttackEffect": {
        "type": "PvZCards.Engine.Components.ExtraAttackEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "MixedUpGravediggerEffectDescriptor": {
        "type": "PvZCards.Engine.Components.MixedUpGravediggerEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "MoveCardToLanesEffectDescriptor": {
        "type": "PvZCards.Engine.Components.MoveCardToLanesEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "ReturnToHandEffect": {
        "type": "PvZCards.Engine.Components.ReturnToHandFromPlayEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "SlowEffect": {
        "type": "PvZCards.Engine.Components.SlowEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },
    "TurnIntoGravestoneEffectDescriptor": {
        "type": "PvZCards.Engine.Components.TurnIntoGravestoneEffectDescriptor",
        "default_data": {},
        "category": "Effect"
    },

    # ---------- 有参数（基础类型）----------
    "AttackInLaneEffectDescriptor": {
        "type": "PvZCards.Engine.Components.AttackInLaneEffectDescriptor",
        "default_data": {
            "DamageAmount": 4
        },
        "editable_params": {
            "DamageAmount": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Effect"
    },
    "BuffEffect": {
        "type": "PvZCards.Engine.Components.BuffEffectDescriptor",
        "default_data": {"AttackAmount": 1, "HealthAmount": 1, "BuffDuration": "Permanent"},
        "editable_params": {
            "AttackAmount": {"type": "int", "min": -2147483648, "max": 2147483647},
            "HealthAmount": {"type": "int", "min": -2147483648, "max": 2147483647},
            "BuffDuration": {"type": "enum", "options": ["Permanent", "EndOfTurn", "NextFighter"]}
        },
        "category": "Effect"
    },
    "ChargeBlockMeterEffectDescriptor": {
        "type": "PvZCards.Engine.Components.ChargeBlockMeterEffectDescriptor",
        "default_data": {
            "ChargeAmount": 10
        },
        "editable_params": {
            "ChargeAmount": {"type": "int", "min": -2147483648, "max": 2147483647}
        },
        "category": "Effect"
    },
    "CopyCardEffectDescriptor": {
        "type": "PvZCards.Engine.Components.CopyCardEffectDescriptor",
        "default_data": {
            "GrantTeamup": False,
            "ForceFaceDown": False,
            "CreateInFront": False
        },
        "editable_params": {
            "GrantTeamup": {"type": "bool"},
            "ForceFaceDown": {"type": "bool"},
            "CreateInFront": {"type": "bool"}
        },
        "category": "Effect"
    },
    "CreateCardEffect": {
        "type": "PvZCards.Engine.Components.CreateCardEffectDescriptor",
        "default_data": {"CardGuid": 0, "ForceFaceDown": False},
        "editable_params": {
            "CardGuid": {"type": "int", "min": 0, "max": 2147483647},
            "ForceFaceDown": {"type": "bool"}
        },
        "category": "Effect"
    },
    "CreateCardInDeckEffect": {
        "type": "PvZCards.Engine.Components.CreateCardInDeckEffectDescriptor",
        "default_data": {"CardGuid": 0, "AmountToCreate": 1, "DeckPosition": "Random"},
        "editable_params": {
            "CardGuid": {"type": "int", "min": 0, "max": 2147483647},
            "AmountToCreate": {"type": "int", "min": 1, "max": 2147483647},
            "DeckPosition": {"type": "enum", "options": ["Random", "Top", "Bottom"]}
        },
        "category": "Effect"
    },
    "DamageEffect": {
        "type": "PvZCards.Engine.Components.DamageEffectDescriptor",
        "default_data": {"DamageAmount": 4},
        "editable_params": {"DamageAmount": {"type": "int", "min": 0, "max": 2147483647}},
        "category": "Effect"
    },
    "DrawCardEffect": {
        "type": "PvZCards.Engine.Components.DrawCardEffectDescriptor",
        "default_data": {"DrawAmount": 1},
        "editable_params": {"DrawAmount": {"type": "int", "min": 1, "max": 2147483647}},
        "category": "Effect"
    },
    "EffectValueDescriptor": {
        "type": "PvZCards.Engine.Components.EffectValueDescriptor",
        "default_data": {
            "MappingType": "DamageToHeal"
        },
        "editable_params": {
            "MappingType": {
                "type": "enum",
                "options": [
                    "DamageToHeal",
                    "HealToDamage"
                ]
            }
        },
        "category": "Effect"
    },
    "GainSunEffect": {
        "type": "PvZCards.Engine.Components.GainSunEffectDescriptor",
        "default_data": {"Amount": 1, "Duration": "Permanent", "ActivationTime": "Immediate"},
        "editable_params": {
            "Amount": {"type": "int", "min": -2147483648, "max": 2147483647},
            "Duration": {"type": "enum", "options": ["Permanent", "EndOfTurn", "NextFighter"]},
            "ActivationTime": {"type": "enum", "options": ["Immediate", "NextTurn"]}
        },
        "category": "Effect"
    },
    "GrantAbilityEffect": {
        "type": "PvZCards.Engine.Components.GrantAbilityEffectDescriptor",
        "default_data": {
            "GrantableAbilityType": "Frenzy",
            "Duration": "Permanent",
            "AbilityValue": 0
        },
        "editable_params": {
            "GrantableAbilityType": {
                "type": "enum",
                "options": [
                    "Unhurtable", "Deadly", "Frenzy", "Truestrike",
                    "Strikethrough", "MinHealth", "NoExtraAttacks",
                    "GravestoneSpy", "Teamup", "Aquatic", "CanPlayFighterInSurprisePhase",
                    "Mustache", "AttackOverride", "MultiplyDamage", "Graveyard",
                    "Untrickable", "Unhealable"
                ]
            },
            "Duration": {"type": "enum", "options": ["Permanent", "EndOfTurn", "NextFighter"]},
            "AbilityValue": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Effect"
    },
    "GrantTriggeredAbilityEffectDescriptor": {
        "type": "PvZCards.Engine.Effects.GrantTriggeredAbilityEffectDescriptor",
        "default_data": {
            "AbilityGuid": 562,
            "AbilityValueType": "None",
            "AbilityValueAmount": 0
        },
        "editable_params": {
            "AbilityGuid": {"type": "int", "min": 0, "max": 2147483647},
            "AbilityValueType": {"type": "enum", "options": ["None", "Damage"]},
            "AbilityValueAmount": {"type": "int", "min": 0, "max": 2147483647}
        },
        "category": "Effect"
    },
    "HealEffect": {
        "type": "PvZCards.Engine.Components.HealEffectDescriptor",
        "default_data": {"HealAmount": 2},
        "editable_params": {"HealAmount": {"type": "int", "min": 1, "max": 2147483647}},
        "category": "Effect"
    },
    "HeroHealthMultiplier": {
        "type": "PvZCards.Engine.Components.HeroHealthMultiplier",
        "default_data": {
            "Faction": "Plants",
            "Divider": 1
        },
        "editable_params": {
            "Faction": {"type": "enum", "options": ["Plants", "Zombies"]},
            "Divider": {"type": "int", "min": 1, "max": 2147483647}
        },
        "category": "Effect"
    },
    "ModifySunCostEffect": {
        "type": "PvZCards.Engine.Components.ModifySunCostEffectDescriptor",
        "default_data": {"SunCostAmount": -1, "BuffDuration": "Permanent"},
        "editable_params": {
            "SunCostAmount": {"type": "int", "min": -2147483648, "max": 2147483647},
            "BuffDuration": {"type": "enum", "options": ["Permanent", "EndOfTurn", "NextFighter"]}
        },
        "category": "Effect"
    },
    "SetStatEffect": {
        "type": "PvZCards.Engine.Components.SetStatEffectDescriptor",
        "default_data": {
            "StatType": "Health",
            "Value": 20,
            "ModifyOperation": "Set",
            "StripNoncontinousModifiers": True
        },
        "editable_params": {
            "StatType": {"type": "enum", "options": ["Attack", "Health", "SunCost"]},
            "ModifyOperation": {"type": "enum", "options": ["Set", "Add"]},
            "Value": {"type": "int", "min": -2147483648, "max": 2147483647},
            "StripNoncontinousModifiers": {"type": "bool"}
        },
        "category": "Effect"
    },
    "SunGainedMultiplier": {
        "type": "PvZCards.Engine.Components.SunGainedMultiplier",
        "default_data": {
            "Faction": "Plants",
            "Divider": 1
        },
        "editable_params": {
            "Faction": {"type": "enum", "options": ["Plants", "Zombies"]},
            "Divider": {"type": "int", "min": 1, "max": 2147483647}
        },
        "category": "Effect"
    },
    "TargetAttackMultiplier": {
        "type": "PvZCards.Engine.Components.TargetAttackMultiplier",
        "default_data": {"Divider": 2},
        "editable_params": {"Divider": {"type": "int", "min": 1, "max": 2147483647}},
        "category": "Effect"
    },
    "TargetHealthMultiplier": {
        "type": "PvZCards.Engine.Components.TargetHealthMultiplier",
        "default_data": {"Divider": 2},
        "editable_params": {"Divider": {"type": "int", "min": 1, "max": 2147483647}},
        "category": "Effect"
    },

    # ---------- 有子节点 ----------
    "CreateCardFromSubsetEffectDescriptor": {
        "type": "PvZCards.Engine.Components.CreateCardFromSubsetEffectDescriptor",
        "default_data": {
            "ForceFaceDown": False
        },
        "editable_params": {
            "ForceFaceDown": {"type": "bool"}
        },
        "child_prop": "SubsetQuery",
        "is_list": False,
        "category": "ComplexEffect",
        "allowed_children": ["CompositeQuery", "Query"]
    },
    "TransformIntoCardFromSubsetEffectDescriptor": {
        "type": "PvZCards.Engine.Components.TransformIntoCardFromSubsetEffectDescriptor",
        "default_data": {},
        "child_prop": "SubsetQuery",
        "is_list": False,
        "category": "ComplexEffect",
        "allowed_children": ["CompositeQuery", "Query"]
    },

    # ==================== ComplexEffect 复合效果 ====================
    "DrawCardFromSubsetEffect": {
        "type": "PvZCards.Engine.Components.DrawCardFromSubsetEffectDescriptor",
        "default_data": {"DrawAmount": 1},
        "editable_params": {"DrawAmount": {"type": "int", "min": 1, "max": 2147483647}},
        "child_prop": "SubsetQuery",
        "is_list": False,
        "category": "ComplexEffect",
        "allowed_children": ["CompositeQuery", "Query"]
    },

    # ==================== Virtual 虚拟/UI辅助 ====================
    "AdditionalTargetQuery": {
        "type": "Virtual.UI.AdditionalTargetQuery",
        "default_data": {},
        "category": "Virtual",
        "allowed_children": ["CompositeQuery", "Query"]
    },
}