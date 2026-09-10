#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_atlas.py — 从 Obsidian 方法论库「真实抽取」生成交互式全景脑图 atlas.html
不手写死数据: 所有节点标题/SOP/方法/卡片 都从库文件解析。
用法: python3 build_atlas.py [> atlas.html]
"""
import os, re, json, io

VAULT = os.path.expanduser("~/Documents/Obsidian Vault/🏗️AI记忆库/方法论")
OUT = os.path.expanduser("~/growth-system-panel/atlas.html")


def read(p):
    fp = os.path.join(VAULT, p)
    if not os.path.exists(fp):
        return ""
    return open(fp, encoding="utf-8", errors="replace").read()


def heads(t, levels=(2, 3), pat=None):
    out = []
    for m in re.finditer(r'^(#{1,6})\s*([^\n]+)$', t, re.M):
        lv = len(m.group(1))
        if lv in levels:
            s = m.group(2).strip()
            if pat and not re.search(pat, s):
                continue
            out.append(s)
    return out


def after_heading(t, head, maxlen=200):
    """取某标题行之后的头两行实质内容作为摘要(点节点时直接可读)"""
    i = t.find(head)
    if i < 0:
        return ""
    lines = t[i + len(head):].split("\n")[1:]
    buf = []
    for ln in lines:
        s = ln.strip()
        if not s:
            if buf:
                break
            continue
        if s.startswith("#"):
            break
        s = re.sub(r'^\s*[-*+>]\s*', '', s)
        s = re.sub(r'^\s*\d+\.\s*', '', s)
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        s = re.sub(r'\*\*|`|\*', '', s)
        if s.startswith("|"):
            continue
        buf.append(s)
        if sum(len(x) for x in buf) >= maxlen:
            break
    return " ".join(buf)[:maxlen]


def first_para_after(t, heading_sub):
    """取某标题后第一段非空文本(作一句话说明)"""
    i = t.find(heading_sub)
    if i < 0:
        return ""
    seg = t[i + len(heading_sub):]
    for ln in seg.split("\n")[1:]:
        s = ln.strip()
        if s and not s.startswith(("#", "|", ">", "```", "-", "*")) and len(s) > 8:
            return re.sub(r'\*\*|`', '', s)[:120]
    return ""


# ─────────────── A. 落地主轴 7 阶段 ───────────────
STAGES = [
    ("阶段 1", "接客户 / 需求澄清", "Discover",
     "先杀错误问题：PSF 三关（痛点/经济性/可行性）；把「想上 AI」翻译成具体的人+事",
     "Discover + 需求门 G1（价值假设可证伪、KPI 可量化、客户签字）",
     "OpenAI「solve a specific problem」· MIT 95% 失败率 · TOGAF ADM",
     ["38 SOP-1 PSF三关", "REQ-001 需求工程", "39 方法1.6 反AI幻觉清单", "requirement-clarifier"]),
    ("阶段 2", "技术选型 / 方案设计", "Design+Architect",
     "定载体与档位：本地/云/混合；按客户成熟度选档（启航包→工作站→近企业）",
     "Design + Architect：方案门 G2（ADR+C4图）· 载体门 G3（决策树+合规预审）",
     "三云厂 Well-Architected · TOGAF B/C/D · Gartner 5 级成熟度",
     ["25 阶段2-3", "23 交付载体怎么选", "ECO-001 生态与工具", "决策卡 7 张", "AR-001 架构决策框架"]),
    ("阶段 3", "MVP / 试点", "Data+Eval+Build+Test",
     "用周级节奏在客户真环境证明价值（MVD）；不做「概念验证坟墓」",
     "Data+Eval+Build+Test：数据门 G4（PII 脱敏）· 评测门 G5（≥5 维度+基线）",
     "OpenAI「deliver early value」· PMBOK 评估 · ISO 42001 · 12-Factor",
     ["38 SOP-2 MVD", "POC-001 POC与MVP验证", "EVAL-001 效果评估", "EVAL-004 评测集与偏见审计", "39 方法1.2 驻场轻量交付五步"]),
    ("阶段 4", "交付部署 / 上线", "Deploy+Accept",
     "企业集成 + 受控试用 → 全面上线；客户团队真的用起来才算完",
     "Deploy + Accept：发布策略（G7 上线门 4 票）· 验收门 G8（UAT+文档+资产移交）",
     "三云厂发布策略 · ISO 审计 · Anthropic「codify patterns」",
     ["25 阶段8-9", "REL-001 可靠性与自愈", "38 SOP-5 热修复文化", "14 装机手册"]),
    ("阶段 5", "质量保障 / 持续稳定", "Operate",
     "持续可见指标 = 续约的筹码（NDR）；出问题按小时计修复",
     "Operate：运营卓越 · 监控告警 · 门禁复核",
     "Palantir NDR 139% · 三云厂运营卓越 · Gartner AI TRiSM",
     ["25 阶段10", "CRISIS-001 危机管理", "34 轨C TRiSM 五支柱", "SALES-002 获客实战手册"]),
    ("阶段 6", "运营 / 续约 / 客户成功", "Iterate",
     "用双段 ROI 证明价值 → 续约 → 横扩 BU/场景（把生意做大）",
     "Iterate：模型漂移监控 · 再训练 · 持续改进（ISO Clause 10）",
     "McKinsey 双段 ROI · ISO Clause 10 持续改进 · ML Lens 漂移监控",
     ["MLOPS-001 模型运维与漂移监控", "ITER-001 反馈闭环", "RESULT-001 按结果付费", "38 SOP-7 灯塔筛选"]),
    ("阶段 7", "复盘沉淀 / 规模化", "Retire+Loop",
     "经验资产化：一个打法服务 N 客户（从 1 到 N 的飞轮）",
     "Retire（G9 退役门：数据/模型/凭据清理+合规证明）+ 现场反馈环反哺平台",
     "Anthropic「team can own」· TOGAF H 变更管理 · ISO 模型退役",
     ["38 SOP-8 经验资产化", "RETIRE-001 退役合规清单", "复盘区 28+ 篇", "41 方法论三件套"]),
]


def build_tree():
    t38 = read("成长系统/38_FDE全流程可指导方法论_v1.md")
    t39 = read("成长系统/39_514视频实战经验方法论文集_v1.md")
    t40 = read("成长系统/40_514视频补缺方法论_v1.md")
    t09 = read("成长系统/09_企业AI落地全流程关卡地图_v1.md")
    t25 = read("成长系统/25_程序全流程工程全景_v1.md")
    t34 = read("成长系统/34_企业AI落地全景地图_工作台.md")
    t43 = read("成长系统/43_Agent调度规则_v1.md")

    # 38: 8 SOP
    sops = [s.strip() for s in re.findall(r'^#{2,3}\s*(SOP\s*\d[^\n]*)', t38, re.M)]
    sop_nodes = []
    for s in sops:
        num = re.search(r'SOP\s*(\d)', s)
        title = re.sub(r'^SOP\s*\d\s*·?\s*', '', s)
        desc = first_para_after(t38, s)
        sop_nodes.append({"id": f"38-sop{num.group(1) if num else ''}", "label": title[:60], "type": "sop",
                          "desc": desc, "file": "成长系统/38_FDE全流程可指导方法论_v1.md", "anchor": s})

    # 39: 9 类 → 58 法
    cat_nodes = []
    for m in re.finditer(r'^##\s*([一二三四五六七八九]、[^\n]+)$', t39, re.M):
        cat = m.group(1).strip()
        start = m.end()
        nxt = re.search(r'^##\s*[一二三四五六七八九]、', t39[start:], re.M)
        seg = t39[start: start + (nxt.start() if nxt else 4000)]
        methods = []
        for mm in re.finditer(r'^###\s*方法\s*(\d+\.\d+)[：: ]*([^\n]*)', seg, re.M):
            mnum = mm.group(1)
            methods.append({"id": f"39-{mnum}", "label": f"{mnum} {mm.group(2).strip()}"[:60],
                            "type": "method", "file": "成长系统/39_514视频实战经验方法论文集_v1.md",
                            "anchor": f"方法 {mnum}",
                            "desc": after_heading(t39, f"方法 {mnum}")})
        cat_nodes.append({"id": "39-" + cat[:4], "label": cat[:44], "type": "cat39",
                          "desc": f"{len(methods)} 条方法", "children": methods})

    # 40: 16 条补缺
    gap_nodes = []
    for m in re.finditer(r'^#{1,6}\s*#?\s*([ABC]\d)\.\s*([^\n]+)$', t40, re.M):
        gap_nodes.append({"id": "40-" + m.group(1), "label": f"{m.group(1)} {m.group(2).strip()}"[:70],
                          "type": "gap",
                          "desc": after_heading(t40, f"{m.group(1)}. {m.group(2).strip()}"),
                          "file": "成长系统/40_514视频补缺方法论_v1.md",
                          "anchor": m.group(1)})

    # 09 阶段
    s09 = [x.strip() for x in re.findall(r'^###\s*(阶段\s*\d[^\n]*)', t09, re.M)]
    # 25 阶段 + 门禁
    s25 = [x.strip() for x in re.findall(r'^###\s*(阶段\s*\d+[^\n]*)', t25, re.M)]
    gates = [x.strip() for x in re.findall(r'^\|\s*(G\d[^\n]*?)\s*\|', t25, re.M)]
    # 34 轨 A
    a34 = [f"{a} {b.strip()}" for a, b in re.findall(r'^\|\s*(A\d)\s*\|\s*([^|]+)\|', t34, re.M)]

    # 方法卡（foundations）
    fcards = {}
    for root, dirs, files in os.walk(os.path.join(VAULT, "foundations")):
        dom = os.path.basename(root)
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            fp = os.path.join(root, f)
            t = open(fp, encoding="utf-8", errors="replace").read()
            m = re.search(r'^title:\s*(.+)$', t, re.M)
            title = m.group(1).strip().strip("'\"") if m else f[:-3]
            rel = os.path.relpath(fp, VAULT)
            body = re.sub(r'^---[\s\S]*?\n---\n', '', t)
            summ = ""
            for ln in body.split("\n"):
                s = ln.strip()
                if not s or s.startswith(("#", "|", ">", "```")):
                    continue
                s = re.sub(r'^\s*[-*+]\s*', '', s)
                s = re.sub(r'\*\*|`', '', s)
                if len(s) > 12:
                    summ = s[:180]
                    break
            fcards.setdefault(dom, []).append({"id": "f-" + f[:-3], "label": title[:60],
                                               "type": "fcard", "desc": summ, "file": rel})
    # 决策卡
    dcards = []
    for f in sorted(os.listdir(os.path.join(VAULT, "cards"))):
        if f.endswith(".md"):
            if f.startswith("index") or f.startswith("_"):
                continue
            ct = open(os.path.join(VAULT, "cards", f), encoding="utf-8", errors="replace").read()
            cbody = re.sub(r'^---[\s\S]*?\n---\n', '', ct)
            csum, cm = "", re.search(r'^#\s*([^\n]+)$', cbody, re.M)
            clabel = cm.group(1).strip() if cm else f[:-3]
            for ln in cbody.split("\n"):
                s = ln.strip()
                if not s or s.startswith(("#", "|", ">", "```")):
                    continue
                s = re.sub(r'^\s*[-*+]\s*', '', s)
                s = re.sub(r'\*\*|`', '', s)
                if len(s) > 12:
                    csum = s[:180]
                    break
            dcards.append({"id": "d-" + f[:-3], "label": clabel[:50], "type": "dcard",
                           "desc": csum, "file": "cards/" + f})

    # 素材池 (videos / clusters 从 panel 的 json 读)
    panel = os.path.expanduser("~/growth-system-panel")
    vid_nodes = []
    try:
        d = json.load(open(os.path.join(panel, "videos_library.json")))
        for c in d.get("cats", []):
            vid_nodes.append({"id": "v-" + c.get("name", "")[:6], "label": c.get("name", ""),
                              "type": "video", "desc": f"{len(c.get('items', []))} 条视频"})
    except Exception:
        pass
    clu_nodes = []
    try:
        mc = json.load(open(os.path.join(panel, "method_clusters.json")))
        for c in mc:
            clu_nodes.append({"id": "c-" + str(c.get("cat", ""))[:6], "label": c.get("cat", ""),
                              "type": "cluster",
                              "desc": f"{len(c.get('clusters', []))} 簇"})
    except Exception:
        pass

    # 43 调度规则场景
    rule_nodes = []
    for m in re.finditer(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', t43, re.M):
        if m.group(1) in ("#", ""):
            continue
        rule_nodes.append({"id": "r" + m.group(1), "label": m.group(2)[:40], "type": "rule",
                           "desc": f"查：{m.group(3).strip()}｜因为：{m.group(4).strip()}",
                           "file": "成长系统/43_Agent调度规则_v1.md"})

    tree = {
        "id": "root", "label": "企业 AI 落地 · 全景知识树", "type": "root",
        "desc": "点任意节点看内容；滚轮缩放、拖拽平移；节点左侧 ▸ 可展开收起",
        "children": [
            {"id": "A", "label": "A 落地主轴（7 阶段）", "type": "branch",
             "desc": "从接客户到规模化的完整落地路径；每阶段 = 业务在干什么 × 工程在干什么 × 权威依据 × 库内武器",
             "children": [
                 {"id": st[0], "label": f"{st[0]} {st[1]}", "type": "stage", "badge": st[2],
                  "desc": st[3], "file": "成长系统/09_企业AI落地全流程关卡地图_v1.md",
                  "anchor": f"阶段 {st[0].split()[1][:1] if st[0].split() else ''}",
                  "children": [
                      {"id": st[0] + "-biz", "label": "业务在干什么（09 · 34轨A）", "type": "leaf", "desc": st[3],
                       "file": "成长系统/09_企业AI落地全流程关卡地图_v1.md", "anchor": st[0]},
                      {"id": st[0] + "-eng", "label": "工程在干什么（25 · 34轨B）", "type": "leaf", "desc": st[4],
                       "file": "成长系统/25_程序全流程工程全景_v1.md", "anchor": st[2].split("+")[0]},
                      {"id": st[0] + "-src", "label": "权威依据（34轨C · 调研2）", "type": "leaf", "desc": st[5],
                       "file": "成长系统/34_企业AI落地全景地图_工作台.md"},
                      {"id": st[0] + "-gun", "label": f"库内武器（{len(st[6])} 件）", "type": "leaf",
                       "desc": " · ".join(st[6])},
                  ]} for st in STAGES
             ]},
            {"id": "B", "label": "B 方法论四件套（本轮提炼）", "type": "branch",
             "desc": "把 1000+ 素材变成能指导工作的东西：38 流程 SOP / 39 实战招式 / 40 补缺 / 41 MECE 汇总",
             "children": [
                 {"id": "38", "label": f"38 FDE 全流程可指导方法论（{len(sop_nodes)} 条 SOP）", "type": "doc",
                  "desc": "从 0 到 1 做 AI 项目的全流程：每条含 问题→步骤→产出物→坑→适配→出处",
                  "file": "成长系统/38_FDE全流程可指导方法论_v1.md", "children": sop_nodes},
                 {"id": "39", "label": f"39 视频实战经验方法论（9 类 {sum(len(c['children']) for c in cat_nodes)} 法）",
                  "type": "doc", "desc": "111 方法簇提炼：★接单弹药 / ⚪工具玩法 / 🟡可迁移",
                  "file": "成长系统/39_514视频实战经验方法论文集_v1.md", "children": cat_nodes},
                 {"id": "40", "label": f"40 视频补缺方法论（{len(gap_nodes)} 条）", "type": "doc",
                  "desc": "514 视频核心 3 类 64 条全文精读出的、没被 39 归纳进去的散点经验",
                  "file": "成长系统/40_514视频补缺方法论_v1.md", "children": gap_nodes},
                 {"id": "41", "label": "41 方法论三件套 MECE 汇总", "type": "doc",
                  "desc": "38/39/40 为什么不重不漏 + 怎么配合用", "file": "成长系统/41_方法论三件套MECE汇总_v1.md"},
                 {"id": "42", "label": "42 全景地图收口审计（为什么这么设计）", "type": "doc",
                  "desc": "10 个地图文档的图鉴 + 设计理由 + 权威等级 + 缺口",
                  "file": "成长系统/42_全景地图收口审计与总图_v1.md"},
             ]},
            {"id": "C", "label": "C 三张视角地图", "type": "branch",
             "desc": "同一件事的三种问法，互斥且穷尽：业务（怎么接单）／工程（怎么做出来）／权威（凭什么信）",
             "children": [
                 {"id": "09", "label": f"09 业务地图（{len(s09)} 阶段 37 关卡）", "type": "doc",
                  "desc": "接客户到规模化的业务侧全景", "file": "成长系统/09_企业AI落地全流程关卡地图_v1.md",
                  "children": [{"id": "09-" + x[:6], "label": x, "type": "leaf",
                                "file": "成长系统/09_企业AI落地全流程关卡地图_v1.md", "anchor": x} for x in s09]},
                 {"id": "25", "label": f"25 工程地图（{len(s25)} 阶段 {len(gates)} 门禁）", "type": "doc",
                  "desc": "一个程序从 0 到 1 到 N 的工程全流程", "file": "成长系统/25_程序全流程工程全景_v1.md",
                  "children": ([{"id": "25-" + x[:8], "label": x, "type": "leaf",
                                 "file": "成长系统/25_程序全流程工程全景_v1.md", "anchor": x} for x in s25]
                               + [{"id": "25-g" + g[:2], "label": g[:52], "type": "gate",
                                   "file": "成长系统/25_程序全流程工程全景_v1.md", "anchor": g[:6]} for g in gates])},
                 {"id": "34", "label": "34 权威地图 v2（三轨合流）", "type": "doc",
                  "desc": "轨A FDE交付（原厂一手）× 轨B 工程标准（云厂/ISO）× 轨C 企业治理（权威机构）",
                  "file": "成长系统/34_企业AI落地全景地图_工作台.md",
                  "children": [{"id": "34-" + a[:2], "label": a, "type": "leaf",
                                "file": "成长系统/34_企业AI落地全景地图_工作台.md", "anchor": a[:2]} for a in a34]},
             ]},
            {"id": "D", "label": f"D 方法卡（{sum(len(v) for v in fcards.values())} 张 · {len(fcards)} 域）",
             "type": "branch", "desc": "单点深度卡：接到项目时按域取用（检索走 retrieve_for_project.py）",
             "children": [{"id": "dom-" + dom, "label": f"{dom}（{len(v)}）", "type": "dom", "children": v}
                          for dom, v in sorted(fcards.items())]},
            {"id": "E", "label": f"E 决策卡（{len(dcards)} 张）", "type": "branch",
             "desc": "带档位+价格+适用边界，可直接拿出跟客户谈",
             "children": dcards},
            {"id": "F", "label": "F 素材池（原始弹药）", "type": "branch",
             "desc": "素材 ≠ 结论：对外引用前必须先经方法卡/SOP 验证",
             "children": [
                 {"id": "F1", "label": f"视频库 514 条（{len(vid_nodes)} 类）", "type": "pool", "children": vid_nodes},
                 {"id": "F2", "label": f"方法簇 111 簇（{len(clu_nodes)} 类）", "type": "pool", "children": clu_nodes},
                 {"id": "F3", "label": "术语词条 239（15 段客户生命周期）", "type": "pool",
                  "desc": "12 关键术语词典；网页里正文名词可点击"},
                 {"id": "F4", "label": "黄金集 19 场景（评测机制）", "type": "pool",
                  "desc": "golden-v1.1；改完卡跑 eval.py 看召回"},
                 {"id": "F5", "label": "学习池 22 篇 + raw 37 篇（别人的经验）", "type": "pool",
                  "desc": "FDE 六阶段速查手册 / 全网资料全景图 等"},
             ]},
            {"id": "G", "label": f"G 学习与调度（{len(rule_nodes)} 场景路由）", "type": "branch",
             "desc": "什么情况查什么、为什么 —— Agent 干活的成文规则",
             "children": ([{"id": "43", "label": "43 Agent 调度规则 v1（15 场景）", "type": "doc",
                            "file": "成长系统/43_Agent调度规则_v1.md", "children": rule_nodes}]
                          + [{"id": "05", "label": "05 顾问学习路线 v1", "type": "doc",
                              "file": "成长系统/05_顾问学习路线_v1.md"},
                             {"id": "29", "label": "29 学习方向六条", "type": "doc",
                              "file": "成长系统/29_学习方向六条_v1.md"},
                             {"id": "06", "label": "06 接客户前自问清单", "type": "doc",
                              "file": "成长系统/06_接客户前自问清单.md"},
                             {"id": "07", "label": "07 项目复盘清单", "type": "doc",
                              "file": "成长系统/07_项目复盘清单.md"}]),
             },
        ],
    }
    return tree


# ─────────────── 输出 HTML ───────────────
TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>企业AI落地 · 全景知识树</title>
<style>
:root{
  --bg:#000;
  --glass:rgba(28,28,30,.72);
  --panel:rgba(28,28,30,.88);
  --line:rgba(255,255,255,.08);
  --line2:rgba(255,255,255,.14);
  --txt:#f5f5f7;--dim:#a1a1a6;--dim2:#6e6e73;
  --blue:#0a84ff;--blue2:#409cff;--blueSoft:rgba(10,132,255,.16);
  --green:#30d158;--orange:#ff9f0a;--purple:#bf5af2;--teal:#40c8e0;--pink:#ff375f;
  --ease:cubic-bezier(.32,.72,0,1);
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%;overflow:hidden}
body{background:var(--bg);color:var(--txt);letter-spacing:.005em;
 font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display","PingFang SC","Helvetica Neue",sans-serif;
 -webkit-font-smoothing:antialiased}
#app{display:flex;flex-direction:column;height:100%}
/* ── 顶栏: 毛玻璃 ── */
#bar{height:52px;flex:0 0 52px;display:flex;align-items:center;gap:9px;padding:0 16px;
 background:var(--glass);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);
 border-bottom:1px solid var(--line);z-index:20;position:relative}
#bar .logo{font-size:14px;font-weight:600;letter-spacing:-.012em;white-space:nowrap}
#bar .logo span{color:var(--dim);font-weight:500}
#q{width:216px;height:31px;background:rgba(255,255,255,.06);border:1px solid transparent;border-radius:9px;
 color:var(--txt);padding:0 11px;font-size:13px;outline:none;font-family:inherit;transition:.2s var(--ease)}
#q::placeholder{color:var(--dim2)}
#q:focus{background:rgba(255,255,255,.1);border-color:var(--blue);box-shadow:0 0 0 3px var(--blueSoft)}
.btn{height:31px;padding:0 12px;border-radius:9px;background:rgba(255,255,255,.06);border:1px solid transparent;
 color:var(--dim);font-size:12.5px;font-weight:500;cursor:pointer;white-space:nowrap;font-family:inherit;
 transition:background .18s var(--ease),color .18s var(--ease),transform .12s var(--ease)}
.btn:hover{background:rgba(255,255,255,.11);color:var(--txt)}
.btn:active{transform:scale(.96)}
.btn.act{background:var(--blueSoft);color:var(--blue2);box-shadow:inset 0 0 0 1px rgba(10,132,255,.32)}
#hint{margin-left:auto;font-size:11.5px;color:var(--dim2);white-space:nowrap;font-weight:500}
/* ── 画布 ── */
#main{flex:1;display:flex;min-height:0;position:relative}
#canvas{flex:1;position:relative;overflow:hidden;cursor:grab;background:
 radial-gradient(1000px 620px at 18% -12%,rgba(10,132,255,.085),transparent 62%),
 radial-gradient(900px 700px at 92% 112%,rgba(191,90,242,.06),transparent 62%),var(--bg)}
#canvas.drag{cursor:grabbing}
svg{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:none}
.link{fill:none;stroke:rgba(255,255,255,.1);stroke-width:1.2}
.link.hi{stroke:rgba(10,132,255,.62);stroke-width:2}
.node{cursor:pointer}
.node .box{fill:rgba(255,255,255,.055);stroke:rgba(255,255,255,.1);stroke-width:1;rx:11;
 transition:fill .18s var(--ease),stroke .18s var(--ease)}
.node:hover .box{fill:rgba(255,255,255,.1);stroke:rgba(255,255,255,.22)}
.node.sel .box{fill:rgba(10,132,255,.18);stroke:var(--blue);stroke-width:1.5}
.node.dim{opacity:.16}
.node.hit .box{stroke:var(--orange);stroke-width:2}
.node .lab{fill:#f0f0f2;font-size:12.5px;font-weight:500;font-family:inherit;pointer-events:none;user-select:none}
.node .sub{fill:var(--dim2);font-size:10.5px;pointer-events:none;user-select:none;font-family:inherit}
.node .acc{pointer-events:none}
.node .tgl{fill:rgba(255,255,255,.09);rx:5;cursor:pointer;transition:fill .18s var(--ease)}
.node .tgl:hover{fill:rgba(255,255,255,.22)}
.node .tsig{fill:#c7c7cc;font-size:11px;font-weight:600;pointer-events:none;user-select:none;text-anchor:middle;font-family:inherit}
.n-root .box{fill:rgba(10,132,255,.16);stroke:rgba(10,132,255,.5)}
/* ── 侧栏: 毛玻璃 ── */
#side{width:0;flex:0 0 0;background:var(--panel);-webkit-backdrop-filter:saturate(180%) blur(24px);
 backdrop-filter:saturate(180%) blur(24px);border-left:1px solid var(--line);overflow:hidden;z-index:15;
 transition:flex-basis .32s var(--ease),width .32s var(--ease);display:flex;flex-direction:column}
#side.on{width:392px;flex:0 0 392px}
#side .hd{padding:18px 20px 14px;border-bottom:1px solid var(--line);flex:0 0 auto}
#side .badge{display:inline-block;font-size:10px;font-weight:600;letter-spacing:.06em;padding:3px 9px;border-radius:999px;
 background:rgba(255,255,255,.08);color:var(--dim);margin-bottom:10px}
#side h2{font-size:16.5px;line-height:1.42;font-weight:600;letter-spacing:-.015em;word-break:break-word}
#side .bd{padding:18px 20px 26px;overflow-y:auto;flex:1;-webkit-overflow-scrolling:touch}
#side .bd p{color:#d6d6da;margin-bottom:14px;font-size:13.5px;line-height:1.78}
#side .kv{font-size:11.5px;color:var(--dim2);margin-bottom:8px;word-break:break-all;line-height:1.6}
#side .acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
#side .act{font-size:13px;font-weight:500;padding:9px 14px;border-radius:10px;background:var(--blue);color:#fff;
 border:none;cursor:pointer;font-family:inherit;transition:.18s var(--ease);box-shadow:0 1px 3px rgba(0,0,0,.35)}
#side .act:hover{background:#0a76e6}
#side .act:active{transform:scale(.97)}
#side .children{margin-top:20px;border-top:1px solid var(--line);padding-top:16px}
#side .children .t{font-size:11px;color:var(--dim2);font-weight:600;letter-spacing:.06em;margin-bottom:10px}
#side .chip{display:inline-block;font-size:12.5px;padding:6px 11px;margin:0 6px 6px 0;border-radius:9px;
 background:rgba(255,255,255,.07);border:1px solid transparent;cursor:pointer;color:#d0d0d5;font-family:inherit;
 transition:.18s var(--ease)}
#side .chip:hover{background:rgba(255,255,255,.13);color:#fff;border-color:var(--line2)}
#sideMask{position:absolute;inset:0;background:rgba(0,0,0,.5);z-index:14;display:none}
#sideMask.on{display:block}
/* ── 原文弹层: iOS sheet ── */
#modal{position:fixed;inset:0;z-index:60;display:none;padding:44px 24px 24px;
 background:rgba(0,0,0,.62);-webkit-backdrop-filter:blur(18px) saturate(180%);backdrop-filter:blur(18px) saturate(180%);
 animation:fadeIn .22s var(--ease)}
#modal.on{display:flex;align-items:flex-start;justify-content:center}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes sheetUp{from{opacity:0;transform:translateY(16px) scale(.99)}to{opacity:1;transform:none}}
#mwrap{background:#1c1c1e;border:1px solid var(--line2);border-radius:18px;max-width:880px;width:100%;
 max-height:calc(100vh - 68px);display:flex;flex-direction:column;overflow:hidden;
 box-shadow:0 26px 74px rgba(0,0,0,.62);animation:sheetUp .3s var(--ease)}
#mhd{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;flex:0 0 auto;
 background:rgba(28,28,30,.94);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
 position:sticky;top:0;z-index:3}
#mhd .t{font-size:13px;font-weight:500;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--dim)}
#mback{display:flex;align-items:center;gap:5px;height:32px;padding:0 14px 0 11px;border-radius:9px;border:none;
 background:var(--blueSoft);color:var(--blue2);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;
 transition:.18s var(--ease);white-space:nowrap}
#mback:hover{background:rgba(10,132,255,.28)}
#mback:active{transform:scale(.96)}
#mbd{padding:26px 30px 44px;overflow-y:auto;font-size:14px;line-height:1.82;color:#e2e2e6;-webkit-overflow-scrolling:touch}
#mbd h1{font-size:21px;font-weight:700;letter-spacing:-.02em;margin:4px 0 16px;padding-bottom:12px;border-bottom:1px solid var(--line)}
#mbd h2{font-size:17px;font-weight:600;letter-spacing:-.012em;margin:26px 0 11px;color:#eef2ff}
#mbd h3{font-size:15px;font-weight:600;margin:19px 0 9px;color:#dbe4f7}
#mbd h4{font-size:14px;font-weight:600;margin:15px 0 7px;color:#cdd7ec}
#mbd p{margin-bottom:12px}
#mbd ul,#mbd ol{margin:0 0 13px 22px}
#mbd li{margin-bottom:6px}
#mbd table{width:100%;border-collapse:collapse;font-size:12.8px;margin:14px 0;
 border:1px solid var(--line);border-radius:10px;overflow:hidden}
#mbd th{background:rgba(255,255,255,.05);text-align:left;padding:9px 10px;color:var(--dim);font-size:11.5px;
 font-weight:600;border-bottom:1px solid var(--line)}
#mbd td{padding:9px 10px;border-bottom:1px solid rgba(255,255,255,.045);vertical-align:top}
#mbd code{background:rgba(255,255,255,.08);padding:2px 6px;border-radius:5px;font-size:12.2px}
#mbd pre{background:#141416;border:1px solid var(--line);border-radius:11px;padding:13px;overflow-x:auto;
 margin:13px 0;font-size:12.2px}
#mbd blockquote{border-left:3px solid var(--blue);padding:3px 0 3px 13px;color:var(--dim);margin:13px 0}
#mbd hr{border:none;border-top:1px solid var(--line);margin:20px 0}
#mbd a{color:var(--blue2)}
/* ── 图例 / 缩放 ── */
#leg{position:absolute;left:16px;bottom:16px;background:rgba(28,28,30,.74);-webkit-backdrop-filter:blur(20px) saturate(180%);
 backdrop-filter:blur(20px) saturate(180%);border:1px solid var(--line);border-radius:14px;padding:12px 14px;
 font-size:11.5px;color:var(--dim);line-height:2;z-index:10}
#leg b{color:#e8e8ea;font-weight:600;font-size:11px;letter-spacing:.05em}
#leg i{display:inline-block;width:8px;height:8px;border-radius:2.5px;margin-right:7px;vertical-align:middle}
#zoomctl{position:absolute;right:16px;bottom:16px;display:flex;gap:8px;z-index:10}
#zoomctl .btn{width:36px;height:36px;padding:0;font-size:16px;border-radius:11px;
 background:rgba(28,28,30,.8);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
 border:1px solid var(--line);color:var(--dim)}
#zoomctl .btn:hover{background:rgba(58,58,62,.92);color:#fff}
/* ── 手机 / 平板 ── */
@media(max-width:900px){
  #bar{height:auto;flex:0 0 auto;flex-wrap:wrap;padding:9px 12px;gap:8px}
  #bar .logo{font-size:13px;order:1;flex:1}
  #hint{display:none}
  .btn{height:32px;padding:0 11px;font-size:12.5px;order:2}
  #q{order:3;width:100%;height:35px;font-size:15px}
  #leg{display:none}
  #zoomctl{right:12px;bottom:12px}
  #zoomctl .btn{width:40px;height:40px;font-size:18px}
  #side{position:fixed;left:0;right:0;bottom:0;top:auto;width:100%;flex:none;height:auto;max-height:68vh;
   border-left:none;border-top:1px solid var(--line);border-radius:20px 20px 0 0;transform:translateY(103%);
   transition:transform .34s var(--ease);box-shadow:0 -14px 54px rgba(0,0,0,.58)}
  #side.on{width:100%;flex:none;transform:translateY(0)}
  #side .hd{padding:10px 18px 12px}
  #side .hd::before{content:"";display:block;width:38px;height:4px;border-radius:2px;
   background:rgba(255,255,255,.22);margin:0 auto 12px}
  #side .bd{padding:14px 18px 34px}
  #modal{padding:0}
  #mwrap{max-width:100%;height:100%;max-height:100%;border-radius:0;border:none}
  #mhd{padding:9px 12px}
  #mback{height:42px;padding:0 17px 0 13px;font-size:14.5px;border-radius:11px}
  #mhd .t{display:none}
  #mbd{padding:20px 18px 70px;font-size:15px;line-height:1.85}
  #mbd h1{font-size:19px}
  #mbd h2{font-size:16.5px}
  #mbd table{font-size:12.5px}
}
</style>
</head>
<body>
<div id="app">
  <div id="bar">
    <div class="logo">🧭 全景知识树 <span>企业AI落地</span></div>
    <input id="q" placeholder="搜索节点…" autocomplete="off">
    <button class="btn" id="bExpand">展开</button>
    <button class="btn" id="bCollapse">收起</button>
    <button class="btn" id="bFit">适应</button>
    <button class="btn" id="bD3">三层</button>
    <div id="hint">滚轮缩放 · 拖拽平移 · 点节点看内容</div>
  </div>
  <div id="main">
    <div id="canvas">
      <svg id="svg"><g id="world"><g id="links"></g><g id="nodes"></g></g></svg>
      <div id="leg"></div>
      <div id="zoomctl">
        <button class="btn" id="bIn">＋</button>
        <button class="btn" id="bOut">－</button>
      </div>
    </div>
    <div id="sideMask"></div>
    <div id="side">
      <div class="hd"><div class="badge" id="sBadge">节点</div><h2 id="sTitle">—</h2></div>
      <div class="bd">
        <div id="sDesc"></div>
        <div class="kv" id="sFile"></div>
        <div class="acts" id="sActs"></div>
        <div class="children" id="sKids"></div>
      </div>
    </div>
  </div>
</div>
<div id="modal"><div id="mwrap">
  <div id="mhd"><button id="mback">‹ 返回</button><div class="t" id="mtitle">原文</div></div>
  <div id="mbd"></div>
</div></div>

<script>
var DATA = /*__DATA__*/;
var COLORS = {root:"#0a84ff",branch:"#0a84ff",stage:"#0a84ff",doc:"#30d158",sop:"#409cff",method:"#8e8e93",
 gap:"#ff9f0a",fcard:"#40c8e0",dcard:"#bf5af2",pool:"#40c8e0",video:"#40c8e0",cluster:"#40c8e0",
 rule:"#bf5af2",gate:"#ff9f0a",dom:"#8e8e93",cat39:"#8e8e93",leaf:"#8e8e93",dflt:"#8e8e93"};
var TYPELABEL = {root:"总入口",branch:"一级板块",stage:"落地阶段",doc:"方法论文档",sop:"SOP 流程",
 method:"实战方法",gap:"补缺经验",fcard:"方法卡",dcard:"决策卡",pool:"素材池",video:"视频类目",
 cluster:"方法簇",rule:"调度场景",gate:"质量门禁",dom:"方法卡域",cat39:"方法类目",leaf:"要点"};

/* ---------- 视图状态 ---------- */
var collapsed = {};          // id -> true 收起
var sel = null;
var k = 1, tx = 40, ty = 40;
var NW = {root:250,branch:250,stage:230,doc:290,sop:250,method:225,gap:245,fcard:230,dcard:230,
 pool:250,video:215,cluster:215,rule:230,gate:210,dom:190,cat39:220,leaf:250};
var NH = 30, VGAP = 9;

function isOpen(n){ return !collapsed[n.id]; }
function visibleKids(n){
  if(!n.children || !n.children.length) return [];
  return isOpen(n) ? n.children : [];
}

/* ---------- 布局: 简洁横向树 ---------- */
var layoutNodes = [], layoutLinks = [];
function layout(){
  layoutNodes = []; layoutLinks = [];
  var y = 0;
  function walk(n, depth, parent){
    var kids = visibleKids(n);
    var w = NW[n.type] || 230;
    var node = {n:n, depth:depth, x:depth*300, y:0, w:w, h:NH, parent:parent, kids:kids};
    if(kids.length){
      var startY = y;
      kids.forEach(function(ch){ walk(ch, depth+1, node); });
      node.y = (startY + y - VGAP) / 2;
    } else {
      node.y = y; y += NH + VGAP;
    }
    layoutNodes.push(node);
    if(parent) layoutLinks.push({p:parent, c:node});
    return node;
  }
  y = 0;
  walk(DATA, 0, null);
}

/* ---------- 渲染 ---------- */
var NS = "http://www.w3.org/2000/svg";
function el(t, a){ var e = document.createElementNS(NS, t); for(var k2 in a) e.setAttribute(k2, a[k2]); return e; }
function trunc(s, n){ return s.length > n ? s.slice(0, n-1) + "…" : s; }

function render(){
  layout();
  var lg = document.getElementById("links"), ng = document.getElementById("nodes");
  lg.innerHTML = ""; ng.innerHTML = "";
  // links
  layoutLinks.forEach(function(l){
    var x1 = l.p.x + l.p.w, y1 = l.p.y + NH/2, x2 = l.c.x, y2 = l.c.y + NH/2;
    var mx = (x1 + x2) / 2;
    var p = el("path", {class:"link", d:"M"+x1+","+y1+" C"+mx+","+y1+" "+mx+","+y2+" "+x2+","+y2});
    lg.appendChild(p);
  });
  // nodes
  layoutNodes.forEach(function(nd){
    var n = nd.n;
    var g = el("g", {class:"node n-" + n.type + (sel && sel.id === n.id ? " sel" : "")});
    g.setAttribute("transform", "translate(" + nd.x + "," + nd.y + ")");
    g.appendChild(el("rect", {class:"box", x:0, y:0, width:nd.w, height:NH, rx:11}));
    g.appendChild(el("rect", {class:"acc", x:3, y:7, width:3, height:NH-14, rx:1.5,
      fill:(COLORS[n.type] || COLORS.dflt), opacity:.9}));
    var t = el("text", {class:"lab", x:15, y:19});
    t.textContent = trunc(n.label, Math.floor((nd.w-30)/6.6));
    g.appendChild(t);
    if(n.badge){
      var b = el("text", {class:"sub", x:15, y:29});
      b.textContent = n.badge;
      g.appendChild(b);
    }
    if(n.children && n.children.length){
      var tg = el("g", {class:"tgl"});
      tg.setAttribute("transform", "translate(" + (nd.w - 15) + ",9)");
      tg.appendChild(el("rect", {width:12, height:12, rx:3}));
      var s = el("text", {class:"tsig", x:6, y:10});
      s.textContent = isOpen(n) ? "–" : "+";
      tg.appendChild(s);
      tg.addEventListener("click", function(ev){ ev.stopPropagation(); toggle(n.id); });
      g.appendChild(tg);
    }
    g.addEventListener("click", function(){ pick(n, nd); });
    ng.appendChild(g);
  });
  applyT();
}

function applyT(){ document.getElementById("world").setAttribute("transform", "translate("+tx+","+ty+") scale("+k+")"); }

function toggle(id){
  if(collapsed[id]) delete collapsed[id]; else collapsed[id] = true;
  render(); if(sel) drawSide(sel);
}

/* ---------- 交互: 缩放/平移 (鼠标 + 触摸) ---------- */
var cv = document.getElementById("canvas");
function zoomAt(mx, my, f){
  var nk = Math.max(0.12, Math.min(3.2, k * f));
  tx = mx - (mx - tx) * (nk / k); ty = my - (my - ty) * (nk / k); k = nk; applyT();
}
cv.addEventListener("wheel", function(e){
  e.preventDefault();
  var r = cv.getBoundingClientRect();
  zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.12 : 1/1.12);
}, {passive:false});
/* 鼠标拖拽 */
var dragging = false, sx = 0, sy = 0, stx = 0, sty = 0;
cv.addEventListener("mousedown", function(e){
  if(e.target.closest(".node")) return;
  dragging = true; sx = e.clientX; sy = e.clientY; stx = tx; sty = ty; cv.classList.add("drag");
});
window.addEventListener("mousemove", function(e){
  if(!dragging) return;
  tx = stx + (e.clientX - sx); ty = sty + (e.clientY - sy); applyT();
});
window.addEventListener("mouseup", function(){ dragging = false; cv.classList.remove("drag"); });
/* 触摸: 单指平移 + 双指捏合缩放(手机/平板) */
var touching = false, pinchD = 0, pinchK = 1;
function tdist(t){ return Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY); }
cv.addEventListener("touchstart", function(e){
  if(e.target.closest(".node")) return;
  if(e.touches.length === 1){
    touching = true; pinchD = 0;
    sx = e.touches[0].clientX; sy = e.touches[0].clientY; stx = tx; sty = ty;
  } else if(e.touches.length === 2){
    touching = true; pinchD = tdist(e.touches); pinchK = k;
    sx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
    sy = (e.touches[0].clientY + e.touches[1].clientY) / 2;
    stx = tx; sty = ty;
  }
}, {passive:true});
cv.addEventListener("touchmove", function(e){
  if(!touching) return;
  e.preventDefault();
  var r = cv.getBoundingClientRect();
  if(e.touches.length === 1 && pinchD === 0){
    tx = stx + (e.touches[0].clientX - sx); ty = sty + (e.touches[0].clientY - sy); applyT();
  } else if(e.touches.length === 2 && pinchD > 0){
    var d = tdist(e.touches);
    var cx = (e.touches[0].clientX + e.touches[1].clientX) / 2 - r.left;
    var cy = (e.touches[0].clientY + e.touches[1].clientY) / 2 - r.top;
    var nk = Math.max(0.12, Math.min(3.2, pinchK * (d / pinchD)));
    var pk = k; k = nk;
    tx = cx - (cx - tx) * (nk / pk); ty = cy - (cy - ty) * (nk / pk); applyT();
  }
}, {passive:false});
cv.addEventListener("touchend", function(e){
  if(e.touches.length === 0){ touching = false; pinchD = 0; }
  else if(e.touches.length === 1){
    pinchD = 0;
    sx = e.touches[0].clientX; sy = e.touches[0].clientY; stx = tx; sty = ty;
  }
}, {passive:true});
function zoom(f){ var r = cv.getBoundingClientRect(); zoomAt(r.width/2, r.height/2, f); }
document.getElementById("bIn").onclick = function(){ zoom(1.25); };
document.getElementById("bOut").onclick = function(){ zoom(0.8); };
/* 取景: 把一组节点框进视野 */
function contentBox(nodes){
  if(!nodes.length) return null;
  return {
    x0: Math.min.apply(null, nodes.map(function(a){ return a.x; })),
    x1: Math.max.apply(null, nodes.map(function(a){ return a.x + a.w; })),
    y0: Math.min.apply(null, nodes.map(function(a){ return a.y; })),
    y1: Math.max.apply(null, nodes.map(function(a){ return a.y + NH; })),
    w: 0, h: 0
  };
}
function frameBox(b, maxK, minK){
  if(!b) return;
  b.w = b.x1 - b.x0; b.h = b.y1 - b.y0;
  var r = cv.getBoundingClientRect();
  var pad = (r.width < 900 ? 24 : 70);
  k = Math.max(minK, Math.min(maxK, Math.min((r.width - pad*2)/(b.w+1), (r.height - pad*2)/(b.h+1))));
  tx = pad + (r.width - pad*2 - b.w*k)/2 - b.x0*k;
  ty = pad + (r.height - pad*2 - b.h*k)/2 - b.y0*k;
  applyT();
}
function fit(){ frameBox(contentBox(layoutNodes), 1.15, 0.22); }
document.getElementById("bFit").onclick = fit;
function setAll(v){
  collapsed = {};
  if(v){ (function w(n){ (n.children||[]).forEach(function(c){ collapsed[c.id] = true; if(c.children && c.children.length) w(c); }); })(DATA); }
  render(); if(sel) drawSide(sel);
}
document.getElementById("bExpand").onclick = function(){ setAll(false); fit(); };
document.getElementById("bCollapse").onclick = function(){ setAll(true); fit(); };

/* ---------- 侧栏 ---------- */
function closeSide(){
  document.getElementById("side").classList.remove("on");
  document.getElementById("sideMask").classList.remove("on");
}
function drawSide(n){
  sel = n;
  document.getElementById("side").classList.add("on");
  if(window.innerWidth <= 900) document.getElementById("sideMask").classList.add("on");
  document.getElementById("sBadge").textContent = TYPELABEL[n.type] || n.type;
  document.getElementById("sTitle").textContent = n.label;
  document.getElementById("sDesc").innerHTML = n.desc ? "<p>" + n.desc.replace(/·/g, " · ") + "</p>" : "";
  document.getElementById("sFile").textContent = n.file ? ("出处：" + n.file) : "";
  var acts = document.getElementById("sActs");
  acts.innerHTML = "";
  if(n.file){
    var b = document.createElement("div"); b.className = "act"; b.textContent = "📖 打开原文";
    b.onclick = function(){ openDoc(n.file, n.anchor, n.label); };
    acts.appendChild(b);
  }
  var kidsEl = document.getElementById("sKids");
  kidsEl.innerHTML = "";
  if(n.children && n.children.length){
    kidsEl.innerHTML = '<div class="t">子节点（'+n.children.length+'）· 点开跳到该节点</div>';
    n.children.forEach(function(c){
      var ch = document.createElement("span"); ch.className = "chip"; ch.textContent = trunc(c.label, 26);
      ch.onclick = function(){ pick(c, null); };
      kidsEl.appendChild(ch);
    });
  }
  render();
}
function pick(n, nd){
  // 点节点 = 选中 + 自动展开下一层（脑图钻取手感）
  if(n.children && n.children.length && collapsed[n.id]) delete collapsed[n.id];
  drawSide(n);
  // 放大到「以该节点为根的可读视图」——钻取时永远看得清
  fitToSub(n, nd);
}
function fitToSub(n, nd){
  var ids = {}; (function w(x){ ids[x.id] = true; visibleKids(x).forEach(w); })(n);
  var sub = layoutNodes.filter(function(a){ return ids[a.n.id]; });
  frameBox(contentBox(sub), 1.25, 0.34);
}
/* ---------- 原文 modal (极简 markdown 渲染) ---------- */
function md2html(md){
  var L = md.split("\n"), out = [], i = 0, inCode = false, codeBuf = [];
  function inline(s){
    s = s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    return s;
  }
  while(i < L.length){
    var ln = L[i];
    if(ln.trim().startsWith("```")){
      if(!inCode){ inCode = true; codeBuf = []; }
      else { inCode = false; out.push("<pre>" + codeBuf.join("\n") + "</pre>"); }
      i++; continue;
    }
    if(inCode){ codeBuf.push(ln.replace(/&/g,"&amp;").replace(/</g,"&lt;")); i++; continue; }
    if(/^\s*\|.*\|\s*$/.test(ln) && i+1 < L.length && /^\s*\|[\s:-]+\|\s*$/.test(L[i+1])){
      var rows = [];
      while(i < L.length && /^\s*\|.*\|\s*$/.test(L[i])){
        var cells = L[i].trim().replace(/^\||\|$/g, "").split("|");
        if(!/^[\s:-]+$/.test(cells[0] || "")) rows.push(cells);
        i++;
      }
      var h = "<table><tr>" + rows[0].map(function(c){ return "<th>" + inline(c.trim()) + "</th>"; }).join("") + "</tr>";
      for(var r = 1; r < rows.length; r++) h += "<tr>" + rows[r].map(function(c){ return "<td>" + inline(c.trim()) + "</td>"; }).join("") + "</tr>";
      out.push(h + "</table>"); continue;
    }
    var m;
    if((m = ln.match(/^(#{1,6})\s+(.*)$/))){ out.push("<h" + m[1].length + ">" + inline(m[2]) + "</h" + m[1].length + ">"); i++; continue; }
    if(/^\s*(---|\*\*\*)\s*$/.test(ln)){ out.push("<hr>"); i++; continue; }
    if(/^\s*>\s?/.test(ln)){ out.push("<blockquote>" + inline(ln.replace(/^\s*>\s?/, "")) + "</blockquote>"); i++; continue; }
    if(/^\s*[-*]\s+/.test(ln)){
      var li = [];
      while(i < L.length && /^\s*[-*]\s+/.test(L[i])){ li.push("<li>" + inline(L[i].replace(/^\s*[-*]\s+/, "")) + "</li>"); i++; }
      out.push("<ul>" + li.join("") + "</ul>"); continue;
    }
    if(/^\s*\d+\.\s+/.test(ln)){
      var lo = [];
      while(i < L.length && /^\s*\d+\.\s+/.test(L[i])){ lo.push("<li>" + inline(L[i].replace(/^\s*\d+\.\s+/, "")) + "</li>"); i++; }
      out.push("<ol>" + lo.join("") + "</ol>"); continue;
    }
    if(ln.trim() === ""){ i++; continue; }
    out.push("<p>" + inline(ln) + "</p>"); i++;
  }
  return out.join("\n");
}
function openDoc(file, anchor, title){
  document.getElementById("mtitle").textContent = title || file;
  document.getElementById("modal").classList.add("on");
  if(!modalOn){
    modalOn = true;
    try { history.pushState({__doc:1}, ""); } catch(e){}
  }
  var bd = document.getElementById("mbd");
  bd.innerHTML = "<p style='color:#98a1b0'>加载中… " + file + "</p>";
  fetch("obs/" + file.split("/").map(encodeURIComponent).join("/")).then(function(r){
    if(!r.ok) throw new Error("HTTP " + r.status);
    return r.text();
  }).then(function(t){
    // 去 frontmatter
    t = t.replace(/^---[\s\S]*?\n---\n/, "");
    bd.innerHTML = md2html(t);
    if(anchor){
      var hits = bd.querySelectorAll("h1,h2,h3,h4");
      for(var q = 0; q < hits.length; q++){
        if(hits[q].textContent.indexOf(anchor) >= 0 || anchor.indexOf(hits[q].textContent.trim()) >= 0){
          hits[q].scrollIntoView({block:"start"}); hits[q].style.color = "#f5b544"; break;
        }
      }
    }
    bd.scrollTop = bd.scrollTop;
  }).catch(function(e){
    bd.innerHTML = "<p style='color:#ff6b6b'>原文加载失败：" + e.message + "</p><p style='color:#98a1b0'>文件：" + file + "</p>";
  });
}
/* 弹层开关 = 接浏览器返回键(手机上按返回=关弹层, 不是退出页面) */
var modalOn = false;
function hideDoc(){
  document.getElementById("modal").classList.remove("on");
  modalOn = false;
}
function closeDoc(){
  hideDoc();                                        // 立即关闭(不等异步 popstate)
  if(history.state && history.state.__doc){         // 再清掉这次 push 的历史, 免得返回键要按两次
    try { history.back(); } catch(e){}
  }
}
document.getElementById("mback").onclick = closeDoc;
document.getElementById("modal").onclick = function(e){ if(e.target.id === "modal") closeDoc(); };
document.getElementById("sideMask").onclick = closeSide;
window.addEventListener("popstate", function(){
  if(modalOn){ hideDoc(); return; }
  if(document.getElementById("side").classList.contains("on")) closeSide();
});
document.addEventListener("keydown", function(e){
  if(e.key === "Escape" && modalOn) closeDoc();
});

/* ---------- 三层视角 ---------- */
document.getElementById("bD3").onclick = function(){
  var ids = ["A","B","C","D","E","F","G"];
  collapsed = {};
  (function w(n){
    (n.children||[]).forEach(function(c){
      if(ids.indexOf(c.id) >= 0) delete collapsed[c.id];
      else if(c.children && c.children.length) collapsed[c.id] = true;
      w(c);
    });
  })(DATA);
  delete collapsed["A"]; delete collapsed["B"]; delete collapsed["C"];
  render(); fit();
};

/* ---------- 搜索 ---------- */
var q = document.getElementById("q");
q.addEventListener("input", function(){
  var v = q.value.trim().toLowerCase();
  var nodes = document.querySelectorAll(".node");
  if(!v){ nodes.forEach(function(e){ e.classList.remove("dim","hit"); }); return; }
  // 命中自动展开祖先
  var hitIds = {};
  (function w(n, chain){
    (n.children||[]).forEach(function(c){
      var c2 = chain.concat([c]);
      if((c.label + " " + (c.desc||"") + " " + (c.badge||"")).toLowerCase().indexOf(v) >= 0){
        c2.forEach(function(a){ delete collapsed[a.id]; });
        hitIds[c.id] = true;
      }
      w(c, c2);
    });
  })(DATA, []);
  render();
  var idx = {}; layoutNodes.forEach(function(nd, i){ idx[nd.n.id] = i; });
  var all = document.querySelectorAll(".node");
  all.forEach(function(e, i){ e.classList.remove("dim","hit"); });
  layoutNodes.forEach(function(nd, i){
    var e = all[i]; if(!e) return;
    if(hitIds[nd.n.id]) e.classList.add("hit"); else e.classList.add("dim");
  });
});

/* ---------- 图例 ---------- */
document.getElementById("leg").innerHTML =
 '<div style="margin-bottom:6px"><b>图例</b></div>' +
 [['branch','板块'],['stage','阶段'],['doc','方法论'],['sop','SOP'],['method','方法'],['gap','补缺'],['fcard','方法卡'],['dcard','决策卡'],['rule','调度'],['pool','素材']]
 .map(function(x){ return '<div><i style="background:' + (COLORS[x[0]]||"#8e8e93") + '"></i>' + x[1] + '</div>'; }).join("");

/* ---------- 启动 ---------- */
// 默认: 只展开「总根 + 一级板块」，其余收起(保证一屏能看清)；点节点逐层钻取
(function initCollapse(){
  collapsed = {};
  (DATA.children || []).forEach(function(b){
    if(b.children && b.children.length) collapsed[b.id] = true;
  });
})();
render(); fit();
</script>
</body>
</html>
"""


def main():
    tree = build_tree()
    html = TPL.replace("/*__DATA__*/", json.dumps(tree, ensure_ascii=False))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    # 统计
    cnt = [0]
    def w(n):
        cnt[0] += 1
        for c in n.get("children", []):
            w(c)
    w(tree)
    print(f"✅ 生成 {OUT}")
    print(f"   节点总数: {cnt[0]}")


if __name__ == "__main__":
    main()
