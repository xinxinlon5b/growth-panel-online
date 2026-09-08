# dsh 任务书 · 架构决策材料清单（2026-09-02）

> 任务来源: Hermes agent (队长, M3)  
> 派发时间: 2026-09-02 11:55  
> 强制模型: minimax/MiniMax-M3  
> 交付期限: 30 分钟内

## 任务目标

梳理「架构决策框架」这个子领域的**完整材料清单**——不是写方法论卡，是**先把材料找齐**。

输出两份：
1. `AR-001-架构决策框架.md` — 提炼自外部权威（AWS Well-Architected + calmrocks notebook + ADR 模式）
2. `AR-002-你的3项目实战映射.md` — 把阿尔泰/NIFTY/中俄轻舟 3 个项目映射到架构决策框架的对应点上

## 输入材料（你必须读完/扫完的）

### 必读
1. **AWS Well-Architected Framework**（5 大支柱：卓越运营/安全/可靠性/性能效率/成本优化）
   - https://aws.amazon.com/cn/architecture/well-architected/
2. **ADR (Architecture Decision Records) 模式**（Michael Nygard 原文）
3. **calmrocks/ai-engineer-notebooks**（FDE 实战 notebook，关注 00-09 章节的「架构决策」部分）
   - https://github.com/calmrocks/ai-engineer-notebooks
4. **NIRDiamant/RAG_Techniques**（RAG 架构模式）
   - https://github.com/NIRDiamant/RAG_Techniques

### 用户项目材料（必须用 read_file 读这些本地路径）
1. `~/bag_ai_studio/server.py`（NIFTY 后端，~3500 行）
2. `~/bag_ai_studio/templates/index.html`（NIFTY 前端）
3. `~/Documents/Obsidian Vault/VK获客/🏗️基础设施/` 下阿尔泰项目的配置文件（install.sh / docker-compose.yml 等）
4. `~/Documents/Obsidian Vault/🏗️AI记忆库/中俄轻舟/` 下的项目说明

### 必填结构

#### AR-001（外部权威）

```markdown
# AR-001 · 架构决策框架

> ID: AR-001 | 创建: 2026-09-02 | 状态: ⭐ 正式

## 这个子领域在解决什么问题
新项目第一周应该按什么顺序做什么决策，避免「想到哪做到哪」。

## 核心问题清单（5-10 个）
1. 业务目标决定什么架构模式？（SaaS vs 工具 vs 嵌入式）
2. 模型选择怎么选（自有模型 vs API vs 本地）
3. ...

## 标杆答案（每个都要标引来源）

### AWS Well-Architected 5 大支柱
- 卓越运营：...（标引: aws.amazon.com/cn/architecture/well-architected/）
- 安全：...
- 可靠性：...
- 性能效率：...
- 成本优化：...

### ADR 模式
- 4 段式（上下文/决策/后果/替代方案）
- 何时记录决策
- 如何回溯

### RAG 架构模式（来自 RAG_Techniques）
- Naive RAG / Advanced RAG / Modular RAG 的取舍

### AI 系统部署模式（来自 calmrocks notebook）
- prompt → RAG → evaluation → agent → adaptation → serving
```

#### AR-002（实战映射）

```markdown
# AR-002 · 你的3项目实战映射

> ID: AR-002 | 创建: 2026-09-02 | 状态: ⭐ 正式

## 这个子领域在解决什么问题
拿我们做过的真实项目，回答「当时为什么选这个架构」——给未来新客户做参考。

## 阿尔泰（中俄跨境电商获客）
- 业务场景：跨境电商找俄罗斯客户
- 核心架构决策：6 平台并行 + 多账号隔离 + 触达闸门
- AWS 5 支柱对应：...
- ADR 记录（事后补）：...
- 当时没做对的：单平台个人号私信（VK 封号教训）

## NIFTY（本地化 AI 商品图）
- 业务场景：电商小白想做商品图
- 核心架构决策：本地 Python 服务 + LibTV 包月 + 火山按量双通道
- AWS 5 支柱对应：...
- ADR 记录：...
- 当时没做对的：单文件 server.py 3500 行（架构债）

## 中俄轻舟（跨境电商卖家向）
- 业务场景：...
- ...

## 共性教训（3 个项目共同的踩坑）
- 共性 1：都先做对再做好，导致 1.0 交付慢
- 共性 2：...
- 共性 3：...

## 与其他子领域的关系
- 依赖: FDE-001（架构决策是 FDE 的核心动作）
- 顺序: 在 FDE 旅程第 2 阶段「激活部署」前
- 替代: 无
```

## 产出要求

1. 文件路径：
   - `/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/foundations/AR/AR-001-架构决策框架.md`
   - `/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/foundations/AR/AR-002-你的3项目实战映射.md`
2. 字数: 每张 ≥ 2000 字
3. 必须读本地项目文件（不只是猜）
4. 必须包含 ADR 实战示例（哪怕是事后补的）

## 验收标准

回复（中文）：
1. ✅/❌ 文件是否落地
2. 读了几个本地项目文件
3. AR-002 里 3 个项目每个有 ≥3 个架构决策记录
4. ADR 模板示例是否完整

## 队长备注

你的强项是工程深度 + 代码实证。这是「材料清单」型任务，需要你看代码、看文件、提炼框架。  
不要假设，直接 read_file 看代码。  
时间 30 分钟。

— Hermes (M3 队长)