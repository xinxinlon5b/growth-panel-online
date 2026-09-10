# -*- coding: utf-8 -*-
"""鱼骨图 SOP 学习页 · v4 重做版(2026-09-10)
- 鱼骨图改为固定 viewBox 1400x900,SVG 整体缩放
- 每个步骤/反模式/军规 = 一个矩形文字块 + 斜线 + 圆点
- 文字用 <text> + <tspan dy> 多行换行,避免重叠
- 整个页面只画一张鱼骨图(主轴+上分支+下分支),不分散
- 苹果风 UI / 黑底 / 大留白
"""
import json, os, html

BASE = "/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库"
OUT = "/Users/tkdesign/growth-system-panel/sop.html"
from _sops_data import SOPS


# ============== SVG 鱼骨图 · 用百分比坐标(避开绝对像素问题) ==============
def wrap_text(text, max_chars=14):
    """中文文本按 max_chars 字符换行"""
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    lines = []
    while len(text) > max_chars:
        # 找最近的标点或空格作为切分点
        cut = text[:max_chars]
        # 优先在标点处切
        for i in range(len(cut)-1, max(0, len(cut)-4), -1):
            if cut[i] in '，。、 ；:：?？!！ ':
                cut = text[:i+1]
                break
        else:
            cut = text[:max_chars]
        lines.append(cut)
        text = text[len(cut):]
    if text:
        lines.append(text)
    return lines


