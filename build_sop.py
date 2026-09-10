# -*- coding: utf-8 -*-
"""鱼骨图 SOP 学习页 · v3 终极版
- 鱼骨图用 SVG 但 viewBox 设为 0 0 容器宽 容器高,JS 渲染后动态改
- 8 SOP 结构化数据
- 苹果风 UI / 黑底 / 大留白
"""
import json, os, html

BASE = "/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库"
JSON_PATH = "/tmp/sop_data.json"
OUT = "/Users/tkdesign/growth-system-panel/sop.html"

data = json.load(open(JSON_PATH, encoding="utf-8"))
SOPS = data


# ============== SVG 鱼骨图 · 用百分比坐标(避开绝对像素问题) ==============
def render_fishbone_svg(sop, W=800, H=440):
    """画鱼骨图:viewBox=0 0 W H,所有坐标都按 W/H 百分比算"""
    steps = sop["steps"]
    aps = sop.get("antipatterns", [])
    rules = sop.get("keyrules", [])
    # 上方步骤
    top_n = max(len(steps), 1)
    bot = []
    for ap in aps[:3]: bot.append({"type":"warn", "short":ap[:55]})
    for r in rules[:3]: bot.append({"type":"army", "short":r[:55]})
    bot_n = max(len(bot), 1)
    # 主轴 y
    main_y = H * 0.55
    main_x0 = W * 0.05
    main_x1 = W * 0.92
    parts = []
    # 主轴
    parts.append(f'<line x1="{main_x0}" y1="{main_y}" x2="{main_x1}" y2="{main_y}" stroke="#48484a" stroke-width="3"/>')
    parts.append(f'<polygon points="{main_x1},{main_y} {main_x1-18},{main_y-10} {main_x1-18},{main_y+10}" fill="#48484a"/>')
    # 鱼骨名
    parts.append(f'<text x="{main_x0-8}" y="{main_y+5}" text-anchor="end" fill="#86868b" font-size="13" font-weight="600" font-family="-apple-system,sans-serif">起点 →</text>')
    # 步骤节点
    if steps:
        step_w = (main_x1 - main_x0) / (len(steps) + 1)
        for i, st in enumerate(steps):
            sx = main_x0 + step_w * (i + 1)
            # 斜线向上到 title 位置
            # title 位置: y = main_y - 130
            tx = sx + 50  # 斜线右移一点
            ty = main_y - 130
            # 斜线
            parts.append(f'<line x1="{sx}" y1="{main_y}" x2="{tx}" y2="{ty}" stroke="#2997ff" stroke-width="2.5"/>')
            # 圆点
            parts.append(f'<circle cx="{sx}" cy="{main_y}" r="9" fill="#2997ff" stroke="#fff" stroke-width="2.5"/>')
            # 编号 + 标题
            title = html.escape(st["title"][:22])
            parts.append(f'<text x="{tx+6}" y="{ty-8}" text-anchor="start" fill="#2997ff" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">{i+1}. {title}</text>')
            # body 文字
            body = html.escape(st.get("body","")[:90])
            parts.append(f'<text x="{tx+6}" y="{ty+12}" text-anchor="start" fill="#d2d2d7" font-size="11.5" font-weight="400" font-family="-apple-system,sans-serif">{body}</text>')
    # 反模式 + 军规 节点(下方)
    if bot:
        bw = (main_x1 - main_x0) / (len(bot) + 1)
        for i, it in enumerate(bot):
            sx = main_x0 + bw * (i + 1)
            ty = main_y + 130
            tx = sx - 50  # 斜线左移
            c = "#ff9f0a" if it["type"] == "army" else "#ff453a"
            tag = "军规" if it["type"] == "army" else "反模式"
            # 斜线
            parts.append(f'<line x1="{sx}" y1="{main_y}" x2="{tx}" y2="{ty}" stroke="{c}" stroke-width="2" stroke-dasharray="5 3"/>')
            # 圆点
            parts.append(f'<circle cx="{sx}" cy="{main_y}" r="7" fill="{c}" stroke="#fff" stroke-width="2"/>')
            # tag
            parts.append(f'<text x="{tx-6}" y="{ty-8}" text-anchor="end" fill="{c}" font-size="13" font-weight="700" font-family="-apple-system,sans-serif">{tag}</text>')
            # text
            short = html.escape(it["short"])
            parts.append(f'<text x="{tx-6}" y="{ty+12}" text-anchor="end" fill="#d2d2d7" font-size="11.5" font-weight="400" font-family="-apple-system,sans-serif">{short}</text>')
    svg = '<svg id="fishSVG" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:auto">' + "".join(parts) + "</svg>"
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

