# localization.py
# 统一管理所有组件在 UI 上的中文/本地化显示名称

NODE_NAMES = {
    # ==================== Framework 基础框架 ====================
    "EffectEntityGrouping": "⚙️ 基础框架 (EffectEntityGrouping)",

    # ==================== Trigger 触发器 ====================
    "PlayTrigger": "🟢 触发: 当打出时",
    "DiscardFromPlayTrigger": "🟢 触发: 当死亡时",
    "BuffTrigger": "🟢 触发: 当获得属性加成时",
    "CombatEndTrigger": "🟢 触发: 战斗结束时",
    "DamageTrigger": "🟢 触发: 受到伤害时",
    "DestroyCardTrigger": "🟢 触发: 消灭卡牌时",
    "DrawCardTrigger": "🟢 触发: 抽牌时",
    "DrawCardFromSubsetTrigger": "🟢 触发: 召唤卡牌触发",
    "EnterBoardTrigger": "🟢 触发: 进场时",
    "ExtraAttackTrigger": "🟢 触发: 额外攻击时",
    "HealTrigger": "🟢 触发: 治疗时",
    "LaneCombatEndTrigger": "🟢 触发: 单路战斗结束时",
    "LaneCombatStartTrigger": "🟢 触发: 单路战斗开始时",
    "MoveTrigger": "🟢 触发: 移动时",
    "ReturnToHandTrigger": "🟢 触发: 返回手牌时",
    "RevealPhaseEndTrigger": "🟢 触发: 揭示阶段结束时",
    "RevealTrigger": "🟢 触发: 揭示时",
    "SlowedTrigger": "🟢 触发: 被冰冻时",
    "SurprisePhaseStartTrigger": "🟢 触发: 奇袭阶段开始时",
    "TurnStartTrigger": "🟢 触发: 回合开始时",

    # ==================== Filter 过滤器 ====================
    "TriggerTargetFilter": "🟡 触发目标限制 (TriggerTargetFilter)",
    "TriggerSourceFilter": "🟡 触发来源限制 (TriggerSourceFilter)",
    "QueryEntityCondition": "🟡 实体条件判断 (QueryEntityCondition)",
    "SelfEntityFilter": "🟡 自身实体过滤 (SelfEntityFilter)",
    "PlayerInfoCondition": "🟡 玩家信息条件 (PlayerInfoCondition)",

    # ==================== TargetSelector 目标选取 ====================
    "PrimaryTargetFilter": "🟠 执行目标选取 (PrimaryTargetFilter)",
    "SecondaryTargetFilter": "🎯 次要目标选取 (SecondaryTargetFilter)",

    # ==================== Condition 限制配置 ====================
    "OncePerGameCondition": "🟣 限制: 每局一次",
    "OncePerTurnCondition": "🟣 限制: 每回合一次",
    "PersistsAfterTransform": "🟣 限制: 变形后保留技能 (PersistsAfterTransform)",

    # ==================== CompositeQuery 复合查询 ====================
    "CompositeAllQuery": "🔗 满足所有条件 [AND]",
    "CompositeAnyQuery": "🔗 满足任一条件 [OR]",
    "NotQuery": "🔗 否定 (NOT)",

    # ==================== Query 原子查询 ====================
    # ---------- 无参数 ----------
    "AlwaysMatchesQuery": "🔵 条件: 永远匹配",
    "BehindSameLaneQuery": "🔵 范围: 在同行的后面",
    "DrawnCardQuery": "🔵 对象: 抽到的卡牌",
    "FighterQuery": "🔵 条件: 是斗士单位",
    "InEnvironmentQuery": "🔵 范围: 在场地上",
    "InHandQuery": "🔵 范围: 在手牌中",
    "InLaneQuery": "🔵 范围: 在行内",
    "InOneTimeEffectZoneQuery": "🔵 范围: 在一次性效果区",
    "InUnopposedLaneQuery": "🔵 条件: 在无对手的行",
    "IsActiveQuery": "🔵 条件: 处于激活状态",
    "IsAliveQuery": "🔵 条件: 存活状态",
    "LastLaneOfSelfQuery": "🔵 范围: 自身的最后一行",
    "OriginalTargetCardGuidQuery": "🔵 对象: 原始目标卡牌",
    "SameFactionQuery": "🔵 条件: 同阵营",
    "SameLaneAsTargetQuery": "🔵 范围: 与目标同行",
    "SameLaneQuery": "🔵 范围: 在同一行",
    "SelfQuery": "🔵 对象: 自己",
    "SourceQuery": "🔵 对象: 来源",
    "SpringboardedOnSelfQuery": "🔵 条件: 跳板作用于自身",
    "TargetCardGuidQuery": "🔵 对象: 目标的卡牌",
    "TargetQuery": "🔵 对象: 选中的目标",
    "TargetableInPlayFighterQuery": "🔵 条件: 场上可选中单位",
    "TrickQuery": "🔵 条件: 是锦囊/法术",
    "WasInSameLaneAsSelfQuery": "🔵 范围: 曾与自身同行",
    "WillTriggerEffectsQuery": "🔵 条件: 将触发效果",
    "WillTriggerOnDeathEffectsQuery": "🔵 条件: 将触发死亡效果",

    # ---------- 单参数 ----------
    "AdjacentLaneQuery": "🔵 范围: 相邻的行 (指定来源)",
    "CardGuidQuery": "🔵 条件: 卡牌GUID匹配",
    "InAdjacentLaneQuery": "🔵 范围: 在相邻的行",
    "InLaneAdjacentToLaneQuery": "🔵 范围: 在相邻的行",
    "InLaneSameAsLaneQuery": "🔵 范围: 行数相同匹配",
    "InSameLaneQuery": "🔵 范围: 在同一行",
    "LaneOfIndexQuery": "🔵 范围: 指定索引的行",
    "QueryMultiplier": "🔵 查询倍率 (QueryMultiplier)",
    "SubsetQuery": "🔵 条件: 属于特定子集",
    "SubtypeQuery": "🔵 条件: 属于特定种族 (Subtype)",

    # ---------- 比较运算符 ----------
    "AttackComparisonQuery": "🔵 条件: 攻击力数值判断",
    "BlockMeterValueQuery": "🔵 条件: 格挡值判断",
    "DamageTakenComparisonQuery": "🔵 条件: 已受伤害判断",
    "HealthComparisonQuery": "🔵 条件: 生命值判断 (HealthComparison)",
    "SunCostComparisonQuery": "🔵 条件: 阳光/脑子费用判断",
    "SunCostPlusNComparisonQuery": "🔵 条件: 费用+N 判断",
    "SunCounterComparisonQuery": "🔵 条件: 阳光计数器判断",
    "TurnCountQuery": "🔵 条件: 回合数判断",

    # ---------- 组件类型 ----------
    "HasComponentQuery": "🔵 条件: 拥有组件",
    "LacksComponentQuery": "🔵 条件: 缺少组件",
    "OnTerrainQuery": "🔵 条件: 在地形上",
    "OpenLaneQuery": "🔵 条件: 空行判断",

    # ---------- 预定义快捷方式 ----------
    "HasZombiesComponent": "🔵 条件: 是僵尸",
    "HasPlantsComponent": "🔵 条件: 是植物",
    "HasPlayerComponent": "🔵 条件: 是英雄/玩家 (Player)",
    "HasLaneComponent": "🔵 条件: 是一整行(地段)",
    "HasFaceDownComponent": "🔵 条件: 是暗置/墓碑",
    "HasEnvironmentComponent": "🔵 条件: 是场地牌",
    "HasWaterTerrainComponent": "🔵 条件: 在水生地形",
    "HasHighgroundTerrainComponent": "🔵 条件: 在高地地形",
    "HasUnhealableComponent": "🔵 条件: 不可治疗",
    "HasSuperpowerComponent": "🔵 条件: 是英雄技能 (Superpower)",

    # ==================== Effect 效果 ====================
    # ---------- 无参数 ----------
    "CopyStatsEffect": "🔴 效果: 复制属性",
    "DestroyCardEffect": "🔴 效果: 直接消灭",
    "ExtraAttackEffect": "🔴 效果: 额外攻击",
    "MixedUpGravediggerEffectDescriptor": "🔴 效果: 掘墓人墓碑",
    "MoveCardToLanesEffectDescriptor": "🔴 效果: 移动",
    "ReturnToHandEffect": "🔴 效果: 弹回手牌",
    "SlowEffect": "🔴 效果: 冰冻 (Slow)",
    "TurnIntoGravestoneEffectDescriptor": "🔴 效果: 回到墓碑",

    # ---------- 有参数（基础类型）----------
    "AttackInLaneEffectDescriptor": "🔴 效果: 攻击本行 (AttackInLane)",
    "BuffEffect": "🔴 效果: 属性改变 (Buff/Debuff)",
    "ChargeBlockMeterEffectDescriptor": "🔴 效果: 充能格挡值 (ChargeBlockMeter)",
    "CopyCardEffectDescriptor": "🔴 效果: 复制卡牌 (CopyCard)",
    "CreateCardEffect": "🔴 效果: 召唤特定卡牌 (GUID)",
    "CreateCardInDeckEffect": "🔴 效果: 洗入牌库",
    "DamageEffect": "🔴 效果: 造成伤害",
    "DrawCardEffect": "🔴 效果: 抽牌",
    "EffectValueDescriptor": "🔴 效果: 效果值映射 (EffectValueDescriptor)",
    "GainSunEffect": "🔴 效果: 获得阳光/脑子",
    "GrantAbilityEffect": "🔴 效果: 赋予特殊能力 (关键字)",
    "GrantTriggeredAbilityEffectDescriptor": "🔴 效果: 赋予能力 (GrantTriggeredAbility)",
    "HealEffect": "🔴 效果: 治疗",
    "HeroHealthMultiplier": "🔴 效果: 英雄血量倍率 (HeroHealthMultiplier)",
    "ModifySunCostEffect": "🔴 效果: 修改卡牌花费",
    "SetStatEffect": "🔴 效果: 属性数值强制设定 (SetStat)",
    "SunGainedMultiplier": "🔴 效果: 获得阳光倍率 (SunGainedMultiplier)",
    "TargetAttackMultiplier": "🔴 效果: 攻击力翻倍/倍增",
    "TargetHealthMultiplier": "🔴 效果: 生命值翻倍/倍增",

    # ==================== ComplexEffect 复合效果 ====================
    "DrawCardFromSubsetEffect": "🟥 复合：召唤",
    "CreateCardFromSubsetEffectDescriptor": "🟥 效果: 生成卡牌 (CreateCardFromSubset)",
    "TransformIntoCardFromSubsetEffectDescriptor": "🟥 效果: 变身 (TransformIntoSubset)",

    # ==================== Virtual 虚拟/UI辅助 ====================
    "AdditionalTargetQuery": "📦 额外目标条件",
    "FinderPlaceholder": "🔍 查找范围 (Finder)",
    "QueryPlaceholder": "📋 满足条件 (Query)",

    # ==================== 以下为补充节点（兼容旧版/别名） ====================
    "AbilityGuid": "能力 GUID (常用: 562=双重攻击, 564=先攻, 615=远古吸血, 668=狩猎场)",
    "AbilityValueType": "能力数值类型",
    "AbilityValueAmount": "能力数值",

    # 组件节点补充
    "CompositeQuery": "🔗 复合查询",
    "Query": "🔵 查询条件",
    "Effect": "🔴 效果",
    "Filter": "🟡 过滤器",
    "TargetSelector": "🎯 目标选择器",

    # 效果补充（别名）
    "BuffEffectDescriptor": "🔴 效果: 属性改变",
    "DamageEffectDescriptor": "🔴 效果: 造成伤害",
    "DestroyCardEffectDescriptor": "🔴 效果: 直接消灭",
    "DrawCardEffectDescriptor": "🔴 效果: 抽牌",
    "HealEffectDescriptor": "🔴 效果: 治疗",
    "ExtraAttackEffectDescriptor": "🔴 效果: 额外攻击",
    "ReturnToHandFromPlayEffectDescriptor": "🔴 效果: 弹回手牌",
    "SlowEffectDescriptor": "🔴 效果: 冰冻",
    "GainSunEffectDescriptor": "🔴 效果: 获得阳光",
    "ModifySunCostEffectDescriptor": "🔴 效果: 修改费用",
    "CreateCardInDeckEffectDescriptor": "🔴 效果: 洗入牌库",
    "GrantAbilityEffectDescriptor": "🔴 效果: 赋予能力",
    "CreateCardEffectDescriptor": "🔴 效果: 召唤卡牌",
    "SetStatEffectDescriptor": "🔴 效果: 设置属性",
    "CopyStatsEffectDescriptor": "🔴 效果: 复制属性",

    # 能力类型补充
    "Multishot": "多重射击 (Multishot)",
    "AttacksInAllLanes": "全路攻击 (AttacksInAllLanes)",
    "PlaysFaceDown": "暗置 (PlaysFaceDown)",
    "Aquatic": "水生 (Aquatic)",
    "DoubleStrike": "连击 (DoubleStrike)",
    "AttackOverride": "攻击覆盖 (AttackOverride)",
    "SplashDamage": "溅射伤害 (SplashDamage)",

    # 参数与枚举追加（用于显示）
    "Divider": "倍数/除数",
    "Amount": "数值",
    "ActivationTime": "执行时间",
    "CardGuid": "卡牌 ID (GUID)",
    "AmountToCreate": "生成数量",
    "DeckPosition": "洗入位置",
    "Immediate": "立即执行",
    "NextTurn": "下回合开始",
    "Top": "牌库顶",
    "Bottom": "牌库底",

    # 参数与枚举值
    "GrantableAbilityType": "赋予的能力类型",
    "StripNoncontinousModifiers": "剥离非持续性加成 (清空临时Buff)",
    "StatType": "修改属性类型",
    "AbilityValue": "特殊修正值 (如免疫类型)",
    "ModifyOperation": "修改方式",
    "ForceFaceDown": "以墓碑/潜行方式召唤",

    # 特殊值
    "Permanent": "永久",
    "EndOfTurn": "回合结束",
    "Either": "任意侧",
    "ToTheLeft": "左侧",
    "ToTheRight": "右侧",
    "Self": "自身",
    "Source": "来源",
    "Target": "目标",
}


