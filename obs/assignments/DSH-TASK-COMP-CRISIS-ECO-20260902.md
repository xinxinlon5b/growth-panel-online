# dsh 任务书 · 3 张周边方法论卡（2026-09-02 v2.0）

> 强制模型: minimax/MiniMax-M3

## 任务：3 张偏工程的方法论卡

### 1. COMP-001 合规与法律 → `~/methodology/foundations/COMP/COMP-001合规与法律.md`
必须包含：
- 一句话：跨境 AI 项目合规风险的"必须知道"清单
- 5-10 个核心问题清单（数据出域 / 隐私 / 行业监管 / 开源协议 / 出口管制）
- 标杆答案（来源标引）：
  - GDPR / 中国《个人信息保护法》/ 俄罗斯 152-FZ
  - VK/TikTok API 合规政策（已有 messaging-send-safety）
  - 阿尔泰跨境电商 VK 教训（个人号私信被封）
  - GitHub awesome-selfhosted 合规清单
- 我们的实战（必填）：
  - 阿尔泰：VK 合规触达上限（账号矩阵）
  - NIFTY：本地部署 = 数据不出本机 = 默认合规
  - 中俄轻舟：Ozon 卖家 API 合规（店铺主体+税务）
- 7 个反模式（违规收集数据/绕过风控/未签隐私协议等）
- 5 个验收问题

### 2. CRISIS-001 危机管理 → `~/methodology/foundations/CRISIS/CRISIS-001危机管理.md`
必须包含：
- 一句话：客户最怕的 4 类危机，AI 项目应对清单
- 5-10 个核心问题清单（账号封禁 / 模型失效 / 数据泄露 / 客户扯皮）
- 标杆答案：
  - messaging-send-safety skill references/account-ban-investigation.md
  - AWS 危机管理（IR plan）
  - Google SRE Book 第 11 章「Being On-Call」
- 我们的实战（必填）：
  - 阿尔泰：VK 个人号 → 社区号迁移（账号封禁教训）
  - NIFTY：双重扣减 bug 修复（程序稳定性教训）
  - 中俄轻舟：Ozon API 限流应对
- 7 个反模式（事后才补监控 / 单一账号全押 / 没有撤退计划等）
- 5 个验收问题

### 3. ECO-001 生态与工具 → `~/methodology/foundations/ECO/ECO-001生态与工具.md`
必须包含：
- 一句话：AI 项目用什么模型/框架/部署/监控，怎么选
- 5-10 个核心问题清单
- 标杆答案：
  - 模型：MiniMax M3 包月 vs DeepSeek 按量 vs Kimi K3（用户明确偏好 M3 牛马 + K3 禁按量）
  - 框架：LangChain / LlamaIndex / AutoGen / CrewAI
  - 部署：launchd / docker / k8s（macOS 客户机推荐 launchd）
  - 监控：Hermes cron + watchdog + Baidu 网盘备份
- 我们的实战（必填）：
  - 阿尔泰：DeepSeek 队长 + M3 牛马 + K3 禁按量
  - NIFTY：launchd 自愈 + watchdog + snapshot
  - 中俄轻舟：Ozon Seller API + 1688 一件代发
- 7 个反模式（盲目追新模型 / 强依赖云端 SaaS / 单一监控指标等）
- 5 个验收问题

## 验收
回复（中文）：3 张卡字数 + 每张「我们的实战」段字数 + 来源数