def render_fishbone_svg(sop, W=1400, H=900):
    """完整鱼骨图(单图,不分多块)
    - viewBox 固定 1400x900
    - 主轴 y=450 水平
    - 上方步骤:斜线向上 60° ,矩形文字块 (宽 280,高 120)
    - 下方反模式/军规:斜线向下 60° ,矩形文字块 (宽 280,高 120)
    - 文字用 <tspan> 换行避免重叠
    """
    steps = sop["steps"]
    aps = sop.get("antipatterns", [])
    rules = sop.get("keyrules", [])
    # 下方分支
    bot = []
    for ap in aps[:3]: bot.append({"type":"warn", "short":ap, "tag":"反模式"})
    for r in rules[:3]: bot.append({"type":"army", "short":r, "tag":"军规"})
    # ===== 布局参数 =====
    main_y = H / 2  # 450
    margin_l, margin_r = 60, 60
    main_x0 = margin_l
    main_x1 = W - margin_r  # 1340
    # 主轴线
    parts = []
    parts.append(f'<line x1="{main_x0}" y1="{main_y}" x2="{main_x1}" y2="{main_y}" stroke="#5a5a5f" stroke-width="3"/>')
    # 起点圆点
    parts.append(f'<circle cx="{main_x0}" cy="{main_y}" r="11" fill="#5a5a5f" stroke="#fff" stroke-width="2.5"/>')
    parts.append(f'<text x="{main_x0+18}" y="{main_y+6}" fill="#86868b" font-size="18" font-weight="600">起点</text>')
    # 鱼头
    head_x = main_x1 + 5
    parts.append(f'<polygon points="{head_x},{main_y} {main_x1-22},{main_y-18} {main_x1-22},{main_y+18}" fill="#5a5a5f"/>')
    # 步骤块尺寸
    box_w, box_h = 220, 130
    line_len = 90  # 斜线长度
    # ===== 上方步骤(等距) =====
    if steps:
        step_gap = (main_x1 - main_x0 - 80) / (len(steps) + 1)
        for i, st in enumerate(steps):
            # 主轴上的连接点(等距)
            anchor_x = main_x0 + 40 + step_gap * (i + 1)
            # 倾斜 25° 朝右上
            angle_deg = 25
            # 文字块位置(以斜线终点为中心)
            # 斜线终点 = (anchor_x + line_len * cos25, main_y - line_len * sin25)
            import math
            rad = math.radians(angle_deg)
            line_end_x = anchor_x + line_len * math.cos(rad)
            line_end_y = main_y - line_len * math.sin(rad)
            # 文字块左上角
            box_x = line_end_x
            box_y = line_end_y - box_h  # 文字块底部与斜线终点齐
            # 斜线
            parts.append(f'<line x1="{anchor_x}" y1="{main_y}" x2="{line_end_x}" y2="{line_end_y}" stroke="#2997ff" stroke-width="2.5"/>')
            # 主轴圆点
            parts.append(f'<circle cx="{anchor_x}" cy="{main_y}" r="10" fill="#2997ff" stroke="#fff" stroke-width="2.5"/>')
            # 文字块底色(微妙玻璃感)
            parts.append(f'<rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" rx="14" ry="14" fill="#2997ff" fill-opacity="0.06" stroke="#2997ff" stroke-opacity="0.25" stroke-width="1"/>')
            # 编号(左上角徽章)
            parts.append(f'<circle cx="{box_x+22}" cy="{box_y+22}" r="14" fill="#2997ff"/>')
            parts.append(f'<text x="{box_x+22}" y="{box_y+27}" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">{i+1}</text>')
            # 标题
            title = html.escape(st["title"][:16])
            parts.append(f'<text x="{box_x+44}" y="{box_y+27}" fill="#2997ff" font-size="15" font-weight="700">{title}</text>')
            # body 多行
            body_lines = wrap_text(st.get("body",""), max_chars=14)
            y_offset = box_y + 52
            for j, ln in enumerate(body_lines[:4]):
                parts.append(f'<text x="{box_x+15}" y="{y_offset}" fill="#d2d2d7" font-size="13" font-weight="400">{html.escape(ln)}</text>')
                y_offset += 18
    # ===== 下方分支(反模式 + 军规) =====
    if bot:
        bot_gap = (main_x1 - main_x0 - 80) / (len(bot) + 1)
        for i, it in enumerate(bot):
            anchor_x = main_x0 + 40 + bot_gap * (i + 1)
            angle_deg = -25  # 朝右下
            import math
            rad = math.radians(-angle_deg)
            line_end_x = anchor_x + line_len * math.cos(rad)
            line_end_y = main_y + line_len * math.sin(rad)
            box_x = line_end_x - box_w  # 文字块朝左,右边缘对齐斜线终点
            box_y = line_end_y
            c = "#ff9f0a" if it["type"] == "army" else "#ff453a"
            # 斜线
            parts.append(f'<line x1="{anchor_x}" y1="{main_y}" x2="{line_end_x}" y2="{line_end_y}" stroke="{c}" stroke-width="2.5" stroke-dasharray="6 4"/>')
            # 圆点
            parts.append(f'<circle cx="{anchor_x}" cy="{main_y}" r="9" fill="{c}" stroke="#fff" stroke-width="2"/>')
            # 文字块(半透明填色)
            parts.append(f'<rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" rx="14" ry="14" fill="{c}" fill-opacity="0.06" stroke="{c}" stroke-opacity="0.3" stroke-width="1"/>')
            # tag 徽章(左上角)
            tag_color = "#ff9f0a" if it["type"] == "army" else "#ff453a"
            parts.append(f'<rect x="{box_x+15}" y="{box_y+12}" width="55" height="20" rx="6" fill="{tag_color}"/>')
            parts.append(f'<text x="{box_x+42}" y="{box_y+27}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">{html.escape(it["tag"])}</text>')
            # body 多行
            body_lines = wrap_text(it["short"], max_chars=14)
            y_offset = box_y + 52
            for j, ln in enumerate(body_lines[:4]):
                parts.append(f'<text x="{box_x+15}" y="{y_offset}" fill="#d2d2d7" font-size="13" font-weight="400">{html.escape(ln)}</text>')
                y_offset += 18
    svg = f'<svg id="fishSVG" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:auto">{"".join(parts)}</svg>'
    return svg


