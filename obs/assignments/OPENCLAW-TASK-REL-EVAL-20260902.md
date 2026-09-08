# OpenClaw 任务书 · REL-001 + EVAL-001（2026-09-02 v1.0 收尾）

> 强制模型: minimax/MiniMax-M3

## 任务

写 2 张方法论卡：

### REL-001 可靠性与自愈
路径: `~/methodology/foundations/REL/REL-001-可靠性与自愈.md`

必须包含：
- 一句话解决什么问题
- 5-10 个核心问题清单
- 标杆答案（来源标引）：
  - AWS Well-Architected「可靠性支柱」
  - NIFTY 项目 launchd 自愈实战
  - messaging-send-safety skill references/account-ban-investigation.md
  - 阿尔泰项目 watchdog + 自愈
- **我们的实战** 段落（必填）：
  - NIFTY: launchd + watchdog + snapshot.py + BAG_AI_BASE 隔离测试
  - 阿尔泰: 多平台冗余 + 触达闸门 + 自我修复
  - 中俄轻舟: 卖家 API 限流 + 失败重试 + 手动兜底
- 7 个反模式（不留详细监控、依赖单点、忽略降级路径、过度乐观SLA等）
- 5 个验收问题

### EVAL-001 效果评估
路径: `~/methodology/foundations/EVAL/EVAL-001-效果评估.md`

必须包含：
- 一句话：怎么判断 AI 项目「真的有用」而不是「看着像有用」
- 核心问题清单（5-10 个）
- 标杆答案：
  - intellagent 评测框架
  - NIFTY 回归测试 103 项
  - golden-v0.2.md 黄金集评测机制
  - obsidian 中俄轻舟项目作战室的「项目全景与决策记录」
- **我们的实战** 段落（必填）：
  - NIFTY: 103 项回归测试 + 真烧积分验收
  - 阿尔泰: 每日筛查报告 + 触达率/账号健康指标
  - 中俄轻舟: Ozon 选品命中率 + Listing 转化率
- 反模式（只看 demo 通过、不量化、用户说好用就行等）
- 5 个验收问题

## 验收

回复（中文）：两张卡字数 + 每张「我们的实战」段字数