# ==================== 弹窗参数名翻译 ====================
PARAM_NAMES = {
    # EffectValueDescriptor
    "MappingType": "映射类型",
    "DestToSourceMap": "目标到源映射 (如 HealAmount: DamageAmount)",

    # 基础参数
    "AbilityGroupId": "技能组 ID",
    "SelectionType": "选择目标方式",
    "NumTargets": "目标数量",
    "TargetScopeType": "目标范围筛选",
    "TargetScopeSortValue": "排序参考数值",
    "TargetScopeSortMethod": "排序方法",
    "AdditionalTargetType": "额外目标类型",
    "OnlyApplyEffectsOnAdditionalTargets": "仅对额外目标生效",
    "OriginEntityType": "基准实体",
    "Side": "相邻方向",
    "ComparisonOperator": "比较符号",
    "AttackValue": "攻击力比较值",
    "DamageAmount": "伤害数值",
    "AttackAmount": "攻击力改变(Buff)",
    "HealthAmount": "生命值改变(Buff)",
    "BuffDuration": "持续时间",

    # 补充参数
    "SunCost": "阳光/脑子费用",
    "DrawAmount": "抽牌数量",
    "HealAmount": "治疗量",
    "Divider": "倍数",
    "Amount": "数值",
    "ActivationTime": "激活时机",
    "CardGuid": "卡牌GUID",
    "AmountToCreate": "创建数量",
    "DeckPosition": "牌库位置",
    "GrantableAbilityType": "赋予的能力",
    "AbilityValue": "能力参数",
    "ModifyOperation": "修改操作",
    "Value": "数值",
    "ForceFaceDown": "强制暗置",
    "StatType": "属性类型",
    "StripNoncontinousModifiers": "移除非持续修正",
    "Duration": "持续时间",
    "Subtype": "子类型/种族",

    # QueryEntityCondition
    "ConditionEvaluationType": "满足规则的判定方式",
    "Finder": "查找器/来源",

    # 其他效果参数
    "ChargeAmount": "充能数值",
    "GrantTeamup": "赋予组队能力",
    "CreateInFront": "在身前创建",

    # GrantTriggeredAbilityEffectDescriptor
    "AbilityGuid": "能力 GUID",
    "AbilityValueType": "能力数值类型",
    "AbilityValueAmount": "能力数值",

    # HealthComparisonQuery
    "HealthValue": "生命值比较值",
}


