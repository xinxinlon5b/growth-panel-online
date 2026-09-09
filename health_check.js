/* ============================================================
 * 项目体检向导 (E1 载体决策 + E2 零件装配 + E3 方案生成 v2)
 * 纯前端规则引擎: 回答 10 个问题 → 输出推荐载体 + 必装零件清单
 * 数据源: 24_项目零件装配清单_v1.md (6步推导法) + 23_交付载体怎么选_v1.md
 * 创建: 2026-09-09
 * ============================================================ */

/* ---------- 问题定义: 每题选项带 tags(影响载体) / parts(影响零件) ---------- */
var HC_QUESTIONS = [
  { q:"① 客户愿意把业务数据放到公有云吗？（合规/敏感度）", k:"cloud",
    opts:[
      { t:"愿意，上云没问题", tags:["cloud-ok"] },
      { t:"不愿意，数据敏感/合规要求不出域", tags:["cloud-no"] },
      { t:"部分可以，核心数据要留本地", tags:["cloud-hybrid"] }
    ]},
  { q:"② 客户有 IT 运维能力吗？（有人会部署/维护服务器吗）", k:"it",
    opts:[
      { t:"有专职 IT/研发", tags:["it-yes"] },
      { t:"没有，希望越省事越好", tags:["it-no"] },
      { t:"半懂，能按文档操作", tags:["it-mid"] }
    ]},
  { q:"③ 业务流程是「长尾多步推理/要调工具」还是「标准表单增删改查」？", k:"flow",
    opts:[
      { t:"长尾流程：多步推理/判断/调多个工具（客服、分析、助手类）", tags:["flow-agent"], parts:["ai"] },
      { t:"标准流程：填表/查数据/审批（ERP 增强类）", tags:["flow-crud"] },
      { t:"两者都有", tags:["flow-both"], parts:["ai"] }
    ]},
  { q:"④ 这系统挂了，客户业务损失有多大？", k:"critical",
    opts:[
      { t:"灾难级：一挂全公司停摆/直接巨额损失", parts:["crit-disaster"] },
      { t:"大：明显影响业务/客户体验", parts:["crit-high"] },
      { t:"小：内部用，挂了忍一会", parts:["crit-low"] },
      { t:"几乎零：demo/实验性质", parts:["crit-zero"] }
    ]},
  { q:"⑤ 预计峰值并发/数据量级？", k:"scale",
    opts:[
      { t:"高并发(>1000 QPS)或大数据(>1TB)", parts:["scale-high"] },
      { t:"中等（几十到几百人用）", parts:["scale-mid"] },
      { t:"低（几个人/内部小范围）", parts:["scale-low"] }
    ]},
  { q:"⑥ 数据里有什么敏感内容？", k:"sensitive",
    opts:[
      { t:"金融/医疗/政府级（极敏感）", parts:["sens-extreme"] },
      { t:"商业机密/客户隐私 PII", parts:["sens-pii"] },
      { t:"内部数据但不涉隐私", parts:["sens-int"] },
      { t:"基本无敏感（公开信息）", parts:["sens-none"] }
    ]},
  { q:"⑦ 一次错误操作/重复提交的代价？", k:"failure",
    opts:[
      { t:"直接经济损失（下单/支付/扣款）", parts:["fail-money"] },
      { t:"用户流失/体验崩（对外服务）", parts:["fail-user"] },
      { t:"内部损失，重来就行", parts:["fail-int"] }
    ]},
  { q:"⑧ 谁在用？多少角色/租户？", k:"users",
    opts:[
      { t:"多角色 + 可能多租户（不同公司/部门隔离）", parts:["user-mt"] },
      { t:"多角色但同一组织（老板/员工/管理员）", parts:["user-role"] },
      { t:"个人/单一使用", parts:["user-single"] }
    ]},
  { q:"⑨ 要接多少个外部服务/系统？", k:"external",
    opts:[
      { t:"≥3 个外部依赖（支付/消息/ERP/模型…）", parts:["ext-many"] },
      { t:"1-2 个外部（如只接一个大模型）", parts:["ext-few"] },
      { t:"基本不接外部", parts:["ext-none"] }
    ]},
  { q:"⑩ 项目含 LLM/Agent 吗？（会调用大模型/智能体）", k:"llm",
    opts:[
      { t:"含：核心是 LLM/Agent", parts:["llm-core"] },
      { t:"含一点：个别功能用 AI", parts:["llm-some"] },
      { t:"不含：纯传统软件", parts:["llm-no"] }
    ]}
];

