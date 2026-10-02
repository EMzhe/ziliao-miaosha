# ziliao-miaosha 资料分析秒杀技能

公务员考试行测**资料分析秒杀**技能（WorkBuddy Agent Skill），基于公考瞪哥《资料分析36绝技》体系，融合各大机构名师速算方法论。

## 核心特性

- **双引擎**：江湖派秒杀路径（考场人脑思维）+ 学院派精确计算（Python 验证兜底），正确率与速度兼顾
- **36绝技全覆盖**：速算技巧 → 基期量 → 基期和差 → 现期量 → 增长率 → 增长量 → 现期比例 → 基期比例 → 两期比例 → 综合分析
- **题型路由表**：16 类题型 → 绝技编号一键映射
- **名师技巧融合**：花生十三（415份数法、假设分配、差分法）、齐麟/李委明（截位直除、错位修正）、粉笔（化除为乘）、华图（特征数字法）、中公（十字交叉、间隔倍数）
- **科学蒙题**：5 套正确率导向的蒙题决策法 + 7 类选项陷阱全录
- **自进化机制**：新坑自动登记陷阱库，更快解法沉淀进化日志，可持续投喂资料迭代

## 目录结构

```
ziliao-miaosha/
├── SKILL.md                        # 技能入口：题型路由表 + 解题流程 + 输出规范
├── references/
│   ├── 36绝技完整手册.md            # 全部绝技操作步骤 + 真题示范
│   ├── 速查表.md                    # 百化分表、幂次方表、特殊数字
│   ├── 蒙题与选项陷阱.md            # 科学蒙题 + 选项陷阱全录
│   └── 进化日志.md                  # 版本记录与新技巧沉淀
└── scripts/
    └── calc_verify.py              # 精确计算验证器（14 种模式）
```

## 使用方法

### WorkBuddy 用户

1. 将本仓库克隆/复制到 `~/.workbuddy/skills/ziliao-miaosha/`
2. 对话中直接提供资料分析题目（材料+问题+选项）即可自动触发

### 计算验证器独立使用

```bash
python scripts/calc_verify.py --mode base --cur 5631.6 --rate 0.078        # 基期量
python scripts/calc_verify.py --mode growth-amt --cur 1057 --rate 0.053   # 增长量
python scripts/calc_verify.py --mode interval --r1 0.15 --r2 0.08         # 间隔增长率
python scripts/calc_verify.py --mode mix --a 4.6 --wa 454.7 --b 3.6 --wb 848  # 混合增长率
python scripts/calc_verify.py --mode avg-rate --a 0.695 --b 0.252         # 平均数增长率
python scripts/calc_verify.py --mode expr --expr "609.0*1.122/1.161"      # 任意算式
```

支持 14 种模式：`base` `growth-amt` `growth-amt2` `rate` `rate2` `interval` `mix` `avg` `avg-amt` `proportion` `prop-change` `avg-rate` `base-prop` `expr`

## 输出格式

每道题输出三件套：

```
【答案】X（选项数值）
【秒杀路径】题型 + 绝技 + 考场思维步骤
【详解验证】完整算式 + 精确值 + 秒杀结论核对
```

## 版本

- v1.0.0（2026-10-02）：初始版本，36绝技全体系 + 名师融合 + 双引擎验证

## 声明

本技能基于公考瞪哥《资料分析36绝技》付费课程资料整理，仅供个人学习使用，请勿公开传播。