// JS 版 SVG 鱼骨图
function fishboneSvg(sop, W, H){{
  var steps = sop.steps || [];
  var aps = sop.antipatterns || [];
  var rules = sop.keyrules || [];
  var bot = [];
  aps.slice(0,3).forEach(function(a){{ bot.push({{type:'warn', short:a.slice(0,55)}}); }});
  rules.slice(0,3).forEach(function(r){{ bot.push({{type:'army', short:r.slice(0,55)}}); }});
  var esc = function(s){{ return String(s||'').replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>'); }};
  var mainY = H * 0.55;
  var mainX0 = W * 0.05;
  var mainX1 = W * 0.92;
  var parts = [];
  parts.push('<line x1="'+mainX0+'" y1="'+mainY+'" x2="'+mainX1+'" y2="'+mainY+'" stroke="#48484a" stroke-width="3"/>');
  parts.push('<polygon points="'+mainX1+','+mainY+' '+(mainX1-18)+','+(mainY-10)+' '+(mainX1-18)+','+(mainY+10)+'" fill="#48484a"/>');
  parts.push('<text x="'+(mainX0-8)+'" y="'+(mainY+5)+'" text-anchor="end" fill="#86868b" font-size="13" font-weight="600" font-family="-apple-system,sans-serif">起点 →</text>');
  if(steps.length){{
    var stepW = (mainX1 - mainX0) / (steps.length + 1);
    for(var i=0; i<steps.length; i++){{
      var st = steps[i];
      var sx = mainX0 + stepW*(i+1);
      var tx = sx + 50;
      var ty = mainY - 130;
      parts.push('<line x1="'+sx+'" y1="'+mainY+'" x2="'+tx+'" y2="'+ty+'" stroke="#2997ff" stroke-width="2.5"/>');
      parts.push('<circle cx="'+sx+'" cy="'+mainY+'" r="9" fill="#2997ff" stroke="#fff" stroke-width="2.5"/>');
      var title = esc(st.title||'').slice(0,22);
      parts.push('<text x="'+(tx+6)+'" y="'+(ty-8)+'" text-anchor="start" fill="#2997ff" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">'+(i+1)+'. '+title+'</text>');
      var body = esc(st.body||'').slice(0,90);
      parts.push('<text x="'+(tx+6)+'" y="'+(ty+12)+'" text-anchor="start" fill="#d2d2d7" font-size="11.5" font-family="-apple-system,sans-serif">'+body+'</text>');
    }}
  }}
  if(bot.length){{
    var bw = (mainX1 - mainX0) / (bot.length + 1);
    for(var j=0; j<bot.length; j++){{
      var it = bot[j];
      var sx = mainX0 + bw*(j+1);
      var tx = sx - 50;
      var ty = mainY + 130;
      var c = it.type==='army' ? '#ff9f0a' : '#ff453a';
      var tag = it.type==='army' ? '军规' : '反模式';
      parts.push('<line x1="'+sx+'" y1="'+mainY+'" x2="'+tx+'" y2="'+ty+'" stroke="'+c+'" stroke-width="2" stroke-dasharray="5 3"/>');
      parts.push('<circle cx="'+sx+'" cy="'+mainY+'" r="7" fill="'+c+'" stroke="#fff" stroke-width="2"/>');
      parts.push('<text x="'+(tx-6)+'" y="'+(ty-8)+'" text-anchor="end" fill="'+c+'" font-size="13" font-weight="700" font-family="-apple-system,sans-serif">'+tag+'</text>');
      parts.push('<text x="'+(tx-6)+'" y="'+(ty+12)+'" text-anchor="end" fill="#d2d2d7" font-size="11.5" font-family="-apple-system,sans-serif">'+esc(it.short)+'</text>');
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
  // SVG 1:1: viewBox 宽高 = SVG 实际像素宽高
  var container = document.getElementById('fishSvg');
  var w = container.clientWidth || 800;
  var h = Math.round(w * 440 / 800);
  container.innerHTML = fishboneSvg(sop, w, h);
  document.getElementById('detail').innerHTML = detailHtml(sop);
  document.querySelectorAll('.chip').forEach(function(b){{ b.classList.toggle('act', b.dataset.n===sop.num); }});
}}

document.querySelectorAll('.chip').forEach(function(b){{
  b.addEventListener('click', function(){{ pick(this.dataset.n); document.getElementById('detail').scrollIntoView({{behavior:'smooth',block:'start'}}); }});
}});
document.querySelector('.chip[data-n="1"]').classList.add('act');
// 首次加载 1:1 缩放
setTimeout(function(){{
  var c = document.getElementById('fishSvg');
  var w = c.clientWidth || 800;
  var h = Math.round(w * 440 / 800);
  c.innerHTML = fishboneSvg(SOPS[0], w, h);
}}, 50);
window.addEventListener('resize', function(){{
  var c = document.getElementById('fishSvg');
  var svg = c.querySelector('svg');
  if(!svg) return;
  var w = c.clientWidth;
  var h = Math.round(w * 440 / 800);
  // 当前 SOP 重画
  var n = document.querySelector('.chip.act');
  if(n) pick(n.dataset.n);
  else {{ c.innerHTML = fishboneSvg(SOPS[0], w, h); }}
}});
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(html_out)
print(f"✅ 生成 {OUT}")
print(f"   大小: {os.path.getsize(OUT):,} B")
for s in SOPS:
    print(f"   SOP{s['num']}: {len(s['steps'])} 步 / {len(s.get('keyrules',[]))} 军规 / {len(s.get('antipatterns',[]))} 反模式")
