/* ============================================================
 * 项目体检 v3：填项目情况 → 派 Hermes agent 带完整知识库真推理 → 输出开工方案
 * 数据源：agent 完整读 23 载体选型 + 24 零件装配 + 25 工程全景（不再前端 if-else）
 * 通道：/api/ask（hermes chat -s ai-architect，带记忆/知识库）→ /api/ask_result 轮询
 * 创建：2026-09-09 v3 重写（原 v2 纯前端规则引擎被否：浅层/无后台/无溯源）
 * ============================================================ */

/* ---------- 辅助字段（可选，选了拼进 prompt，不选交给 agent 从文本推断） ---------- */
var HC_FIELDS = {
  sens:   { label:"数据敏感度", opts:["不敏感/公开信息","PII 隐私数据","商业机密","金融/医疗/政府级"] },
  it:     { label:"客户 IT 能力", opts:["没有，越省事越好","半懂，能按文档操作","有专职 IT/研发"] },
  budget: { label:"预算档位", opts:["¥3-8k 入门","¥8-30k 增长型","¥80-300k 企业级","不确定"] }
};

/* ---------- 表单：主角是「项目情况」自由文本，3 个字段做辅助 ---------- */
function hcStepHtml(){
  var h = '<div style="display:flex;flex-direction:column;gap:12px;max-height:calc(100vh - 220px);overflow-y:auto;padding:4px 2px">';
  h += '<div style="background:#eef7f1;border:1px solid #d5e8dc;border-radius:12px;padding:10px 14px;font-size:12.5px;line-height:1.7;color:#2c5a46">'
     + '💡 把项目情况一句话讲清楚（谁用、做什么、数据在哪、规模多大、什么预算），Hermes 会完整读三份方法论文档（载体选型/零件装配/工程全景）后，给你一份能落地的 <b>开工方案</b>：推荐载体 + 必装零件 + 工程阶段 + 报价。约 1 分钟。</div>';
  h += '<textarea id="hcInput" rows="6" placeholder="例：长春 8 人货代公司，老板想花 5 万上 AI 自动找俄罗斯客户、自动回消息，要求全自动群发，自己不懂技术、没有 IT，数据是客户联系方式（PII），希望越快上线越好" style="width:100%;box-sizing:border-box;border:1px solid #d8d2c0;border-radius:12px;padding:12px;font-size:13px;line-height:1.7;font-family:inherit;resize:vertical;background:#fdfcf8"></textarea>';
  // 3 个辅助字段
  h += '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">';
  ['sens','it','budget'].forEach(function(k){
    var f = HC_FIELDS[k];
    h += '<div style="background:#faf7ef;border:1px solid #ece5d3;border-radius:12px;padding:9px 11px">';
    h += '<div style="font-weight:700;font-size:12px;color:#2c3a33;margin-bottom:6px">' + f.label + ' <span style="font-weight:400;color:#aaa;font-size:10px">(选填)</span></div>';
    f.opts.forEach(function(o, oi){
      h += '<label style="display:flex;align-items:center;gap:6px;padding:4px 6px;border-radius:7px;cursor:pointer;font-size:11.5px;color:#555" onmouseover="this.style.background=\'#f0f5f1\'" onmouseout="this.style.background=\'transparent\'">';
      h += '<input type="radio" name="hcf_' + k + '" value="' + oi + '" style="accent-color:var(--green)">';
      h += '<span>' + esc(o) + '</span></label>';
    });
    h += '</div>';
  });
  h += '</div>';
  h += '<div style="display:flex;gap:10px;justify-content:flex-end">';
  h += '<button onclick="hcReset()" style="padding:10px 18px;border-radius:11px;border:1px solid #d8d2c0;background:transparent;color:#666;cursor:pointer;font-size:13px">清空</button>';
  h += '<button onclick="hcRun()" style="padding:10px 22px;border-radius:11px;border:0;background:linear-gradient(135deg,#1e5a44,#2a7a55);color:#fff;cursor:pointer;font-weight:700;font-size:14px;box-shadow:0 2px 10px rgba(30,90,68,.28)">🩺 开始体检（派 Hermes 真推理）</button>';
  h += '</div></div>';
  return h;
}
function hcReset(){
  var t = document.getElementById('hcInput'); if(t) t.value = '';
  ['sens','it','budget'].forEach(function(k){
    var radios = document.querySelectorAll('#mBody input[name="hcf_' + k + '"]');
    for(var i=0;i<radios.length;i++) radios[i].checked = false;
  });
}