/* ---------- 载体决策规则: tags → 载体 (对应 23 文档决策树) ---------- */
function hcDecideCarrier(tags, parts){
  var cloudNo = tags.indexOf("cloud-no") >= 0;
  var cloudHy = tags.indexOf("cloud-hybrid") >= 0;
  var itYes   = tags.indexOf("it-yes") >= 0;
  var itNo    = tags.indexOf("it-no") >= 0;
  var agent   = tags.indexOf("flow-agent") >= 0 || tags.indexOf("flow-both") >= 0;
  var crud    = tags.indexOf("flow-crud") >= 0;
  var llmCore = parts.indexOf("llm-core") >= 0;

  // 决策树: 数据敏感分支
  if(cloudNo){
    if(itYes) return { id:"c2", name:"② 容器化私有部署", why:"数据不出域 + 客户有 IT 能维护，软件行业标准答案", icon:"📦" };
    return { id:"c3", name:"③ 客户端本地部署", why:"数据不出域 + 客户无 IT，退到装客户机器上", icon:"💻" };
  }
  // 数据可上云
  if(crud && !agent){
    return { id:"c1", name:"① 托管 SaaS", why:"标准流程 CRUD + 数据可上云 = 订阅即用最省", icon:"☁️" };
  }
  if(agent){
    return { id:"c4", name:"④ 智能体 + 网页 (Agent+Web)", why:"长尾流程/多步推理是 Agent 主场；2025 中小企业事实主流", icon:"🤖" };
  }
  if(cloudHy && itYes){
    return { id:"c2b", name:"②/④ 混合: 容器私有 + Agent 内核", why:"核心数据留本地 + 长尾流程 → 私有化部署 AI", icon:"🏗️" };
  }
  return { id:"c4", name:"④ 智能体 + 网页 (Agent+Web)", why:"不确定时选 Agent+Web 做 MVP，上可接 SaaS 下可沉私有", icon:"🤖" };
}

/* ---------- 零件装配规则: parts → 零件清单 (对应 24 文档六步法) ---------- */
var HC_PART_LIB = {
  "crit-disaster": [["灾备/异地容灾","灾难级：挂了会停摆 → 必须有灾备"],["混沌测试/演练","灾难级：不演练等于没有"],["SLO + 24x7 告警","灾难级：要有承诺和值班"]],
  "crit-high":     [["备份恢复","挂了影响大 → 数据必须有备份"],["监控告警","大损失 → 挂了要立刻知道"],["健康检查","大损失 → 自动探活"],["回滚方案","大损失 → 错了要能退"]],
  "crit-low":      [["基础日志","小损失 → 排障够用"],["健康检查","小损失 → 能探活即可"]],
  "scale-high":    [["缓存","高并发 → 扛读压力"],["读写分离/分库","大数据量 → 扩展"],["压测","高并发 → 上线前验证"]],
  "scale-mid":     [["索引优化","中等规模 → 查询别慢"],["基础缓存(可选)","中等 → 热数据缓存"]],
  "sens-extreme":  [["加密存储+传输","极敏感 → 全链路加密"],["审计日志","极敏感 → 谁动了什么要留痕"],["数据脱敏","极敏感 → 展示/导出要脱敏"],["密钥管理","极敏感 → key 集中管"]],
  "sens-pii":      [["TLS + 加密","有 PII → 传输存储加密"],["隐私政策/授权","有 PII → 合规"],["密钥管理","有 PII → key 不能裸奔"]],
  "fail-money":    [["幂等","重复提交=损失 → 同一操作只生效一次"],["重试+超时","下游抖动 → 自动补但不过度"],["熔断","下游挂了 → 别连带我们"],["事务","多步写 → 原子性"]],
  "fail-user":     [["降级方案","体验崩 → 挂了也给基础服务"],["灰度发布","对外服务 → 新版本小流量试"],["监控告警","对外服务 → 用户体验实时盯"]],
  "user-mt":       [["租户隔离","多租户 → 数据必须隔离"],["限流/防滥用","多租户 → 防一个拖垮全部"],["审计日志","多租户 → 责任可追溯"]],
  "user-role":     [["鉴权(登录)","多角色 → 身份要区分"],["授权(RBAC)","多角色 → 权限分级"],["审计日志","多角色操作 → 留痕"]],
  "ext-many":      [["熔断","外部多 → 一个挂了别全崩"],["超时+重试","外部多 → 不能无限等"],["调用链监控","外部多 → 知道卡在哪"]],
  "ext-few":       [["超时","有外部 → 至少别无限等"],["重试(基础)","有外部 → 临时失败自动补"]],
  "llm-core":      [["评测集","LLM 核心 → 没有评测=不知道对错"],["Prompt 版本管理","LLM 核心 → 要能回滚到好版本"],["Token 成本监控","LLM 核心 → 花钱要看得见"],["幻觉/输出审核","LLM 给用户看 → 不能胡说"],["注入防护","用户输入进 Prompt → 防注入"]],
  "llm-some":      [["评测集(轻)","个别 AI 功能 → 至少能验证"],["成本告警","用了模型 → 超预算要知道"]]
};
/* 零件去重 & 排序 */
function hcCollectParts(parts){
  var map = {};
  parts.forEach(function(p){
    (HC_PART_LIB[p] || []).forEach(function(item){
      if(!map[item[0]]) map[item[0]] = item;
    });
  });
  return Object.keys(map).map(function(k){ return map[k]; });
}
/* AI 附属零件: 含 llm-some 且无 llm-core 时补轻量 */
function hcAiExtra(parts){
  var extra = [];
  if(parts.indexOf("llm-some") >= 0 && parts.indexOf("llm-core") < 0){
    extra.push(["评测集(轻)","用到 AI → 至少能验证对错"]);
    extra.push(["输出审核","AI 输出给人看 → 防幻觉"]);
  }
  return extra;
}

