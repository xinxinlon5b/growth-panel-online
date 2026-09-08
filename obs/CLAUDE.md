# 方法论库 · 交接手册（CLAUDE.md）

> 创建: 2026-09-02 v3.0 锁版 | 给后接手者

## 这是什么

这是「企业 AI 落地全图」方法论库，**给后接手者看的完整地图**。

**不是**给客户看的产品文档，**是**给接手者看的内部沉淀。

## 一句话定位

> 7 张决策卡（**能直接拿出去跟客户谈**）+ 15 张方法论卡（**给客户做架构/合规/可靠性参考**）+ 黄金集 100% 覆盖（**真能跑**的评测机制）+ 主动学习引擎（**飞轮自转**不依赖我）。

## 目录结构

```
~/Documents/Obsidian Vault/🏗️AI记忆库/方法论/   # 真实路径（勿用 ~/methodology/，不存在）
├── README.md                    # 索引（最重要，先进这个看全局）
├── cards/                       # 决策卡（能直接给客户，正式）
│   ├── index.json              # 机器可读索引（agent 用这个）
│   ├── ALT-001-中俄跨境电商获客.md
│   ├── NIF-001-本地化AI商品图工作室.md
│   ├── STARTER-001-启航包档决策卡.md
│   ├── AR-003-顾问式AI架构决策.md
│   ├── ENTERPRISE-001-近企业档决策卡.md
│   ├── MIGRATE-001-Coze迁移本地化决策卡.md
│   └── RESULT-001-按结果付费决策卡.md
│   └── candidates/             # 飞轮候选（decision-card-miner 起草, 待人工 ★）
├── foundations/                 # 方法论卡（架构/合规/可靠性等, 正式）
│   ├── FDE/  · 角色 + 六阶段 + 试点先行
│   ├── AR/   · 架构 + 实战 + 顾问
│   ├── POC/ · CJ/ · REL/ · EVAL/ · COMP/ · CRISIS/ · ECO/ · PRICE/ · SALES/ · ORG/
├── 候选池/                      # 待审核内容（[候选]/[学习] 前缀, 人工在工作台把关）
├── 学习池/                      # 学别人的经验（raw/ 原文 + 提炼 md）
│   └── raw/                    # 采集原文层（原始素材, 沉淀链条源头）
├── 复盘区/                      # 我们的实战复盘（经验/反模式）
│   ├── 审核报告/               # 三审通过报告（正式审计留档）
│   └── 已驳回_主题错位/         # 主题错位归档（不污染主线）
├── 成长系统/                    # 规划/决策文档（00 目标基线 → 12 术语词典, **09 是知识枢纽入口**）
├── 方案库/                      # 自由拼装/场景向导保存的组合方案
├── 项目库/                      # 客户项目挂靠（可空）
├── 黄金集/                      # 评测机制（golden-v0.1…v1.1 + eval.py）
├── assignments/                 # 交付任务/作业
├── raw/  reports/               # ⚠️ 空目录（历史 scaffold, 待清理或标注）
```

## 运维须知

- **工作台 8895 由 launchd 守护**（com.hermes.growth-panel，KeepAlive 自愈）——不要手动 `python3 server.py` 起（会和 launchd 抢端口）。改代码后重启：`launchctl kickstart -k gui/$(id -u)/com.hermes.growth-panel`
- 日志：/tmp/growth-panel.log（stdout）+ /tmp/growth-panel.err.log（stderr）

## 3 个最重要的入口

### 1. **README.md**
- 看完整地图（14 子领域 + 5 核心 + 7 决策卡）
- 看飞轮进度（什么时候 ★ 了多少张卡）
- 看 v3.0 → v4.0 路线

### 2. **cards/index.json**
- 机器可读索引
- agent 接到客户咨询时**自动加载这个**（不是 markdown）
- 含 tags 字段（精确匹配，不误中）

### 3. **黄金集/eval.py**
- `python3 "$HOME/Documents/Obsidian Vault/🏗️AI记忆库/方法论/黄金集/eval.py"`
- 真跑评测，告诉你覆盖率多少
- 改完卡 → 跑这个 → 看命中率变化

## 4 个使用场景（接手者怎么用）

### 场景 A：客户咨询来了
```
1. 读 cards/index.json（agent 自动加载）
2. 用 tag 匹配客户咨询
3. 命中 → 读对应卡 + 给客户方案
4. 未命中 → 标「需补卡」（不强推）
```

### 场景 B：飞轮跑通（每 1-2 周）
```
1. 看 "$HOME/Documents/Obsidian Vault/🏗️AI记忆库/方法论/cards/candidates/" 有几张候选
2. ★ 觉得好的（移到 cards/ + 更新 index.json）
3. 跑 eval.py 看命中率
4. push companion.html 更新（cd altai-page && git push）
```

### 场景 C：客户实战反馈
```
1. 客户用了某张卡，遇到问题
2. 写到「我们的实战」段（每个卡都有这个段）
3. 加反模式或教训（让卡越来越准）
4. 同步更新到网页（companion.html 数据驱动）
```

### 场景 D：v4.0 升级
```
1. 看黄金集 v1.1 → 哪些场景半命中
2. 写新决策卡覆盖
3. 加决策卡到 index.json
4. 跑 eval.py 看覆盖率
5. 更新 companion.html + architect-helper.html
```

## 5 条铁律（不要违反）

### 铁律 1：**公开页只放脱敏结论**
- companion.html / architect-helper.html 都公开
- 不放客户真实数据 / Token / 微信 ID / 本机路径

### 铁律 2：**候选永远不是正式**
- candidates/ 里的卡必须人工 ★ 才入正式库
- 不自动 push 网页