def detail_html(sop):
    parts = []
    if sop.get("intro"):
        parts.append(f'<div class="sopIntro">{html.escape(sop["intro"])}</div>')
    parts.append('<div class="secTitle">📋 完整步骤</div>')
    for st in sop["steps"]:
        parts.append(f'<div class="stepCard"><div class="stepN">{st.get("n","")}</div><div class="stepBody"><div class="stepT">{html.escape(st["title"])}</div><div class="stepD">{html.escape(st.get("body",""))}</div></div></div>')
    if sop.get("keyrules"):
        parts.append('<div class="secTitle">🟧 核心军规</div>')
        for r in sop["keyrules"]:
            parts.append(f'<div class="armyCard">{html.escape(r)}</div>')
    if sop.get("antipatterns"):
        parts.append('<div class="secTitle">🔴 反模式(别踩)</div>')
        for ap in sop["antipatterns"]:
            parts.append(f'<div class="warnCard">{html.escape(ap)}</div>')
    parts.append('<div class="secTitle">✅ 适用边界</div>')
    for u in sop.get("usewhen", []):
        parts.append(f'<div class="okCard">✅ 用：{html.escape(u)}</div>')
    for d in sop.get("dontuse", []):
        parts.append(f'<div class="badCard">❌ 不用：{html.escape(d)}</div>')
    return "\n".join(parts)