/* ---------- 档位建议 ---------- */
function hcTier(carrierId, parts){
  if(carrierId === "c2" || carrierId === "c2b") return "ENTERPRISE ¥80-300k (容器私有化=重交付, 按大单走)";
  if(carrierId === "c3") return "STARTER~AR ¥3-30k (本地部署, 轻量)";
  if(carrierId === "c4") {
    var llm = parts.indexOf("llm-core") >= 0;
    return llm ? "AR 增长型 ¥8-30k (Agent+Web+评测护栏)" : "STARTER ¥3-8k (Agent+Web 入门)";
  }
  if(carrierId === "c1") return "STARTER~AR ¥3-30k (SaaS 订阅, 按场景)";
  return "视范围定";
}

/* ---------- 渲染 ---------- */
function hcStepHtml(){
  var h = '<div style="display:flex;flex-direction:column;gap:12px;max-height:calc(100vh - 240px);overflow-y:auto;padding:4px 2px">';
  HC_QUESTIONS.forEach(function(q, qi){
    h += '<div style="background:#faf7ef;border:1px solid #ece5d3;border-radius:12px;padding:10px 12px">';
    h += '<div style="font-weight:700;font-size:13px;color:#2c3a33;margin-bottom:7px">' + esc(q.q) + '</div>';
    h += '<div style="display:flex;flex-direction:column;gap:5px">';
    q.opts.forEach(function(o, oi){
      h += '<label style="display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:9px;background:#fff;border:1px solid #e8e2d2;cursor:pointer;font-size:12.5px;transition:.15s" onmouseover="this.style.borderColor=\'var(--lime)\'" onmouseout="this.style.borderColor=\'#e8e2d2\'">';
      h += '<input type="radio" name="hcq' + qi + '" value="' + oi + '" style="accent-color:var(--green)">';
      h += '<span>' + esc(o.t) + '</span></label>';
    });
    h += '</div></div>';
  });
  h += '</div>';
  h += '<div style="display:flex;gap:10px;margin-top:14px;justify-content:flex-end">';
  h += '<button onclick="hcReset()" style="padding:9px 16px;border-radius:10px;border:1px solid #d8d2c0;background:transparent;color:#666;cursor:pointer;font-size:13px">清空重选</button>';
  h += '<button onclick="hcAnalyze()" style="padding:9px 20px;border-radius:10px;border:0;background:linear-gradient(135deg,#1e5a44,#2a7a55);color:#fff;cursor:pointer;font-weight:700;font-size:13.5px;box-shadow:0 2px 8px rgba(30,90,68,.25)">🩺 开始分析 →</button>';
  h += '</div>';
  return h;
}
function hcReset(){
  var radios = document.querySelectorAll('#mBody input[type=radio]');
  for(var i=0;i<radios.length;i++) radios[i].checked = false;
}
function hcAnalyze(){
  var tags = [], parts = [];
  var ok = true;
  HC_QUESTIONS.forEach(function(q, qi){
    var sel = document.querySelector('#mBody input[name="hcq' + qi + '"]:checked');
    if(!sel){ ok = false; return; }
    var o = q.opts[parseInt(sel.value, 10)];
    (o.tags || []).forEach(function(t){ tags.push(t); });
    (o.parts || []).forEach(function(p){ parts.push(p); });
  });
  if(!ok){ alert("还有问题没选，请全部答完再分析"); return; }
  var carrier = hcDecideCarrier(tags, parts);
  var lib = hcCollectParts(parts);
  var aiX = hcAiExtra(parts);
  var all = lib.concat(aiX);
  var tier = hcTier(carrier.id, parts);

  var h = '<div style="display:flex;flex-direction:column;gap:14px;max-height:calc(100vh - 240px);overflow-y:auto;padding:2px">';
  /* 结论卡 */
  h += '<div style="border-radius:16px;padding:16px 18px;background:linear-gradient(135deg,#163c31,#2a6b4f);color:#fff">';
  h += '<div style="font-size:11px;opacity:.75;letter-spacing:.5px">🩺 体检结论</div>';
  h += '<div style="font-size:21px;font-weight:800;margin:4px 0 6px">' + carrier.icon + ' ' + carrier.name + '</div>';
  h += '<div style="font-size:12.5px;opacity:.92;line-height:1.55">' + esc(carrier.why) + '</div>';
  h += '<div style="margin-top:10px;font-size:12px;background:rgba(255,255,255,.14);border-radius:8px;padding:7px 10px">💰 档位参考: ' + esc(tier) + '</div>';
  h += '</div>';
  /* 零件清单 */
  h += '<div style="font-size:13px;font-weight:800;color:var(--green)">🧰 必装零件清单 (' + all.length + ' 个) <span style="font-weight:600;font-size:11px;opacity:.6">—— 每个都是你答的问题推导出来的，不是装饰</span></div>';
  if(all.length === 0){
    h += '<div style="padding:14px;border-radius:12px;background:#faf7ef;color:#888;font-size:13px">这个项目很轻（demo/纯展示），暂不需要额外零件，把基础日志加上即可。</div>';
  } else {
    all.forEach(function(it){
      h += '<div style="background:#faf7ef;border:1px solid #ece5d3;border-left:3px solid var(--lime);border-radius:9px;padding:8px 12px;display:flex;gap:8px;align-items:baseline">';
      h += '<span style="font-weight:700;font-size:13px;color:#2c3a33;white-space:nowrap">' + esc(it[0]) + '</span>';
      h += '<span style="font-size:12px;color:#7a837e">' + esc(it[1]) + '</span>';
      h += '</div>';
    });
  }
  h += '<div style="font-size:11px;color:#999;line-height:1.6;margin-top:2px">💡 下一步: 到 🗺️ 关卡地图看每个零件对应哪一关 · 📦 23 载体选型看完整决策树 · 🧰 24 零件装配看六步推导法全文</div>';
  /* 操作按钮 */
  h += '<div style="display:flex;gap:10px;margin-top:6px;flex-wrap:wrap">';
  h += '<button onclick="hcSaveResult()" style="padding:9px 16px;border-radius:10px;border:0;background:linear-gradient(135deg,#8a5a17,#c9962e);color:#fff;cursor:pointer;font-weight:700;font-size:13px">📌 存进 Obsidian</button>';
  h += '<button onclick="openHealthCheck()" style="padding:9px 16px;border-radius:10px;border:1px solid #d8d2c0;background:#fff;color:#444;cursor:pointer;font-size:13px">↩ 重新体检</button>';
  h += '</div></div>';

  document.getElementById("mBody").innerHTML = h;
  document.getElementById("mSub").innerHTML = '<span style="color:var(--muted);font-size:12px">回答汇总 → 规则引擎推导 · 载体/零件/档位</span>';
  hcLast = { carrier:carrier, parts:all, tier:tier };
}
var hcLast = null;