### 铁律 3：**黄金集是唯一真理**
- 不靠感觉判断卡好不好
- 改完跑 eval.py，分数说话

### 铁律 4：**M3 牛马，K3 禁按量**
- 用户明确偏好（2026-08-31 / 09-01 两次纠正）
- 所有任务用 MiniMax-M3
- K3 只在用户点名时用

### 铁律 5：**每周复盘飞轮**
- cron job 跑不跑（每周一 03:00）
- 候选 ★率多少
- 黄金集命中率趋势
- Obsidian 备份是否成功（Baidu 网盘）

## 关键决策记录

### v3.0 锁版决定
- **黄金集 100% 命中**（19/19）
- **7 张决策卡**能直接给客户谈
- **15 张方法论卡**提供架构支持
- **decision-card-miner 飞轮自转**启动

### 历程（仅记录决策点）

| 版本 | 日期 | 关键决策 |
|---|---|---|
| v1.0 | 09-02 上午 | 8 张方法论卡骨架 + 网页上线 |
| v1.1 | 09-02 中午 | + 3 张决策卡（启航包/NIF/顾问） |
| v1.2 | 09-02 下午 | + ENTERPRISE-001（覆盖近企业档） |
| v2.0 | 09-02 傍晚 | + 7 张周边方法论卡 + 飞轮 skill + cron + 架构师助手网页 |
| v3.0 | 09-02 晚 | + MIGRATE-001 + RESULT-001 + 黄金集 100% |

## 失败教训（**别再踩**）

### 教训 1：eval.py 早期版本太宽容
- 早期给方法论卡命中 0.5 分 → 高覆盖率假象
- v3.0 改正确规则：方法论卡命中 = 1 分（在 cards 库里就 1 分）
- **结论**：不要让评测脚本掩盖问题

### 教训 2：patch 误删代码
- companion.html 多次 patch 把 renderStats IIFE 删了
- 飞轮条不显示但 flywheel 数据存在
- **教训**：改 script 块后**必须浏览器实测**，不能只看 fetch 的 HTML

### 教训 3：snapshop 显示 JS 文字误判
- browser_navigate snapshot 显示「StaticText < ...function renderStats()...」
- 实际是 snapshot 工具的 bug，不是页面 bug
- **教训**：用 fetch + Function 解析真验证 JS 执行

### 教训 4：Docker 缓存陷阱（不是本项目，是其他项目）
- templates/index.html 改完不重启 → 服务返回旧版
- 本方法论库是 markdown，没这问题
- 但网页部分（companion.html）改完要刷新 CDN（GitHub Pages 有缓存）

## 7 张决策卡快速对照

| 卡 | 一句话定位 | 价格 |
|---|---|---|
| STARTER-001 | 个人/小团队首单 | ¥3-8k |
| ALT-001 | 跨境电商/物流找俄客户 | ¥3-80k |
| NIF-001 | 电商 AI 出图本地化 | ¥3-8k |
| AR-003 | 传统企业零基础顾问 | ¥3-100k+ |
| ENTERPRISE-001 | 大企业多平台审计 | ¥80-300k+ |
| MIGRATE-001 | Coze/Dify 迁移 | ¥15-50k |
| RESULT-001 | 按结果付费 | ¥5-80k 封顶 |

## 外部资源（GitHub 标杆）

- **obra/superpowers**（280k★）— skill 框架
- **llm-wiki-agent**（3.5k★）— 知识库自维护
- **plurai-ai/intellagent**（1.3k★）— agent 评测
- **xdash/FDE-Guidance-Book**（4.5k★）— FDE 中文完整指南
- **pierpaolo28/Awesome-FDE-Roadmap**（1k★）— FDE 角色技能图
- **calmrocks/ai-engineer-notebooks**（0.6k★）— FDE 实战技能
- **alexeygrigorev/ai-engineering-field-guide**（5.4k★）— 6964 招聘数据
- **product-on-purpose/pm-skills**（0.6k★）— 68 个 PM skill 模板

## 不该做的事（红线）

❌ **不要**强推客户买最贵的卡（启航包 / 工作站 / 近企业客户自己选）
❌ **不要**在公开网页放客户真实数据 / Token
❌ **不要**用 Kimi K3 按量付费（用户明确禁）
❌ **不要**没 ★ 候选就入正式库（飞轮纪律）
❌ **不要**改完卡不跑 eval.py（不知道效果变了多少）
❌ **不要**不写反模式就入卡（卡就废了）

## 该做的事（推荐）

✅ **每天**：跑一遍 eval.py（10 秒）
✅ **每周**：看 candidates/ ★ 候选（5 分钟）
✅ **每月**：复盘黄金集命中率（30 分钟）
✅ **每季**：重读 5 张核心决策卡（看实战反馈是否要改）
✅ **每半年**：跑一次主动学习（看 GitHub 新趋势）

## 联系方式（如果接手者需要问问题）

- **Obsidian 路径**：`~/Documents/Obsidian Vault/🏗️AI记忆库/方法论/`
- **Obsidian 全文搜索**：M3 牛马会用 grep / search_files
- **Hermes agent 加载**：~/.hermes/skills/ai-architect/SKILL.md + decision-card-miner/SKILL.md
- **公开网页**：https://xinxinlon5b.github.io/altai-page/companion.html

## 最后一句话

**这不只是文档，是一个活的系统**。

飞轮每跑一次，方法论就厚一点。客户每签一单，决策卡就更准。**别让它停止转动**。

## 变更日志
- **2026-09-02 v3.0**: 首版交接手册