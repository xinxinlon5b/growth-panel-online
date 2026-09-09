# 知识库 Agent 工具链速查

> 创建: 2026-09-09 | 配套: 成长系统/31_知识库分类与Agent协作架构_v1.md
> 工具都在 `~/.hermes/scripts/growth_kb/`

## 四件套用法

| 场景 | 命令 |
|---|---|
| 🔑 来新项目/客户（**每次必跑**） | `python3 ~/.hermes/scripts/growth_kb/retrieve_for_project.py --text "<用户画像/大白话>"`<br>加 `--json` 输出结构化给程序 |
| 📥 复盘完回流（给卡 evidence +1） | `python3 ~/.hermes/scripts/growth_kb/bump_evidence.py --review "复盘区/xxx.md"` |
| 🧪 改了卡/关键词后回归 | `python3 ~/.hermes/scripts/growth_kb/eval_retrieval.py`（召回率 ≥0.7 才 PASS） |
| 🏷️ 新卡入库后补 frontmatter | `python3 ~/.hermes/scripts/growth_kb/add_frontmatter.py`（dry-run 预览）→ 确认后 `--apply` |

## 关键设计

- **检索**：读卡 frontmatter 的 `triggers`（触发词）匹配画像 → 命中决策卡 + 关联方法论卡（按域关键词）+ 老项目/复盘 evidence（只认 项目库/复盘区/方案库 = 真实战，过滤黄金集等评测文件）
- **口语扩展**：`SYN` 词典把用户大白话映射到卡 tags（"小单"→试水、"几千块"→低预算、"图片"→商品图…），评估集 12 条真实画像召回率 **1.00**
- **评测集**：`retrieval_cases.json` 12 条（10 期望命中 + 2 期望诚实拒绝）
- **回流**：复盘提到卡 ID（如 ALT-001）→ bump_evidence 自动把复盘路径加进卡 frontmatter `evidence`（幂等，重复跳过）
- **frontmatter schema**：type/domain/tags/triggers/status/updated/source_file/evidence

## 维护注意

- 新决策卡要写 `triggers`（口语触发词），不写就匹配不到
- 用户说话方式变了匹配不到 → 往 SYN 加映射 + 往 retrieval_cases.json 加一条 → 跑 eval 验证
- 网页渲染已支持剥 YAML frontmatter（mdToHtml 顶部 --- 剥离），Obsidian 文档可以直接在网页看
