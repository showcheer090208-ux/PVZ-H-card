# logic_translator.py
from core_utils import safe_get
from constants import parse_type_str
import localization

def parse_query(query_data):
    if not query_data: 
        return ""
    comp_name = parse_type_str(query_data.get("$type", ""))
    d = query_data.get("$data", {})

    # ========= 复合查询 =========
    if comp_name == "CompositeAllQuery":
        return " 且 ".join(filter(None, [parse_query(q) for q in d.get("queries", [])]))
    if comp_name == "CompositeAnyQuery":
        return " 或 ".join(filter(None, [parse_query(q) for q in d.get("queries", [])]))
    if comp_name == "NotQuery":
        inner = parse_query(d.get("Query", {}))
        return f"不满足【{inner}】" if inner else "否定条件"

    # ========= 原子条件查表法 =========
    query_map = {
        "SelfQuery": "其自身",
        "TargetQuery": "目标",
        "InSameLaneQuery": "同一行的",
        "InLaneSameAsLaneQuery": "相同指定行的",
        "TargetableInPlayFighterQuery": "场上的斗士",
        "WillTriggerOnDeathEffectsQuery": "具备死亡效果的",
        "AlwaysMatchesQuery": "所有目标",
        "BehindSameLaneQuery": "同行的后面",
        "DrawnCardQuery": "抽到的卡牌",
        "FighterQuery": "斗士单位",
        "InEnvironmentQuery": "场地上的",
        "InHandQuery": "手牌中的",
        "InLaneQuery": "行内的",
        "InOneTimeEffectZoneQuery": "一次性效果区的",
        "InUnopposedLaneQuery": "无对手的行中的",
        "IsActiveQuery": "激活状态的",
        "IsAliveQuery": "存活状态的",
        "LastLaneOfSelfQuery": "自身的最后一行",
        "OriginalTargetCardGuidQuery": "原始目标卡牌",
        "SameFactionQuery": "同阵营的",
        "SameLaneAsTargetQuery": "与目标同行的",
        "SameLaneQuery": "同一行的",
        "SourceQuery": "来源",
        "SpringboardedOnSelfQuery": "跳板作用于自身的",
        "TargetCardGuidQuery": "目标的卡牌",
        "TrickQuery": "锦囊/法术",
        "WasInSameLaneAsSelfQuery": "曾与自身同行的",
        "WillTriggerEffectsQuery": "将触发效果的",
        "HasZombiesComponent": "僵尸",
        "HasPlantsComponent": "植物",
        "HasPlayerComponent": "英雄/玩家",
        "HasLaneComponent": "整行(地段)",
        "HasSuperpowerComponent": "英雄技能",
        "HasFaceDownComponent": "暗置/墓碑",
        "HasEnvironmentComponent": "场地牌",
        "HasWaterTerrainComponent": "水域地形",
        "HasHighgroundTerrainComponent": "高地地形",
        "HasUnhealableComponent": "不可治疗",
    }
    if comp_name in query_map:
        return query_map[comp_name]

    # ========= 带参数的原子条件 =========
    if comp_name == "AdjacentLaneQuery":
        side = d.get("Side", "Either")
        origin = d.get("OriginEntityType", "Self")
        side_str = {"ToTheLeft": "左侧", "ToTheRight": "右侧", "Either": "任意侧"}.get(side, "相邻")
        origin_str = {"Self": "自身", "Source": "来源", "Target": "目标"}.get(origin, "自身")
        return f"{origin_str}的{side_str}相邻行"
    
    if comp_name == "InAdjacentLaneQuery":
        side = d.get("Side", "Either")
        return {"ToTheLeft": "左侧相邻行", "ToTheRight": "右侧相邻行", "Either": "相邻行"}.get(side, "相邻行")
    
    if comp_name == "InLaneAdjacentToLaneQuery":
        side = d.get("Side", "Either")
        return {"ToTheLeft": "左侧相邻行的", "ToTheRight": "右侧相邻行的"}.get(side, "相邻行的")
    
    if comp_name == "InSameLaneQuery":
        origin = d.get("OriginEntityType", "Self")
        origin_str = {"Self": "自身", "Source": "来源", "Target": "目标"}.get(origin, "自身")
        return f"与{origin_str}同一行的"
    
    if comp_name == "LaneOfIndexQuery":
        idx = d.get("LaneIndex", 0)
        return f"第{idx + 1}行的"
    
    if comp_name == "SubsetQuery":
        subset = d.get("Subset", "")
        return f"属于【{subset}】标签的" if subset else "特定标签的"
    
    if comp_name == "SubtypeQuery":
        subtype = d.get("Subtype", 0)
        return f"种族ID为{subtype}的"
    
    if comp_name == "CardGuidQuery":
        guid = d.get("Guid", 0)
        return f"卡牌GUID为{guid}的"
    
    if comp_name == "QueryMultiplier":
        divider = d.get("Divider", 1)
        inner = parse_query(d.get("Query", {}))
        return f"({inner}) 的数值除以 {divider}" if inner else f"查询结果除以 {divider}"
    
    if comp_name == "HasComponentQuery":
        comp_type = d.get("ComponentType", "")
        if "Zombies" in comp_type: return "僵尸"
        if "Plants" in comp_type: return "植物"
        if "Lane" in comp_type: return "地段(整行)"
        if "Player" in comp_type: return "英雄/玩家"
        if "Superpower" in comp_type: return "英雄技能"
        if "Environment" in comp_type: return "场地"
        if "FaceDown" in comp_type: return "暗置/墓碑"
        return "特定实体"
    
    if comp_name == "LacksComponentQuery":
        comp_type = d.get("ComponentType", "")
        return "缺少特定组件的"
    
    if comp_name == "OnTerrainQuery":
        terrain_type = d.get("TerrainType", "")
        if "Water" in terrain_type: return "在水域地形上"
        if "Highground" in terrain_type: return "在高地地形上"
        return "在特定地形上"
    
    if comp_name == "OpenLaneQuery":
        faction = d.get("PlayerFactionType", "Plants")
        faction_str = "植物" if "Plants" in faction else "僵尸"
        is_teamup = d.get("IsForTeamupCard", False)
        teamup_str = "（可为组队卡）" if is_teamup else ""
        return f"{faction_str}方的空行{teamup_str}"
    
    # ========= 比较运算符查询 =========
    if comp_name == "AttackComparisonQuery":
        op = d.get("ComparisonOperator", "LessOrEqual")
        val = d.get("AttackValue", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≤")
        return f"攻击力{op_str}{val}的"
    
    if comp_name == "HealthComparisonQuery":
        op = d.get("ComparisonOperator", "LessOrEqual")
        val = d.get("HealthValue", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≤")
        return f"生命值{op_str}{val}的"
    
    if comp_name == "BlockMeterValueQuery":
        op = d.get("ComparisonOperator", "GreaterOrEqual")
        val = d.get("BlockMeterValue", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≥")
        return f"格挡值{op_str}{val}的"
    
    if comp_name == "DamageTakenComparisonQuery":
        op = d.get("ComparisonOperator", "GreaterOrEqual")
        val = d.get("DamageTakenValue", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≥")
        return f"已受伤害{op_str}{val}的"
    
    if comp_name == "SunCostComparisonQuery":
        op = d.get("ComparisonOperator", "LessOrEqual")
        val = d.get("SunCost", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≤")
        return f"费用{op_str}{val}的"
    
    if comp_name == "SunCostPlusNComparisonQuery":
        op = d.get("ComparisonOperator", "Equal")
        val = d.get("AdditionalCost", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "=")
        return f"费用+{val}{op_str}比较的"
    
    if comp_name == "SunCounterComparisonQuery":
        op = d.get("ComparisonOperator", "GreaterOrEqual")
        val = d.get("SunCounterValue", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≥")
        return f"阳光计数器{op_str}{val}的"
    
    if comp_name == "TurnCountQuery":
        op = d.get("ComparisonOperator", "GreaterOrEqual")
        val = d.get("TurnCount", 0)
        op_str = {"LessOrEqual": "≤", "Equal": "=", "GreaterOrEqual": "≥"}.get(op, "≥")
        return f"回合数{op_str}{val}的"
    
    return ""


def translate_entities_to_text(entities):
    if not entities:
        return "暂无技能配置。\n(请在左侧双击组件添加，或在上方新建技能组)"

    descriptions = []
    for i, entity in enumerate(entities):
        comps = entity.get("components", [])
        trigger_actions, trigger_targets, effects, targets, conditions = [], [], [], [], []

        for comp in comps:
            comp_name = parse_type_str(comp.get("$type", ""))
            d = comp.get("$data", {})

            # ========= 触发器 =========
            if comp_name == "PlayTrigger":
                trigger_actions.append("打出")
            elif comp_name == "DiscardFromPlayTrigger":
                trigger_actions.append("被消灭/离场")
            elif comp_name == "BuffTrigger":
                trigger_actions.append("获得属性提升")
            elif comp_name == "DamageTrigger":
                trigger_actions.append("造成伤害")
            elif comp_name == "HealTrigger":
                trigger_actions.append("治疗")
            elif comp_name == "DrawCardTrigger":
                trigger_actions.append("抽牌")
            elif comp_name == "DrawCardFromSubsetTrigger":
                trigger_actions.append("从特定子集抽牌")
            elif comp_name == "EnterBoardTrigger":
                trigger_actions.append("进场")
            elif comp_name == "ExtraAttackTrigger":
                trigger_actions.append("额外攻击")
            elif comp_name == "TurnStartTrigger":
                trigger_actions.append("回合开始")
            elif comp_name == "CombatEndTrigger":
                trigger_actions.append("战斗结束")
            elif comp_name == "LaneCombatEndTrigger":
                trigger_actions.append("单路战斗结束")
            elif comp_name == "LaneCombatStartTrigger":
                trigger_actions.append("单路战斗开始")
            elif comp_name == "MoveTrigger":
                trigger_actions.append("移动")
            elif comp_name == "ReturnToHandTrigger":
                trigger_actions.append("返回手牌")
            elif comp_name == "RevealTrigger":
                trigger_actions.append("揭示")
            elif comp_name == "RevealPhaseEndTrigger":
                trigger_actions.append("揭示阶段结束")
            elif comp_name == "SlowedTrigger":
                trigger_actions.append("被冰冻")
            elif comp_name == "SurprisePhaseStartTrigger":
                trigger_actions.append("奇袭阶段开始")
            
            # ========= 过滤器 =========
            elif comp_name in ("TriggerTargetFilter", "TriggerSourceFilter"):
                q = parse_query(d.get("Query", {}))
                if q:
                    trigger_targets.append(q)
            elif comp_name == "SelfEntityFilter":
                q = parse_query(d.get("Query", {}))
                if q:
                    trigger_targets.append(f"自身满足【{q}】")
            elif comp_name == "PlayerInfoCondition":
                faction = d.get("Faction", "Plants")
                faction_str = "植物" if faction == "Plants" else "僵尸"
                q = parse_query(d.get("Query", {}))
                if q:
                    trigger_targets.append(f"{faction_str}方满足【{q}】")
                else:
                    trigger_targets.append(f"{faction_str}方")
            elif comp_name == "QueryEntityCondition":
                eval_type = d.get("ConditionEvaluationType", "All")
                eval_str = "全部满足" if eval_type == "All" else "任意满足"
                # 这个需要特殊处理 Finder 和 Query，这里简化
                trigger_targets.append(f"实体条件判断({eval_str})")
            
            # ========= 限制条件 =========
            elif comp_name == "OncePerGameCondition":
                conditions.append("每局游戏只能触发一次")
            elif comp_name == "OncePerTurnCondition":
                conditions.append("每回合只能触发一次")
            elif comp_name == "PersistsAfterTransform":
                conditions.append("变形后保留此技能")

            # ========= 目标选取 =========
            elif comp_name in ("PrimaryTargetFilter", "SecondaryTargetFilter"):
                sel = d.get("SelectionType", "All")
                num = d.get("NumTargets", 0)
                query_str = parse_query(d.get("Query", {})) or "目标"
                if sel == "Manual":
                    targets.append(f"玩家手动选择的 1 个【{query_str}】")
                elif sel == "Random":
                    targets.append(f"随机选择的 {num} 个【{query_str}】")
                else:
                    targets.append(f"所有【{query_str}】")
                
                # 额外目标
                if d.get("AdditionalTargetType") == "Query":
                    targets.append("（额外目标条件已启用）")
            
            # ========= 效果 =========
            elif comp_name == "DamageEffect":
                effects.append(f"造成 {d.get('DamageAmount', 0)} 点伤害")
            
            elif comp_name == "BuffEffect":
                dur = "永久" if d.get("BuffDuration", "Permanent") == "Permanent" else "本回合"
                try:
                    effects.append(f"{dur}获得 {int(d.get('AttackAmount', 0)):+d} 攻击力 / {int(d.get('HealthAmount', 0)):+d} 生命值")
                except ValueError:
                    effects.append(f"{dur}获得属性改变")
            
            elif comp_name == "DestroyCardEffect":
                effects.append("将其直接消灭")
            
            elif comp_name == "AttackInLaneEffectDescriptor":
                effects.append(f"对本行造成 {d.get('DamageAmount', 0)} 点伤害")
            
            elif comp_name == "ChargeBlockMeterEffectDescriptor":
                effects.append(f"充能格挡值 {d.get('ChargeAmount', 0)}")
            
            elif comp_name == "CopyCardEffectDescriptor":
                parts = []
                if d.get("GrantTeamup"): parts.append("赋予组队能力")
                if d.get("ForceFaceDown"): parts.append("强制暗置")
                if d.get("CreateInFront"): parts.append("在身前创建")
                effects.append(f"复制卡牌" + (f"({', '.join(parts)})" if parts else ""))
            
            elif comp_name == "CopyStatsEffect":
                effects.append("复制目标的属性数值")
            
            elif comp_name == "CreateCardEffect":
                face_down = "以墓碑/潜行方式" if d.get("ForceFaceDown") else ""
                effects.append(f"{face_down}召唤卡牌 ID:{d.get('CardGuid', 0)}")
            
            elif comp_name == "CreateCardInDeckEffect":
                effects.append(f"将 {d.get('AmountToCreate', 1)} 张 ID 为 {d.get('CardGuid', 0)} 的卡牌洗入牌库")
            
            elif comp_name == "CreateCardFromSubsetEffectDescriptor":
                face_down = "强制暗置" if d.get("ForceFaceDown") else ""
                effects.append(f"从指定子集生成卡牌{face_down}")
            
            elif comp_name == "TransformIntoCardFromSubsetEffectDescriptor":
                effects.append("变身为指定子集中的卡牌")
            
            elif comp_name == "DrawCardEffect":
                effects.append(f"抽 {d.get('DrawAmount', 1)} 张牌")
            
            elif comp_name == "DrawCardFromSubsetEffect":
                effects.append(f"从指定子集中抽 {d.get('DrawAmount', 1)} 张牌")
            
            elif comp_name == "ExtraAttackEffect":
                effects.append("获得额外一次攻击机会")
            
            elif comp_name == "GainSunEffect":
                act_time = "立即" if d.get("ActivationTime") == "Immediate" else "下回合"
                effects.append(f"{act_time}获得 {d.get('Amount', 0)} 点阳光/脑子")
            
            elif comp_name == "GrantAbilityEffect":
                ability = localization.ENUM_NAMES.get(d.get("GrantableAbilityType"), d.get("GrantableAbilityType"))
                dur = "永久" if d.get("Duration") == "Permanent" else "本回合"
                val_note = ""
                if d.get("GrantableAbilityType") == "Untrickable":
                    val_note = " (免疫植物)" if d.get("AbilityValue") == 1 else " (免疫僵尸)" if d.get("AbilityValue") == 2 else ""
                effects.append(f"{dur}赋予技能【{ability}】{val_note}")
            
            elif comp_name == "GrantTriggeredAbilityEffectDescriptor":
                guid = d.get("AbilityGuid", 0)
                val_type = d.get("AbilityValueType", "None")
                val_amount = d.get("AbilityValueAmount", 0)
                if val_type == "Damage":
                    effects.append(f"赋予触发能力 GUID:{guid}，伤害值 {val_amount}")
                else:
                    effects.append(f"赋予触发能力 GUID:{guid}")
            
            elif comp_name == "HealEffect":
                effects.append(f"治疗 {d.get('HealAmount', 0)} 点生命值")
            
            elif comp_name == "HeroHealthMultiplier":
                faction = d.get("Faction", "Plants")
                faction_str = "植物" if faction == "Plants" else "僵尸"
                divider = d.get("Divider", 1)
                effects.append(f"{faction_str}英雄血量变为原来的 1/{divider}")
            
            elif comp_name == "ModifySunCostEffect":
                dur = "永久" if d.get("BuffDuration") == "Permanent" else "本回合"
                effects.append(f"{dur}使卡牌花费改变 {d.get('SunCostAmount', 0)}")
            
            elif comp_name == "MixedUpGravediggerEffectDescriptor":
                effects.append("触发掘墓人效果")
            
            elif comp_name == "MoveCardToLanesEffectDescriptor":
                effects.append("移动卡牌到指定行")
            
            elif comp_name == "ReturnToHandEffect":
                effects.append("将其弹回手牌")
            
            elif comp_name == "SetStatEffect":
                stat = d.get("StatType", "Health")
                stat_str = {"Attack": "攻击力", "Health": "生命值", "SunCost": "费用"}.get(stat, stat)
                op = "增加" if d.get("ModifyOperation") == "Add" else "重置为"
                val = d.get("Value", 0)
                effects.append(f"将{stat_str}{op} {val}")
            
            elif comp_name == "SlowEffect":
                effects.append("冰冻目标")
            
            elif comp_name == "SunGainedMultiplier":
                faction = d.get("Faction", "Plants")
                faction_str = "植物" if faction == "Plants" else "僵尸"
                divider = d.get("Divider", 1)
                effects.append(f"{faction_str}方获得的阳光变为原来的 1/{divider}")
            
            elif comp_name == "TargetAttackMultiplier":
                effects.append(f"攻击力变为 {d.get('Divider', 1)} 倍")
            
            elif comp_name == "TargetHealthMultiplier":
                effects.append(f"生命值变为 {d.get('Divider', 1)} 倍")
            
            elif comp_name == "TurnIntoGravestoneEffectDescriptor":
                effects.append("转化为墓碑")
            
            elif comp_name == "EffectValueDescriptor":
                mapping = d.get("MappingType", "DamageToHeal")
                if mapping == "DamageToHeal":
                    effects.append("数值映射：伤害量 → 治疗量")
                elif mapping == "HealToDamage":
                    effects.append("数值映射：治疗量 → 伤害量")
                else:
                    effects.append("数值映射")
            
            elif comp_name == "SlowEffect":
                effects.append("冰冻目标")

        # ========= 组装语义 =========
        # 限制条件前缀
        cond_str = ""
        if conditions:
            cond_str = f"【限制】{', '.join(conditions)}。"
        
        # 触发器
        trigger_str = "【被动生效】"
        if trigger_actions:
            tgt = "、".join(trigger_targets) if trigger_targets else "此卡牌"
            trigger_str = f"当【{tgt}】{'或'.join(trigger_actions)}时，"
        
        # 目标
        target_str = f"对 {'、'.join(targets)}，" if targets else ""
        
        # 效果
        effect_str = f"{'、'.join(effects)}。" if effects else "未配置实际效果。"
        
        descriptions.append(f"🔹 技能组 {i+1}：\n{cond_str}{trigger_str}{target_str}{effect_str}")

    return "\n\n".join(descriptions)