# ==================== 下拉框枚举值翻译 ====================
ENUM_NAMES = {
    # EffectValueDescriptor
    "DamageToHeal": "伤害 → 治疗 (DamageAmount → HealAmount)",
    "HealToDamage": "治疗 → 伤害 (HealAmount → DamageAmount)",

    # PrimaryTargetFilter / SecondaryTargetFilter
    "Manual": "手动选取 (Manual)",
    "Random": "随机选取 (Random)",
    "All": "全部符合条件者 (All)",
    "Sorted": "按条件排序 (Sorted)",
    "None": "无 (None)",
    "Attack": "攻击力 (Attack)",
    "Health": "生命值 (Health)",
    "Lowest": "最低的 (Lowest)",
    "Highest": "最高的 (Highest)",
    "Query": "自定义查询 (Query)",

    # OriginEntityType
    "Self": "自身 (Self)",
    "Source": "来源 (Source)",
    "Target": "目标 (Target)",

    # Side
    "Either": "任意两侧 (Either)",
    "ToTheLeft": "左侧 (ToTheLeft)",
    "ToTheRight": "右侧 (ToTheRight)",

    # ComparisonOperator
    "LessOrEqual": "小于等于 (<=)",
    "Equal": "等于 (==)",
    "GreaterOrEqual": "大于等于 (>=)",

    # BuffDuration / Duration
    "Permanent": "永久 (Permanent)",
    "EndOfTurn": "回合结束时 (EndOfTurn)",

    # ActivationTime
    "Immediate": "立即 (Immediate)",
    "NextTurn": "下回合 (NextTurn)",

    # DeckPosition
    "Top": "牌库顶 (Top)",
    "Bottom": "牌库底 (Bottom)",
    "Random": "随机位置 (Random)",

    # ModifyOperation
    "Add": "增加 (Add)",
    "Set": "设置为 (Set)",

    # GrantableAbilityType
    "Unhurtable": "无敌 (Unhurtable)",
    "Deadly": "致命 (Deadly)",
    "Frenzy": "狂怒 (Frenzy)",
    "Truestrike": "精准打击 (Truestrike)",
    "Strikethrough": "穿透 (Strikethrough)",
    "Afterlife": "来世 (Afterlife)",
    "MinHealth": "最小生命值 (MinHealth)",
    "NoExtraAttacks": "无法额外攻击 (NoExtraAttacks)",
    "GravestoneSpy": "墓碑侦察 (GravestoneSpy)",
    "Teamup": "组队 (Teamup)",
    "Aquatic": "水生 (Aquatic)",
    "CanPlayFighterInSurprisePhase": "奇袭阶段可打出 (CanPlayFighterInSurprisePhase)",
    "Mustache": "胡子 (Mustache)",
    "AttackOverride": "攻击覆盖 (AttackOverride)",
    "MultiplyDamage": "伤害翻倍 (MultiplyDamage)",
    "Graveyard": "墓地 (Graveyard)",
    "Untrickable": "锦囊免疫 (Untrickable)",
    "Unhealable": "不可治疗 (Unhealable)",

    # 其他枚举值
    "BlockMeterValue": "格挡值",
    "DamageTakenValue": "已受伤害值",
    "AdditionalCost": "额外费用",
    "SunCounterValue": "阳光计数器值",
    "TurnCount": "回合数",

    # 阵营选择
    "Plants": "植物阵营",
    "Zombies": "僵尸阵营",
    "PvZCards.Engine.Components.Plants, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null": "植物阵营",
    "PvZCards.Engine.Components.Zombies, EngineLib, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null": "僵尸阵营",

    # 地形类型
    "GrassTerrain": "草地",
    "WaterTerrain": "水域",
    "HighgroundTerrain": "高地",
    "Environment": "场地",
    "FaceDown": "暗置/墓碑",

    # QueryEntityCondition
    "All": "全部满足 (All)",
    "Any": "任意满足 (Any)",

    # GrantTriggeredAbilityEffectDescriptor 的枚举
    "562: 双重攻击 (DoubleStrike)": "562: 双重攻击 (DoubleStrike)",
    "564: 先攻 (FirstStrike)": "564: 先攻 (FirstStrike)",
    "615: 远古吸血僵尸 (AncientVampireZombie)": "615: 远古吸血僵尸 (AncientVampireZombie)",
    "668: 狩猎场 (HuntingGrounds)": "668: 狩猎场 (HuntingGrounds)",
    "0: 自定义 GUID": "0: 自定义 GUID (手动输入)",

    # AbilityValueType
    "None": "无 (None)",
    "Damage": "伤害 (Damage)",
}


