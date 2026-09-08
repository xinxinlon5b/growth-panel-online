# 学习总结：AI agent evaluation

- **时间**：2026-09-03 20:11
- **来源**：GitHub 关键词搜索（自动采集）

## 学到的高价值项目

1. **mlflow/mlflow** → [学习] mlflow_mlflow.md
2. **promptfoo/promptfoo** → [学习] promptfoo_promptfoo.md
3. **google/adk-python** → [学习] google_adk-python.md
4. **Tencent/WeKnora** → [学习] Tencent_WeKnora.md
5. **raga-ai-hub/RagaAI-Catalyst** → [学习] raga-ai-hub_RagaAI-Catalyst.md

## 一句话结论（队长补 20:11）

这批项目回答的问题是：**AI 应用上线后怎么知道它好不好、怎么持续保证它好**——正是用户需求里"审计/评测"缺的那块。

1. **promptfoo / RagaAI-Catalyst** → 评测工具：给 prompt/agent/RAG 建测试集，自动化回归（promptfoo 还能做红队/漏洞扫描）。对应 09 关卡地图的"评测关"——**上线前必须有评测集，不是靠感觉**。
2. **mlflow** → ML/LLM 生命周期管理：实验追踪/模型注册/版本回滚。对应"模型版本与回滚"卡——**每次推理能定位到模型版本，出问题能回滚**。
3. **google/adk-python** → Agent 开发框架（Google 官方）。对应 12-Factor-Agents 的"小而专注"——框架给你编排底座，但 prompt/上下文/控制流要自己拥有。
4. **Tencent/WeKnora** → 腾讯 RAG 知识库框架。对应"RAG 质量评估"——知识库不是搭完就行，要测召回/忠实度。

**共性启示**：成熟项目都强调"AI 要像软件一样被工程化管理"——测试集、版本、可观测、回滚，缺一不可。这正是"企业 AI 落地 vs 玩具 demo"的分水岭。