/* ---------- 提交：拼 prompt → /api/ask → 轮询 ---------- */
function hcRun(){
  var inp = document.getElementById('hcInput');
  var txt = (inp && inp.value || '').trim();
  if(!txt){ alert('先把项目情况填上'); return; }
  // 收集辅助字段
  var aux = [];
  ['sens','it','budget'].forEach(function(k){
    var sel = document.querySelector('#mBody input[name="hcf_' + k + '"]:checked');
    if(sel){ aux.push(HC_FIELDS[k].label + '：' + HC_FIELDS[k].opts[parseInt(sel.value,10)]); }
  });
  var auxTxt = aux.length ? ('\n已选辅助信息：' + aux.join(' / ')) : '';
  // 渲染「思考中」占位
  document.getElementById('mBody').innerHTML = '<div style="padding:40px 20px;text-align:center">'
    + '<div style="font-size:34px;margin-bottom:12px">🩺</div>'
    + '<div style="font-size:14px;font-weight:700;color:#2c3a33;margin-bottom:6px">Hermes 正在完整读三份方法论文档并推导…</div>'
    + '<div style="font-size:12px;color:#999">载体选型 + 零件装配 + 工程全景 → 约 1 分钟，别关窗口</div>'
    + '<div id="hcStatus" style="margin-top:14px;font-size:12px;color:#888"></div></div>';
  document.getElementById('mSub').innerHTML = '<span style="color:var(--muted);font-size:12px">派 Hermes agent 真推理 · 带 23/24/25 完整知识库</span>';

  // 组织成体检指令 —— agent 会完整读 23/24/25 文档，结论全部有溯源
  var q = '你是王昕「企业 AI 落地知识系统」的项目体检引擎，现在给一个新项目做开工前问诊。\n\n'
    + '先完整读这三份知识库文档（经过验证的成熟方法论，一切结论以它们为依据，不要凭空想象）：\n'
    + '1. /Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/成长系统/23_交付载体怎么选_v1.md（7种载体+决策树+档位报价）\n'
    + '2. /Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/成长系统/24_项目零件装配清单_v1.md（90+零件+6步判定法+3个真实项目解剖）\n'
    + '3. /Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/成长系统/25_程序全流程工程全景_v1.md（12阶段+9门禁）\n\n'
    + '【客户项目情况】\n' + txt + auxTxt + '\n\n'
    + '【输出要求】基于这三份文档，输出一份 markdown 格式的「项目开工方案」，必须包含 5 个部分：\n'
    + '1. **一句话结论**：载体 + 档位 + 一句话理由\n'
    + '2. **推荐载体**：走 23 的决策树，说清决策路径（数据能否上云→客户IT→业务流程→载体），并附一个真实案例\n'
    + '3. **必装零件清单**：走 24 的六步判定法，列出这个项目必须有的零件，每个零件标注触发条件（为什么这个项目必须有它）\n'
    + '4. **工程阶段定位**：按 25 全景，当前项目处在哪个阶段、接下来要过哪几个门禁\n'
    + '5. **档位报价建议**：按 23 的档位适配（STARTER ¥3-8k / 增长型 ¥8-30k / ENTERPRISE ¥80-300k）给报价结构\n\n'
    + '结论在前、理由在后，每个结论都要能追溯到这三份文档的哪一节。总长控制在 2000 字内，能压成表格就压成表格。';

  fetch('/api/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({q: q, max_turns: 8, max_len: 16000, max_q: 4000})})
    .then(function(r){ return r.json(); })
    .then(function(d){
      if(!d.ok){ document.getElementById('mBody').innerHTML = '<div style="color:#c0392b;font-size:13px;padding:20px">✗ ' + (d.error || '提交失败') + '</div>'; return; }
      pollHC(d.tid);
    })
    .catch(function(e){ document.getElementById('mBody').innerHTML = '<div style="color:#c0392b;font-size:13px;padding:20px">✗ 网络错误：' + esc(String(e)) + '</div>'; });
}

/* ---------- 轮询结果 ---------- */
function pollHC(tid){
  var tries = 0;
  var timer = setInterval(function(){
    tries++;
    fetch('/api/ask_result?tid=' + tid).then(function(r){ return r.json(); }).then(function(d){
      if(d.status === 'done'){
        clearInterval(timer);
        hcLast = { answer: d.answer || '' };
        renderHC(d.answer || '(空)');
      } else if(d.status === 'error'){
        clearInterval(timer);
        document.getElementById('mBody').innerHTML = '<div style="color:#c0392b;font-size:13px;padding:20px">✗ ' + esc(d.answer || 'agent 出错') + '</div>';
      } else if(tries > 30){
        clearInterval(timer);
        document.getElementById('mBody').innerHTML = '<div style="color:#c0392b;font-size:13px;padding:20px">✗ 等太久了（>2 分钟），刷新重试</div>';
      } else {
        var st = document.getElementById('hcStatus');
        if(st) st.textContent = '⏳ 第 ' + tries + ' 次轮询（每 4 秒一次）…';
      }
    }).catch(function(){ if(tries > 30){ clearInterval(timer); } });
  }, 4000);
}

/* ---------- 渲染方案卡（agent 返回 markdown，用 mdToHtml 渲染） ---------- */
function renderHC(answer){
  var h = '<div style="background:#163c31;border-radius:14px;padding:13px 16px;margin-bottom:12px">'
    + '<div style="font-size:11px;letter-spacing:.5px;color:rgba(255,255,255,.75)">🩺 项目开工方案 · Hermes 基于 23/24/25 三份文档真推理</div>'
    + '</div>';
  h += '<div style="max-height:calc(100vh - 280px);overflow-y:auto;padding:0 2px">'
    + '<div id="hcDoc" style="font-size:13.5px;line-height:1.85;color:#333">' + mdToHtml(answer) + '</div></div>';
  h += '<div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap;border-top:1px solid #eee;padding-top:12px">';
  h += '<button onclick="hcSaveResult()" style="padding:9px 16px;border-radius:10px;border:0;background:linear-gradient(135deg,#8a5a17,#c9962e);color:#fff;cursor:pointer;font-weight:700;font-size:13px">📌 存进 Obsidian</button>';
  h += '<button onclick="openHealthCheck()" style="padding:9px 16px;border-radius:10px;border:1px solid #d8d2c0;background:#fff;color:#444;cursor:pointer;font-size:13px">↩ 重新体检</button>';
  h += '<button onclick="closeM()" style="padding:9px 16px;border-radius:10px;border:1px solid #d8d2c0;background:#fff;color:#444;cursor:pointer;font-size:13px">关闭</button>';
  h += '</div>';
  document.getElementById('mBody').innerHTML = h;
  document.getElementById('mSub').innerHTML = '<span style="color:var(--muted);font-size:12px">Hermes agent 真推理 · 结论可追溯到 23/24/25 文档章节</span>';
}

var hcLast = null;
/* ---------- 保存方案到 Obsidian ---------- */
function hcSaveResult(){
  if(!hcLast){ alert('还没有体检结果'); return; }
  var md = '# 项目开工方案 · ' + new Date().toISOString().slice(0,10) + '\n\n' + (hcLast.answer || '');
  fetch('/api/save_doc', {
    method:'POST',
    headers:{ 'Content-Type':'application/json' },
    body: JSON.stringify({ folder:'项目库', name:'体检_' + new Date().toISOString().slice(0,10) + '_' + Date.now().toString(36), content: md })
  }).then(function(r){ return r.json(); }).then(function(d){
    alert(d && d.ok ? '✅ 已存进 Obsidian 项目库' : ('⚠️ ' + (d && d.error || '保存失败')));
  }).catch(function(){ alert('⚠️ 保存失败（服务未开/接口不可用）'); });
}

/* ---------- 入口 ---------- */
function openHealthCheck(){
  vlShowModal('🩺 项目体检 · 填项目情况出开工方案', hcStepHtml());
}