# ==================== 辅助函数 ====================
def get_node_name(key, default=None):
    """获取节点/组件的中文显示名称"""
    return NODE_NAMES.get(key, default or key)


def get_param_name(key, default=None):
    """获取参数的中文名称"""
    return PARAM_NAMES.get(key, default or key)


def get_enum_name(key, default=None):
    """获取枚举值的中文名称"""
    return ENUM_NAMES.get(key, default or key)


# ==================== 效果描述模板（供 logic_translator.py 使用）====================
EFFECT_DESCRIPTIONS = {
    "DamageEffect": "造成 {damage} 点伤害",
    "BuffEffect": "{duration}获得攻击力 {attack:+d} / 生命值 {health:+d}",
    "DestroyCardEffect": "直接消灭目标",
    "DrawCardEffect": "抽 {amount} 张牌",
    "HealEffect": "恢复 {amount} 点生命值",
    "ExtraAttackEffect": "获得额外一次攻击机会",
    "TargetAttackMultiplier": "攻击力变为 {divider} 倍",
    "TargetHealthMultiplier": "生命值变为 {divider} 倍",
    "ReturnToHandEffect": "将目标弹回手牌",
    "SlowEffect": "冰冻目标",
    "GainSunEffect": "{when}获得 {amount} 点阳光/脑子",
    "ModifySunCostEffect": "{duration}使卡牌花费改变 {amount}",
    "CreateCardInDeckEffect": "将 {amount} 张卡牌 (ID:{card_id}) 洗入牌库的 {position}",
    "GrantAbilityEffect": "{duration}赋予能力【{ability}】{extra}",
    "CreateCardEffect": "{face_down}召唤卡牌 (ID:{card_id})",
    "SetHeroHealthEffect": "{operation}英雄生命值 {amount} 点",
    "CopyStatsEffect": "复制目标的属性数值",
}