html_out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOP 鱼骨图学习 · 企业 AI 落地</title>
<style>
:root {{
  --bg:#000; --bg2:#0a0a0a; --glass:rgba(22,22,23,.72);
  --line:rgba(255,255,255,.08); --line2:rgba(255,255,255,.14);
  --txt:#f5f5f7; --txt2:#d2d2d7; --dim:#86868b; --dim2:#6e6e73; --dim3:#48484a;
  --blue:#2997ff; --blue2:#4cc2ff;
  --orange:#ff9f0a; --green:#30d158; --red:#ff453a;
  --ease:cubic-bezier(.32,.72,0,1);
  --radius-lg:22px; --radius-md:14px; --radius-sm:9px;
}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html,body{{height:100%;overflow-x:hidden;background:var(--bg)}}
body{{color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","PingFang SC","Helvetica Neue",sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.005em}}

#bar{{position:sticky;top:0;left:0;right:0;height:48px;z-index:30;display:flex;align-items:center;gap:10px;padding:0 22px;background:rgba(0,0,0,.6);-webkit-backdrop-filter:saturate(180%) blur(28px);backdrop-filter:saturate(180%) blur(28px);border-bottom:.5px solid var(--line);font-size:14px;font-weight:500;letter-spacing:-.01em}}
.logo{{font-size:14px;font-weight:600;color:var(--txt);white-space:nowrap;margin-right:6px}}
.logo i{{color:var(--dim);font-weight:400;font-style:normal;margin-left:6px}}
.back{{color:var(--dim);text-decoration:none;font-size:13px;margin-left:auto;transition:.2s var(--ease)}}
.back:hover{{color:var(--txt)}}

#hero{{padding:64px 5vw 24px}}
#hero h1{{font-size:clamp(48px,6vw,88px);font-weight:600;letter-spacing:-.045em;line-height:1.05;margin:0;background:linear-gradient(180deg,#f5f5f7 0%,#a1a1a6 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
#hero .sub{{font-size:17px;color:var(--dim);margin-top:14px;font-weight:400;line-height:1.5;max-width:780px}}

#picker{{padding:24px 5vw 12px;display:flex;flex-wrap:wrap;gap:8px;border-bottom:.5px solid var(--line);background:rgba(0,0,0,.4);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);position:sticky;top:48px;z-index:20}}
.chip{{padding:8px 14px;border-radius:980px;border:.5px solid var(--line);background:rgba(255,255,255,.04);font-size:13px;font-weight:500;color:var(--txt2);cursor:pointer;transition:.2s var(--ease);font-family:inherit}}
.chip:hover{{background:rgba(255,255,255,.1);color:var(--txt)}}
.chip.act{{background:var(--blue);color:#fff;border-color:var(--blue)}}

#main{{padding:32px 5vw 80px;display:grid;grid-template-columns:minmax(0,1fr) 420px;gap:32px;max-width:1400px;margin:0 auto}}
@media(max-width:1100px){{#main{{grid-template-columns:1fr}}}}

#fishbone{{background:rgba(22,22,23,.5);border:.5px solid var(--line);border-radius:var(--radius-lg);padding:32px 24px;overflow:hidden}}
#fishbone h2{{font-size:24px;font-weight:600;letter-spacing:-.02em;margin-bottom:6px;color:var(--txt)}}
#fishbone .fishSub{{font-size:13px;color:var(--dim);margin-bottom:18px}}
.sopNum{{color:var(--blue);font-weight:700;margin-right:8px}}
#fishSvg svg{{width:100% !important;height:auto !important;display:block}}

#detail{{position:sticky;top:140px;align-self:start;max-height:calc(100vh - 160px);overflow-y:auto;background:rgba(22,22,23,.5);border:.5px solid var(--line);border-radius:var(--radius-lg);padding:28px;-webkit-overflow-scrolling:touch}}
#detail::-webkit-scrollbar{{width:6px}}
#detail::-webkit-scrollbar-thumb{{background:var(--line2);border-radius:3px}}
.sopIntro{{font-size:14px;color:var(--txt2);line-height:1.7;padding:0 0 20px;border-bottom:.5px solid var(--line);margin-bottom:20px}}
.secTitle{{font-size:12px;color:var(--dim3);font-weight:600;letter-spacing:.08em;margin:20px 0 12px;text-transform:uppercase}}
.secTitle:first-of-type{{margin-top:0}}
.stepCard{{display:flex;gap:14px;padding:14px;background:rgba(41,151,255,.06);border:.5px solid rgba(41,151,255,.18);border-radius:var(--radius-md);margin-bottom:10px}}
.stepN{{flex:0 0 32px;height:32px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700}}
.stepBody{{flex:1;min-width:0}}
.stepT{{font-size:14px;font-weight:600;color:var(--txt);margin-bottom:6px}}
.stepD{{font-size:12.5px;color:var(--dim);line-height:1.65}}
.armyCard{{padding:12px 14px;background:rgba(255,159,10,.08);border:.5px solid rgba(255,159,10,.25);border-radius:var(--radius-md);color:var(--txt2);font-size:13px;line-height:1.6;margin-bottom:8px}}
.warnCard{{padding:12px 14px;background:rgba(255,69,58,.08);border:.5px solid rgba(255,69,58,.22);border-radius:var(--radius-md);color:var(--txt2);font-size:13px;line-height:1.6;margin-bottom:8px}}
.okCard{{padding:10px 14px;background:rgba(48,209,88,.06);border:.5px solid rgba(48,209,88,.18);border-radius:var(--radius-sm);color:var(--txt2);font-size:12.5px;line-height:1.6;margin-bottom:6px}}
.badCard{{padding:10px 14px;background:rgba(255,69,58,.06);border:.5px solid rgba(255,69,58,.18);border-radius:var(--radius-sm);color:var(--txt2);font-size:12.5px;line-height:1.6;margin-bottom:6px}}

#legend{{display:flex;gap:18px;padding:14px 5vw;flex-wrap:wrap;font-size:12px;color:var(--dim);border-top:.5px solid var(--line);margin-top:24px}}
#legend span{{display:inline-flex;align-items:center;gap:6px}}
#legend i{{display:inline-block;width:8px;height:8px;border-radius:50%}}

@media(max-width:700px){{
  #bar{{height:auto;padding:8px 14px;flex-wrap:wrap}}
  .logo i{{display:none}}
  .back{{order:99}}
  #hero{{padding:32px 20px 18px}}
  #hero h1{{font-size:42px}}
  .hero .sub{{font-size:14px}}
  #picker{{padding:14px 16px;gap:6px;top:0;position:relative}}
  .chip{{padding:7px 11px;font-size:12px}}
  #main{{padding:16px 14px 60px;gap:18px}}
  #fishbone{{padding:16px;border-radius:14px}}
  #detail{{position:relative;top:0;max-height:none;padding:18px}}
}}
</style>
</head>
<body>

<div id="bar">
  <div class="logo">🪢 SOP 鱼骨图 <i>企业 AI 落地 8 套流程</i></div>
  <a class="back" href="atlas.html">← 全景知识树</a>
</div>

<div id="hero">
  <h1>SOP 鱼骨图学习</h1>
  <div class="sub">8 套接单/落地全流程,可视化呈现「步骤 + 军规 + 反模式」三件套,点 SOP 切换,右侧看完整内容。</div>
</div>

<div id="picker">
{''.join(f'<button class="chip" data-n="{s["num"]}">SOP {s["num"]} · {html.escape(s["title"].split("·")[1].strip()[:24])}</button>' for s in SOPS)}
</div>

<div id="main">
  <div id="fishbone">
    <h2><span class="sopNum" id="fNum">SOP 1</span><span id="fTitle">{html.escape(SOPS[0]["title"].split("·")[1].strip())}</span></h2>
    <div class="fishSub">上方 = 主线步骤 · 下方 = 军规 + 反模式 · 点右侧详情看完整内容</div>
    <div id="fishSvg">{render_fishbone_svg(SOPS[0])}</div>
  </div>
  <div id="detail">{detail_html(SOPS[0])}</div>
</div>

<div id="legend">
  <span><i style="background:var(--blue)"></i>主轴步骤</span>
  <span><i style="background:var(--orange)"></i>核心军规</span>
  <span><i style="background:var(--red)"></i>反模式</span>
  <span><i style="background:var(--green)"></i>适用边界</span>
</div>

<script>
var SOPS = {json.dumps(SOPS, ensure_ascii=False)};

// JS 版 SVG 鱼骨图(完整单图,viewBox 1400x900)
function fishboneSvg(sop, W, H){{
  W = W || 1400; H = H || 900;
  var steps = sop.steps || [];
  var aps = sop.antipatterns || [];
  var rules = sop.keyrules || [];
  var bot = [];
  aps.slice(0,3).forEach(function(a){{ bot.push({{type:'warn', short:a, tag:'反模式'}}); }});
  rules.slice(0,3).forEach(function(r){{ bot.push({{type:'army', short:r, tag:'军规'}}); }});
  var esc = function(s){{ return String(s||'').replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>'); }};
  // 文字换行
  function wrapText(t, mc){{
    t = String(t||'').trim();
    if(t.length <= mc) return [t];
    var lines = [];
    while(t.length > mc){{
      var cut = t.substring(0, mc);
      var idx = -1;
      for(var i=cut.length-1; i>=Math.max(0, cut.length-4); i--){{
        if('，。、 ；:：?？!！ '.indexOf(cut[i]) >= 0){{ idx = i; break; }}
      }}
      if(idx >= 0) cut = t.substring(0, idx+1);
      else cut = t.substring(0, mc);
      lines.push(cut);
      t = t.substring(cut.length);
    }}
    if(t) lines.push(t);
    return lines;
  }}
  var mainY = H / 2;
  var mL = 60, mR = 60;
  var mainX0 = mL, mainX1 = W - mR;
  var parts = [];
  parts.push('<line x1="'+mainX0+'" y1="'+mainY+'" x2="'+mainX1+'" y2="'+mainY+'" stroke="#5a5a5f" stroke-width="3"/>');
  parts.push('<circle cx="'+mainX0+'" cy="'+mainY+'" r="11" fill="#5a5a5f" stroke="#fff" stroke-width="2.5"/>');
  parts.push('<text x="'+(mainX0+18)+'" y="'+(mainY+6)+'" fill="#86868b" font-size="18" font-weight="600">起点</text>');
  parts.push('<polygon points="'+(mainX1+5)+','+mainY+' '+(mainX1-22)+','+(mainY-18)+' '+(mainX1-22)+','+(mainY+18)+'" fill="#5a5a5f"/>');
  var boxW = 220, boxH = 130;
  var lineLen = 90;
  function deg2rad(d){{ return d * Math.PI / 180; }}
  // 上方步骤
  if(steps.length){{
    var stepGap = (mainX1 - mainX0 - 80) / (steps.length + 1);
    for(var i=0; i<steps.length; i++){{
      var st = steps[i];
      var anchorX = mainX0 + 40 + stepGap * (i + 1);
      var rad = deg2rad(25);
      var lineEndX = anchorX + lineLen * Math.cos(rad);
      var lineEndY = mainY - lineLen * Math.sin(rad);
      var boxX = lineEndX;
      var boxY = lineEndY - boxH;
      parts.push('<line x1="'+anchorX+'" y1="'+mainY+'" x2="'+lineEndX+'" y2="'+lineEndY+'" stroke="#2997ff" stroke-width="2.5"/>');
      parts.push('<circle cx="'+anchorX+'" cy="'+mainY+'" r="10" fill="#2997ff" stroke="#fff" stroke-width="2.5"/>');
      parts.push('<rect x="'+boxX+'" y="'+boxY+'" width="'+boxW+'" height="'+boxH+'" rx="14" ry="14" fill="#2997ff" fill-opacity="0.06" stroke="#2997ff" stroke-opacity="0.3" stroke-width="1"/>');
      parts.push('<circle cx="'+(boxX+22)+'" cy="'+(boxY+22)+'" r="14" fill="#2997ff"/>');
      parts.push('<text x="'+(boxX+22)+'" y="'+(boxY+27)+'" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">'+(i+1)+'</text>');
      parts.push('<text x="'+(boxX+44)+'" y="'+(boxY+27)+'" fill="#2997ff" font-size="15" font-weight="700">'+esc(st.title||'').slice(0,16)+'</text>');
      var bodyLines = wrapText(st.body||'', 14);
      var yOff = boxY + 52;
      for(var j=0; j<Math.min(bodyLines.length,4); j++){{
        parts.push('<text x="'+(boxX+15)+'" y="'+yOff+'" fill="#d2d2d7" font-size="13" font-weight="400">'+esc(bodyLines[j])+'</text>');
        yOff += 18;
      }}
    }}
  }}
  // 下方分支
  if(bot.length){{
    var botGap = (mainX1 - mainX0 - 80) / (bot.length + 1);
    for(var i=0; i<bot.length; i++){{
      var it = bot[i];
      var anchorX = mainX0 + 40 + botGap * (i + 1);
      var rad = deg2rad(25);
      var lineEndX = anchorX + lineLen * Math.cos(rad);
      var lineEndY = mainY + lineLen * Math.sin(rad);
      var boxX = lineEndX - boxW;
      var boxY = lineEndY;
      var c = it.type==='army' ? '#ff9f0a' : '#ff453a';
      parts.push('<line x1="'+anchorX+'" y1="'+mainY+'" x2="'+lineEndX+'" y2="'+lineEndY+'" stroke="'+c+'" stroke-width="2.5" stroke-dasharray="6 4"/>');
      parts.push('<circle cx="'+anchorX+'" cy="'+mainY+'" r="9" fill="'+c+'" stroke="#fff" stroke-width="2"/>');
      parts.push('<rect x="'+boxX+'" y="'+boxY+'" width="'+boxW+'" height="'+boxH+'" rx="14" ry="14" fill="'+c+'" fill-opacity="0.06" stroke="'+c+'" stroke-opacity="0.3" stroke-width="1"/>');
      parts.push('<rect x="'+(boxX+15)+'" y="'+(boxY+12)+'" width="55" height="20" rx="6" fill="'+c+'"/>');
      parts.push('<text x="'+(boxX+42)+'" y="'+(boxY+27)+'" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">'+it.tag+'</text>');
      var bodyLines = wrapText(it.short||'', 14);
      var yOff = boxY + 52;
      for(var j=0; j<Math.min(bodyLines.length,4); j++){{
        parts.push('<text x="'+(boxX+15)+'" y="'+yOff+'" fill="#d2d2d7" font-size="13" font-weight="400">'+esc(bodyLines[j])+'</text>');
        yOff += 18;
      }}
    }}
  }}
  return '<svg id="fishSVG" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:auto">'+parts.join('')+'</svg>';
}}

function detailHtml(sop){{
  var esc = function(s){{ return String(s||'').replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>'); }};
  var h = '';
  if(sop.intro) h += '<div class="sopIntro">'+esc(sop.intro)+'</div>';
  h += '<div class="secTitle">📋 完整步骤</div>';
  (sop.steps||[]).forEach(function(st){{
    h += '<div class="stepCard"><div class="stepN">'+(st.n||'')+'</div><div class="stepBody"><div class="stepT">'+esc(st.title)+'</div><div class="stepD">'+esc(st.body||'')+'</div></div></div>';
  }});
  if(sop.keyrules && sop.keyrules.length){{
    h += '<div class="secTitle">🟧 核心军规</div>';
    sop.keyrules.forEach(function(r){{ h += '<div class="armyCard">'+esc(r)+'</div>'; }});
  }}
  if(sop.antipatterns && sop.antipatterns.length){{
    h += '<div class="secTitle">🔴 反模式(别踩)</div>';
    sop.antipatterns.forEach(function(a){{ h += '<div class="warnCard">'+esc(a)+'</div>'; }});
  }}
  h += '<div class="secTitle">✅ 适用边界</div>';
  (sop.usewhen||[]).forEach(function(u){{ h += '<div class="okCard">✅ 用：'+esc(u)+'</div>'; }});
  (sop.dontuse||[]).forEach(function(d){{ h += '<div class="badCard">❌ 不用：'+esc(d)+'</div>'; }});
  return h;
}}

function pick(n){{
  var sop = SOPS[parseInt(n)-1];
  if(!sop) return;
  document.getElementById('fNum').textContent = 'SOP '+sop.num;
  document.getElementById('fTitle').textContent = sop.title.split('·')[1].trim();
  // viewBox 固定 1400x900,SVG 等比缩放
  document.getElementById('fishSvg').innerHTML = fishboneSvg(sop, 1400, 900);
  document.getElementById('detail').innerHTML = detailHtml(sop);
  document.querySelectorAll('.chip').forEach(function(b){{ b.classList.toggle('act', b.dataset.n===sop.num); }});
}}

document.querySelectorAll('.chip').forEach(function(b){{
  b.addEventListener('click', function(){{ pick(this.dataset.n); document.getElementById('detail').scrollIntoView({{behavior:'smooth',block:'start'}}); }});
}});
document.querySelector('.chip[data-n="1"]').classList.add('act');
// 首屏渲染鱼骨图(viewBox 固定 1400x900,等比缩放)
document.getElementById('fishSvg').innerHTML = fishboneSvg(SOPS[0], 1400, 900);
// resize 不重画,SVG 自动等比缩放
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(html_out)
print(f"✅ 生成 {OUT}")
print(f"   大小: {os.path.getsize(OUT):,} B")
for s in SOPS:
    print(f"   SOP{s['num']}: {len(s['steps'])} 步 / {len(s.get('keyrules',[]))} 军规 / {len(s.get('antipatterns',[]))} 反模式")