function hcSaveResult(){
  if(!hcLast){ alert("还没有体检结果"); return; }
  var lines = [];
  lines.push("# 项目体检结果 · " + new Date().toISOString().slice(0,10));
  lines.push("");
  lines.push("## 推荐载体");
  lines.push("- " + hcLast.carrier.name + " — " + hcLast.carrier.why);
  lines.push("");
  lines.push("## 档位参考");
  lines.push("- " + hcLast.tier);
  lines.push("");
  lines.push("## 必装零件清单 (" + hcLast.parts.length + ")");
  hcLast.parts.forEach(function(p){ lines.push("- **" + p[0] + "**: " + p[1]); });
  lines.push("");
  lines.push("> 由 8895 项目体检向导生成 · 六步推导法见 24_项目零件装配清单");
  fetch("/api/save_doc", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({ folder:"项目库", name:"体检_" + new Date().toISOString().slice(0,10), content: lines.join("\n") })
  }).then(function(r){ return r.json(); }).then(function(d){
    alert(d && d.ok ? "✅ 已存进 Obsidian 项目库" : ("⚠️ " + (d && d.error || "保存失败")));
  }).catch(function(){ alert("⚠️ 保存失败（服务未开/接口不可用）"); });
}

/* ---------- 入口 ---------- */
function openHealthCheck(){
  vlShowModal("🩺 项目体检 · 10 问出方案", hcStepHtml());
}
