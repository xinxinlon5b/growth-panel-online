# 候选决策卡 · 企业AI Agent 安全观测（uber/ADR）

> ID: CAND-2026-09-03-002
> 状态: ⏳ 候选（未经人工 ★，不允许入正式库）
> 起草: 2026-09-03 by decision-card-miner 飞轮首跑（路径修正后实测）
> 标签: 企业安全 / agent 运维 / 审计
> 推荐度: 🟡 观察（高相关，需人工验证）

## 信号来源
- GitHub 仓库: `uber/ADR`（★1527, 2026-09-02 更新）
- 描述: ADR secures enterprise AI agents through observability, security benchmarks and safety guardrails

## 为什么值得关注
与你「目的1：理解企业AI落地全流程」中的 **运维与可靠性/危机管理** 子领域直接对应。企业客户上 AI agent 后最怕的不是模型不好，是「agent 行为失控 / 数据泄露 / 无法审计」——uber 开源的这套观测+安全基准，正好是给客户做企业级交付时能直接引用的安全层参考。

## 证据链（≥3 条要求）
1. GitHub 仓库本体（uber/ADR，★1527，2026-09-02 更新）——企业级背书（Uber 出品）
2. 你已有的实战：EAC 项目的身份边界（guest/staff/owner 保密级过滤）+ 审计事件链，正是「agent 安全观测」的本地实现（~/Documents/Codex/2026-08-17/wa/work/enterprise-ai-companion）
3. 方法论库 CRISIS-001 危机管理 + REL-001 可靠性（foundations/CRISIS/、foundations/REL/）——本卡若 ★ 通过应补充这两块的证据来源

## 反模式（不适用场景）
- 个人/小团队低价项目（启航包档）不需要企业级安全观测 → 杀鸡用牛刀
- 客户无运维能力时纯堆安全工具 → 变成摆设，必须配自愈/看板

## 下一步（等人工 ★）
- [ ] 你花 10 分钟看仓库，决定 ★（进正式库）还是 ✗（拒绝）
- [ ] 若 ★：扩展成正式卡（Enterprise 档），进 cards/ 并更新 index.json，跑黄金集 eval.py