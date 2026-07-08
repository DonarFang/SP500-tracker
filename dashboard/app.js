/**
 * SP500 Trend Decision Support Cockpit — app.js v2.0
 * 5 tabs: Market Overview / Leader Board / Watchlist / Positions & Exit / Research & Backtest
 */

const EXPORTS_BASE = 'https://donarfang.github.io/SP500-tracker/exports';
const RESEARCH_BASE = 'https://donarfang.github.io/SP500-tracker/data/research/e1r';
const PALETTE = ['#378ADD','#1D9E75','#D85A30','#7F77DD','#BA7517','#D4537E','#639922','#5DCAA5','#E24B4A','#EF9F27'];
const TS_COLOR = {'Strong Expansion':'#1D9E75','Healthy Trend':'#378ADD','Mature Trend':'#BA7517','Weakening Trend':'#D85A30','Broken Trend':'#993C1D'};
const TS_ZH    = {'Strong Expansion':'强势扩张','Healthy Trend':'健康趋势','Mature Trend':'趋势成熟','Weakening Trend':'趋势减弱','Broken Trend':'趋势破坏'};
const REG_META = {
  Expansion:  {zh:'扩张期',desc:'高TH+高动量 — 最佳持有'},
  Mature:     {zh:'成熟期',desc:'高TH+低动量 — 观察减速'},
  Speculative:{zh:'投机期',desc:'低TH+高动量 — 短线机会'},
  Broken:     {zh:'破坏期',desc:'低TH+低动量 — 规避风险'},
};
const IDX_ICONS = {SPX:'📊',NDX:'💻',VIX:'😨',SOX:'🔬'};

let DATA = {market:null,leaderboard:null,watchlist:null,lifecycle:null,health:null,backtest:null,tradelog:null,stockCharts:null,oosEquity:null,e1rRegime:null,e1rConfirmed:null,e1rSideways3i:null,e1rSideways3ir:null,e1rSideways3k:null,e1rFormal:null};
let charts = {};

const $   = id => document.getElementById(id);
const p2  = (v,d=2) => parseFloat(v||0).toFixed(d);
const sgn = v => v>=0?'+':'';
const badge = a => `<span class="badge badge-${a}">${a}</span>`;
const tsBadge = s => { const zh=TS_ZH[s]||s,col=TS_COLOR[s]||'#888'; return `<span style="font-size:10px;padding:2px 7px;border-radius:10px;background:${col}20;color:${col};font-weight:600">${zh}</span>`; };
const scCol = s => s>=75?'#1D9E75':s>=50?'#378ADD':s>=30?'#BA7517':'#D85A30';
const scBar = (s,w='80px') => `<div class="score-wrap" style="width:${w}"><div class="score-bar" style="width:${Math.min(s,100)}%;background:${scCol(s)}"></div></div>`;
const avg   = (arr,k) => arr.length ? arr.reduce((a,x)=>a+(parseFloat(x[k])||0),0)/arr.length : 0;
const aiBox = (obs,rsn,con,act) => `<div class="ai-box">
  <div class="ai-row"><strong>📊 Observation</strong>：${obs}</div>
  <div class="ai-row"><strong>🧠 Reasoning</strong>：${rsn}</div>
  <div class="ai-row"><strong>✅ Conclusion</strong>：${con}</div>
  <div class="ai-row"><strong>⚡ Action</strong>：${act}</div></div>`;
const fmt = v => { if(v==null)return'—'; const n=parseFloat(v); return isNaN(n)?v:(n>=0?'+':'')+n.toFixed(2)+'%'; };

// ── Reusable Stock Preview Chart ────────────────────────
function getStockChartPayload(symbol){
  const sc = DATA.stockCharts || {};
  return sc[symbol] || null;
}

function chartKeyForPreview(previewContainerId){
  return `preview_${previewContainerId}`;
}

function renderStockPreviewChart(containerId, symbol){
  const wrap = $(containerId);
  if(!wrap) return;
  const chartKey = chartKeyForPreview(containerId);
  // 先销毁该容器自己的旧实例
  if(charts[chartKey]){ charts[chartKey].destroy(); charts[chartKey]=null; }

  const p = getStockChartPayload(symbol);
  if(!p || !p.dates || !p.dates.length){
    wrap.innerHTML = `<div style="padding:24px;text-align:center;color:var(--text2);font-size:13px">No chart data available for ${symbol}</div>`;
    return;
  }
  // 副标题指标
  const metaBits = [];
  if(p.leader_score!=null)   metaBits.push(`LeaderScore <strong>${p2(p.leader_score,1)}</strong>`);
  if(p.rs_score!=null)       metaBits.push(`RS <strong>${p2(p.rs_score,1)}</strong>`);
  if(p.momentum_score!=null) metaBits.push(`Mom <strong>${p2(p.momentum_score,1)}</strong>`);
  if(p.trend_health!=null)   metaBits.push(`TH <strong>${p2(p.trend_health,1)}</strong>`);
  if(p.trend_state)          metaBits.push(tsBadge(p.trend_state));
  if(p.trade_action)         metaBits.push(badge(p.trade_action));
  // 1D return（用最后两个 close）
  const cl = p.close||[];
  if(cl.length>=2 && cl[cl.length-2]){
    const r1d = (cl[cl.length-1]/cl[cl.length-2]-1)*100;
    const rc  = r1d>=0?'var(--green)':'var(--red)';
    metaBits.push(`<span style="color:${rc}">1D ${r1d>=0?'+':''}${p2(r1d,2)}%</span>`);
  }

  // 每次重建容器内 canvas（不用全局 id，避免多容器 id 冲突）
  wrap.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px;margin-bottom:6px">
      <div><strong style="font-size:15px">${symbol}</strong>
        <span style="color:var(--text2);font-size:12px">${p.name||''} · ${p.sector||''}</span></div>
      <div style="font-size:11px;color:var(--text2);display:flex;gap:10px;flex-wrap:wrap;align-items:center">${metaBits.join('<span style="opacity:.4">·</span>')}</div>
    </div>
    <div class="cwrap" style="height:200px"><canvas></canvas></div>`;

  const el = wrap.querySelector('canvas');
  if(!el) return;
  const labels = p.dates.map(d=>String(d).slice(5));
  const ds = [{label:'Close',data:p.close,borderColor:'#378ADD',backgroundColor:'rgba(55,138,221,0.08)',borderWidth:2,pointRadius:0,fill:true,tension:0.15}];
  if(p.ma20 && p.ma20.length) ds.push({label:'MA20',data:p.ma20,borderColor:'#1D9E75',borderWidth:1.5,pointRadius:0,borderDash:[],tension:0.15});
  if(p.ma50 && p.ma50.length) ds.push({label:'MA50',data:p.ma50,borderColor:'#BA7517',borderWidth:1.5,pointRadius:0,borderDash:[4,3],tension:0.15});
  charts[chartKey] = new Chart(el,{type:'line',data:{labels,datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
      plugins:{legend:{display:true,labels:{font:{size:10},boxWidth:18,usePointStyle:true}},
        tooltip:{callbacks:{title:items=>p.dates[items[0].dataIndex]}}},
      scales:{x:{ticks:{font:{size:9},maxTicksLimit:8},grid:{display:false}},
              y:{ticks:{font:{size:9}},grid:{color:'rgba(128,128,128,0.1)'}}}}});
}

function bindStockPreviewRows(rootSelector, rowSelector, symbolGetter, previewContainerId){
  const root = document.querySelector(rootSelector);
  if(!root) return;
  const rows = Array.from(root.querySelectorAll(rowSelector));
  if(!rows.length) return;
  let pinned = null; // click/tap 锁定的 symbol

  const showFor = sym => { if(sym) renderStockPreviewChart(previewContainerId, sym); };

  rows.forEach(row=>{
    const sym = symbolGetter(row);
    if(!sym) return;
    row.style.cursor = 'pointer';
    // desktop hover
    row.addEventListener('mouseenter',()=>{ if(!pinned) showFor(sym); });
    // click/tap 锁定切换
    row.addEventListener('click',()=>{
      pinned = (pinned===sym) ? null : sym;
      showFor(sym);
      rows.forEach(r=>r.classList.remove('row-pinned'));
      if(pinned) row.classList.add('row-pinned');
    });
  });
  // mouseleave 不清空（保留当前图）— 不绑定 mouseleave 清空逻辑
  // 默认显示第一只
  const firstSym = symbolGetter(rows[0]);
  if(firstSym) showFor(firstSym);
}


async function fetchJ(name) {
  const r = await fetch(`${EXPORTS_BASE}/${name}.json?t=${Date.now()}`);
  if (!r.ok) throw new Error(`${name}.json: HTTP ${r.status}`);
  return r.json();
}

async function fetchResearchJ(name) {
  const r = await fetch(`${RESEARCH_BASE}/${name}.json?t=${Date.now()}`);
  if (!r.ok) throw new Error(`${name}.json: HTTP ${r.status}`);
  return r.json();
}

async function loadAll() {
  ['market','leader','watchlist','positions','research'].forEach(t=>{
    const el=$('s-'+t); if(el) el.innerHTML='<div class="loading"><span class="spin"></span>加载中...</div>';
  });
  $('uptime').textContent='加载中...';
  try {
    // 核心数据：market_state / leaderboard 失败则整页报错
    // 辅助数据：其余均 graceful fallback，不阻塞渲染
    const [mkt,lb] = await Promise.all([
      fetchJ('market_state'),
      fetchJ('leaderboard'),
    ]);
    DATA.market=mkt.market; DATA.leaderboard=lb.leaders||[];
    $('uptime').textContent='数据时间：'+(mkt.generated_at_display||mkt.generated_at||'未知');

    // 辅助数据并行加载，各自 fallback
    const [wl,lc,dh,bt,tlog,sc,oosEq,e1rReg,e1rConf,e1r3i,e1r3ir,e1r3k,e1rFormal] = await Promise.all([
      fetchJ('watchlist').catch(()=>({watchlist:[]})),
      fetchJ('lifecycle').catch(()=>({regimes:{}})),
      fetchJ('data_health').catch(()=>null),
      fetchJ('backtest').catch(()=>null),
      fetchJ('trade_log').catch(()=>null),
      fetchJ('stock_charts').catch(()=>({symbols:{}})),
      fetchJ('oos_equity_curve').catch(()=>null),
      fetchResearchJ('e1r_regime_attribution_review').catch(()=>null),
      fetchResearchJ('e1r_phase3e_confirmed_quality_diagnostic').catch(()=>null),
      fetchResearchJ('e1r_phase3i_sideways_quality_decomposition_diagnostic').catch(()=>null),
      fetchResearchJ('e1r_phase3ir_sideways_recovery_robustness_diagnostic').catch(()=>null),
      fetchResearchJ('e1r_phase3k_sideways_recovery_regime_definition_review').catch(()=>null),
      fetchResearchJ('e1r_formal_backtest_v0_1').catch(()=>null),
    ]);
    DATA.watchlist=wl.watchlist||[]; DATA.lifecycle=lc.regimes||{};
    DATA.health=dh; DATA.backtest=bt; DATA.tradelog=tlog;
    DATA.stockCharts=(sc&&sc.symbols)||{};
    DATA.oosEquity=oosEq;
    DATA.e1rRegime=e1rReg; DATA.e1rConfirmed=e1rConf;
    DATA.e1rSideways3i=e1r3i; DATA.e1rSideways3ir=e1r3ir; DATA.e1rSideways3k=e1r3k; DATA.e1rFormal=e1rFormal;

    ['market','leader','watchlist','positions','research'].forEach(t=>render(t));
  } catch(e) {
    // 只有核心数据失败才整页报错
    ['market','leader','watchlist','positions','research'].forEach(t=>{
      const el=$('s-'+t);
      if(el) el.innerHTML=`<div class="error"><strong>核心数据加载失败</strong><br>${e.message}<br><br>请先运行 GitHub Actions → 初始化历史数据。</div>`;
    });
  }
}

function go(name,btn){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on')); btn.classList.add('on');
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on')); $('s-'+name).classList.add('on');
}


function renderE1RResearchPanel(vr){
  const reg=DATA.e1rRegime, conf=DATA.e1rConfirmed, s3i=DATA.e1rSideways3i, s3ir=DATA.e1rSideways3ir, s3k=DATA.e1rSideways3k;
  const formal=DATA.e1rFormal||{}, fm=formal.metrics||{};
  const e1r=vr?.E1R_REGIME_AWARE_V0_1;
  if(!reg && !conf && !s3i && !s3ir && !s3k && !e1r && !formal.variant_id) return '';

  const nfmt = (v,d=2) => (v===null||v===undefined||v==='') ? '—' : (Number(v)>=0?'+':'') + Number(v).toFixed(d) + '%';
  const num  = (v,d=2) => (v===null||v===undefined||v==='') ? '—' : Number(v).toFixed(d);

  const fullRet = fm.total_return_pct ?? e1r?.total_return_pct ?? reg?.summary?.e1r_full_return_pct ?? reg?.e1r_full_return_pct;
  const maxDD   = fm.max_drawdown_pct ?? e1r?.max_drawdown_pct ?? reg?.summary?.e1r_max_drawdown_pct ?? reg?.e1r_max_drawdown_pct;
  const pf      = fm.profit_factor ?? e1r?.profit_factor ?? reg?.summary?.e1r_profit_factor ?? reg?.e1r_profit_factor;
  const sharpe  = fm.sharpe_ratio ?? e1r?.sharpe_ratio ?? e1r?.sharpe ?? reg?.summary?.e1r_sharpe ?? reg?.e1r_sharpe;
  const trades  = fm.number_of_trades ?? e1r?.number_of_trades ?? e1r?.num_trades ?? e1r?.trades_count ?? reg?.summary?.e1r_trades;
  const alpha   = fm.alpha_pct;
  const exposure= fm.exposure_pct;

  const up = reg?.regime_attribution?.UPTREND || reg?.regime_results?.UPTREND || reg?.UPTREND || {};
  const upE1R = up?.e1r_return_pct ?? up?.e1r_total_return_pct ?? 70.92;
  const upE1  = up?.e1_return_pct ?? up?.e1_total_return_pct ?? 10.63;
  const upDelta = up?.delta_pct ?? up?.excess_pct ?? 60.29;

  const r3i = s3i?.rule_results?.UPGRADE_WATCH_RECOVERY || s3i?.UPGRADE_WATCH_RECOVERY || {};
  const r3ir = s3ir?.robustness_summary || s3ir?.summary || {};
  const r3k = s3k?.summary || s3k?.decision || {};

  const pass3ir = r3ir?.checks_passed ?? r3ir?.passed_checks ?? '5/7';
  const dec3ir = r3ir?.decision || s3ir?.decision || 'PROMISING_BUT_STILL_DIAGNOSTIC_ONLY';
  const dec3k = r3k?.decision || s3k?.decision || 'PROMISING_BUT_TIME_CONCENTRATED_DIAGNOSTIC_ONLY';

  return `<div class="e1r-panel">
    <div class="e1r-head">
      <div>
        <h3>🧪 E1-R Research Summary</h3>
        <div class="muted">Formal backtest available from 5Y research export. Main engine migration / OOS tracking not yet completed.</div>
      </div>
      <span class="badge-e1r">E1R_REGIME_AWARE_V0_1</span>
    </div>

    <div class="e1r-metrics-row">
      <div class="metric"><div>Full Return</div><strong>${nfmt(fullRet)}</strong></div>
      <div class="metric"><div>MaxDD</div><strong>${nfmt(maxDD)}</strong></div>
      <div class="metric"><div>PF</div><strong>${num(pf)}</strong></div>
      <div class="metric"><div>Sharpe</div><strong>${num(sharpe)}</strong></div>
      <div class="metric"><div>Trades</div><strong>${trades??'—'}</strong></div>
      <div class="metric"><div>Alpha</div><strong>${nfmt(alpha)}</strong></div>
      <div class="metric"><div>Exposure</div><strong>${nfmt(exposure)}</strong></div>
    </div>

    <div class="grid-3">
      <div class="card mini">
        <h4>UPTREND Confirmed</h4>
        <p>E1-R ${nfmt(upE1R)} vs E1 ${nfmt(upE1)}，delta ${nfmt(upDelta)}。</p>
        <div class="tag-good">Execution channel</div>
      </div>
      <div class="card mini">
        <h4>SIDEWAYS Recovery</h4>
        <p>Phase 3I upgrade-watch recovery: 20D excess ${nfmt(r3i?.excess_20d_pct ?? 3.90)}，30D excess ${nfmt(r3i?.excess_30d_pct ?? 8.10)}。</p>
        <div class="tag-warn">Watchlist only</div>
      </div>
      <div class="card mini">
        <h4>Robustness Gate</h4>
        <p>3I-R checks ${pass3ir}；3K decision: ${dec3k || dec3ir}。</p>
        <div class="tag-warn">Diagnostic only</div>
      </div>
    </div>
  </div>`;
}


// ═══════════════════════════════════════════════════════
// render dispatcher
// ═══════════════════════════════════════════════════════
function render(tab) {
  // B_STAGE_3_8E1_NATIVE_RESEARCH_BACKTEST_CLEANUP: native tab cleanup only; no strategy logic changes.

  // ── Tab 1: Market Overview ───────────────────────────
  if (tab==='market') {
    if (!DATA.market) return;
    const m=DATA.market||{}, idx=m.indices||{}, sc=m.market_score||0, bd=m.score_breakdown||{};
    const scC=sc>=80?'#1D9E75':sc>=60?'#BA7517':'#D85A30';
    const dh=DATA.health;

    let h='';
    if(dh){
      const st=dh.data_status, col=st==='PASS'?'var(--green)':st==='WARN'?'var(--amber)':'var(--red)';
      const ic=st==='PASS'?'✅':st==='WARN'?'⚠️':'❌';
      h+=`<div style="background:${col}15;border:.5px solid ${col}40;border-radius:var(--radius);padding:.6rem 1rem;margin-bottom:1rem;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px">
        <span>${ic} 数据质量 <strong style="color:${col}">${st}</strong> · 成分股 ${dh.universe_count||0} 只 · 有效 ${dh.valid_symbols||0} 只 · 覆盖率 ${dh.history_coverage_pct||0}% · 最新 ${dh.latest_data_date||'—'}</span>
        <span style="color:var(--text3)">${dh.generated_at_display||''}</span>
      </div>`;
    }

    // Gate v2.1 status
    const gateOn = m.leadership_confirmed && (m.spx_ma50_slope_positive !== false);
    const gateColor = gateOn ? '#1D9E75' : '#D85A30';
    const gateLabel = gateOn ? 'FULL_ON' : 'RISK_OFF';
    h+=`<div style="background:${gateColor}15;border:.5px solid ${gateColor}40;border-radius:var(--radius);padding:.6rem 1rem;margin-bottom:1rem;font-size:13px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-weight:600;color:${gateColor}">Gate v2.1 · ${gateLabel}</span>
      <span style="color:var(--text2);font-size:12px">SPX MA50 slope: ${m.spx_ma50_slope_positive!==false?'positive ↑':'negative ↓'}</span>
      <span style="color:var(--text2);font-size:12px">Leadership: ${m.leadership_confirmed?'2/2 confirmed ✓':'unconfirmed ⚠️'}</span>
      <span style="color:var(--text3);font-size:11px">Shock · VIX excluded from Gate</span>
    </div>`;

    h+=`<div class="grid-3">
      <div class="mc" style="text-align:center">
        <div class="mc-label">Market Score</div>
        <div style="font-size:48px;font-weight:700;color:${scC};line-height:1.1">${sc}</div>
        <div class="score-wrap" style="height:8px;margin:.4rem 0"><div class="score-bar" style="width:${sc}%;background:${scC}"></div></div>
        <div style="font-size:10px;color:var(--text2)">SPX 35% · NDX 25% · SOX 25% · VIX 15%</div>
      </div>
      <div class="mc" style="text-align:center">
        <div class="mc-label">市场状态</div>
        <div style="font-size:36px;margin:.3rem 0">${m.state_icon||'🟡'}</div>
        <div style="font-size:18px;font-weight:700;color:${m.state_color||scC}">${m.state_zh||'中性观望'}</div>
        <div style="font-size:10px;color:var(--text2);margin-top:.4rem">${sc>=80?'80-100 Strong Risk-On':sc>=60?'60-80 Risk-On':sc>=40?'40-60 Neutral':sc>=20?'20-40 Risk-Off':'0-20 Defensive'}</div>
      </div>
      <div class="mc" style="text-align:center">
        <div class="mc-label">领涨确认</div>
        <div style="font-size:28px;margin:.3rem 0">${m.leadership_confirmed?'✅':'⚠️'}</div>
        <div style="font-size:12px;font-weight:600;color:${m.leadership_confirmed?'var(--green)':'var(--amber)'}">${m.leadership_confirmed?'Leadership Confirmed':'Leadership Unconfirmed'}</div>
        <div style="font-size:10px;color:var(--text2);margin-top:.3rem">NDX &amp; SOX &gt; MA50</div>
      </div>
    </div>`;

    h+=`<div class="card"><div class="card-head">四大指数实时概览</div><div class="card-body"><div class="grid-4">`;
    ['SPX','NDX','VIX','SOX'].forEach(code=>{
      const ix=idx[code]||{}, av=ix.available!==false, cp=av?ix.change_pct||0:0, cc=cp>=0?'var(--green)':'var(--red)';
      if(code==='VIX'){
        h+=`<div style="background:var(--bg2);border-radius:var(--radius);padding:.85rem">
          <div style="font-size:11px;color:var(--text2);margin-bottom:6px">${IDX_ICONS[code]} ${ix.name||code} <span style="font-size:10px;opacity:.6">(ref only)</span></div>
          <div style="font-size:22px;font-weight:700;color:${ix.vix_color||'var(--text)'}">${av?p2(ix.price,2):'N/A'}</div>
          <div style="font-size:11px;margin-top:4px;display:flex;justify-content:space-between">
            <span style="color:${cc}">${sgn(cp)}${p2(cp,2)}%</span>
            <span style="color:${ix.vix_color||'var(--text2)'};">${ix.vix_state||''}</span>
          </div>
          <div style="font-size:10px;color:var(--text3);margin-top:4px">Not a Gate condition</div>
        </div>`;
      } else {
        h+=`<div style="background:var(--bg2);border-radius:var(--radius);padding:.85rem">
          <div style="font-size:11px;color:var(--text2);margin-bottom:6px">${IDX_ICONS[code]} ${ix.name||code}</div>
          <div style="font-size:22px;font-weight:700">${av?parseFloat(ix.price||0).toLocaleString(undefined,{maximumFractionDigits:0}):'N/A'}</div>
          <div style="font-size:11px;margin-top:4px;display:flex;justify-content:space-between">
            <span style="color:${cc}">${sgn(cp)}${p2(cp,2)}%</span>
            <span style="color:${ix.trend_color||'var(--text2)'};font-size:10px">${ix.trend||''}</span>
          </div>
          <div style="font-size:10px;color:var(--text3);margin-top:4px">MA50: ${av?parseFloat(ix.ma50||0).toLocaleString(undefined,{maximumFractionDigits:0}):'—'} · ${ix.above_ma50?'↑ above':'↓ below'}</div>
        </div>`;
      }
    });
    h+=`</div></div></div>`;

    h+=`<div class="card"><div class="card-head">Market Score 评分明细</div><div class="card-body"><div class="grid-4">`;
    ['SPX','NDX','SOX','VIX'].forEach(code=>{
      const b=bd[code]||{}, sc2=b.score||0, col2=scCol(sc2);
      const extra=code==='VIX'
        ?`<div style="font-size:10px;color:${b.vix_color||'var(--text2)'}">${b.vix_state||'—'}</div>`
        :`<div style="font-size:10px;color:${b.above_ma50?'var(--green)':'var(--red)'}">MA50：${b.above_ma50?'↑上方':'↓下方'}</div>`;
      h+=`<div style="text-align:center;background:var(--bg2);border-radius:var(--radius);padding:.7rem .5rem">
        <div style="font-size:11px;color:var(--text2);margin-bottom:4px">${IDX_ICONS[code]} ${code} (${b.weight||'—'})</div>
        <div style="font-size:22px;font-weight:700;color:${col2}">${p2(sc2,0)}</div>
        <div class="score-wrap" style="margin:.3rem auto;width:55px"><div class="score-bar" style="width:${sc2}%;background:${col2}"></div></div>
        ${extra}</div>`;
    });
    h+=`</div></div></div>`;

    const tp=idx.tech_premium, sp=idx.sox_premium;
    if(tp!==undefined||sp!==undefined){
      h+=`<div style="display:flex;gap:8px;margin-bottom:1rem;flex-wrap:wrap">`;
      if(tp!==undefined) h+=`<span style="font-size:12px;padding:5px 14px;border-radius:20px;background:var(--bg2)">💻 ${idx.tech_premium_signal||''} &nbsp;<strong style="color:${tp>=0?'var(--green)':'var(--red)'}">${sgn(tp)}${p2(tp,2)}%</strong> vs SPX 20日</span>`;
      if(sp!==undefined) h+=`<span style="font-size:12px;padding:5px 14px;border-radius:20px;background:var(--bg2)">🔬 ${idx.sox_premium_signal||''} &nbsp;<strong style="color:${sp>=0?'var(--green)':'var(--red)'}">${sgn(sp)}${p2(sp,2)}%</strong> vs SPX 20日</span>`;
      h+=`</div>`;
    }

    h+=`<div class="grid-2">
      <div class="card" style="margin-bottom:0"><div class="card-head">标普500 趋势 <span class="sub">距MA50 ${sgn(m.pct_above_ma50)}${p2(m.pct_above_ma50)}%</span></div><div class="card-body">
        <div class="cwrap" style="height:200px"><canvas id="cw-spx"></canvas></div>
      </div></div>
      <div class="card" style="margin-bottom:0"><div class="card-head">领涨板块 Top10</div><div class="card-body">
        <div id="sec-legend" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;font-size:10px;color:var(--text2)"></div>
        <div class="cwrap" style="height:160px"><canvas id="cw-sector"></canvas></div>
      </div></div>
    </div><br>`;

    h+=`<div class="mc" style="margin-bottom:1rem"><div class="mc-label">涨跌家数</div>
      <div class="mc-val"><span style="color:var(--green)">${m.advance_count||'-'}</span><span style="color:var(--text3);font-size:14px"> / </span><span style="color:var(--red)">${m.decline_count||'-'}</span></div>
      <div class="mc-sub">A/D Ratio: ${p2(m.advance_decline,2)}</div>
    </div>`;

    const vix=idx['VIX']||{};
    h+=aiBox(
      `Market Score ${sc}，SPX ${parseFloat(m.spx_close||0).toLocaleString()}，VIX ${vix.available?p2(vix.price,1)+'（'+vix.vix_state+'）':'N/A'}，涨跌比 ${m.advance_count}:${m.decline_count}。Gate v2.1 状态：${gateLabel}。`,
      `${m.leadership_confirmed?'NDX/SOX 均位于MA50上方，Leadership Confirmed。':'Leadership Unconfirmed，等待指数收复MA50。'}${idx.tech_premium!==undefined?' NDX相对SPX 20日：'+(idx.tech_premium>=0?'+':'')+p2(idx.tech_premium,2)+'%。':''}`,
      `${m.state_icon||'🟡'} ${m.state_zh||'中性观望'}，${sc>=80?'强势偏好，全力持仓领导股。':sc>=60?'风险偏好，适合趋势跟随。':sc>=40?'中性观望，控制仓位。':sc>=20?'风险规避，大幅减仓。':'防御模式，空仓等待。'}`,
      sc>=80?'满仓持有 BUY 信号强势股':sc>=60?'保留核心持仓，新仓只买 BUY 信号':sc>=40?'减少新仓，保留 HOLD 信号':sc>=20?'只保留最强持仓，清理 REDUCE 信号':'全面防御，清仓等待 Market Score ≥ 40'
    );
    h+='<p class="note">数据来自 Yahoo Finance，每交易日 18:00 ET 自动更新。不构成投资建议。</p>';
    $('s-market').innerHTML=h;

    setTimeout(()=>{
      const spxEl=$('cw-spx'), spxIdx=idx['SPX']||{};
      if(spxEl&&spxIdx.chart_dates?.length){
        if(charts.spx)charts.spx.destroy();
        charts.spx=new Chart(spxEl,{type:'line',data:{labels:spxIdx.chart_dates.map(d=>d.slice(5)),datasets:[
          {label:'SPX',data:spxIdx.chart_prices,borderColor:'#378ADD',backgroundColor:'rgba(55,138,221,0.06)',borderWidth:2,pointRadius:0,tension:0.2,fill:true},
          {label:'MA20',data:spxIdx.chart_ma20,borderColor:'#1D9E75',borderWidth:1.5,pointRadius:0,borderDash:[4,3],fill:false},
          {label:'MA50',data:spxIdx.chart_ma50,borderColor:'#BA7517',borderWidth:1.5,pointRadius:0,borderDash:[6,3],fill:false},
        ]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
          plugins:{legend:{labels:{font:{size:10},boxWidth:10,padding:8}}},
          scales:{x:{ticks:{font:{size:10},maxTicksLimit:10},grid:{display:false}},
                  y:{ticks:{font:{size:10},callback:v=>parseFloat(v).toLocaleString()},grid:{color:'rgba(128,128,128,0.1)'}}}
        }});
      }
      const secEl=$('cw-sector'), secLeg=$('sec-legend');
      const secmap={}; (DATA.leaderboard||[]).forEach(s=>{const sec=s.sector||'Other';secmap[sec]=(secmap[sec]||0)+1;});
      const secArr=Object.entries(secmap).sort((a,b)=>b[1]-a[1]);
      if(secEl&&secArr.length){
        if(secLeg) secLeg.innerHTML=secArr.map((e,i)=>`<span style="display:flex;align-items:center;gap:3px"><span style="width:8px;height:8px;border-radius:2px;background:${PALETTE[i%PALETTE.length]}"></span>${e[0]}(${e[1]})</span>`).join('');
        if(charts.sector)charts.sector.destroy();
        charts.sector=new Chart(secEl,{type:'doughnut',data:{labels:secArr.map(e=>e[0]),datasets:[{data:secArr.map(e=>e[1]),backgroundColor:PALETTE.slice(0,secArr.length),borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}}});
      }
    },80);
  }

  // ── Tab 2: Leader Board ──────────────────────────────
  if (tab==='leader') {
    const leaders=DATA.leaderboard||[];
    if(!leaders.length){$('s-leader').innerHTML='<div class="loading">暂无数据</div>';return;}
    let h=`<div class="card"><div class="card-head">Top 10 Leader Board <span class="sub">LeaderScore = 0.5×RS + 0.3×Momentum + 0.2×TrendHealth</span></div><div class="card-body"><div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>代码</th><th>板块</th><th>RS%</th><th>动量</th><th>健康度</th><th>Leader分</th><th>趋势状态</th><th>操作</th></tr></thead><tbody>`;
    leaders.forEach(s=>{
      const rc=(s.rs_score||0)>=70?'var(--green)':(s.rs_score||0)>=40?'var(--amber)':'var(--red)';
      h+=`<tr data-symbol="${s.symbol}">
        <td style="color:var(--text3);font-weight:500">${s.rank}</td>
        <td><div class="stock-symbol">${s.symbol}</div><div class="stock-name">${s.name||''}</div></td>
        <td><span class="pill">${s.sector||'—'}</span></td>
        <td style="color:${rc};font-weight:600">${p2(s.rs_score||0,1)}</td>
        <td style="color:${(s.momentum_score||0)>=50?'var(--green)':'var(--red)'};font-weight:500">${p2(s.momentum_score||0,1)}</td>
        <td><span style="font-weight:600;color:${scCol(s.trend_health||0)}">${p2(s.trend_health,0)}</span>${scBar(s.trend_health||0,'55px')}</td>
        <td style="font-weight:700;font-size:14px;color:${scCol(s.leader_score||0)}">${p2(s.leader_score,1)}</td>
        <td>${tsBadge(s.trend_state||'')}</td>
        <td>${badge(s.trade_action||'HOLD')}</td>
      </tr>`;
    });
    h+=`</tbody></table></div></div></div>`;

    h+=`<div class="card" id="lb-preview-card"><div class="card-head">个股预览 <span class="sub">hover / tap 行切换</span></div><div class="card-body"><div id="lb-stock-preview"></div></div></div>`;

    h+=`<div class="grid-2">
      <div class="card" style="margin-bottom:0"><div class="card-head">RS% vs 动量散点</div><div class="card-body"><div class="cwrap" style="height:240px"><canvas id="cw-rs-mom"></canvas></div></div></div>
      <div class="card" style="margin-bottom:0"><div class="card-head">健康度对比</div><div class="card-body"><div class="cwrap" style="height:240px"><canvas id="cw-health"></canvas></div></div></div>
    </div>`;

    // Lifecycle 象限摘要（从 lifecycle 数据迁入）
    const lc=DATA.lifecycle||{};
    const order=['Expansion','Mature','Speculative','Broken'];
    if(Object.keys(lc).length){
      h+=`<div class="card"><div class="card-head">个股生命周期象限 <span class="sub">Top50 趋势分布</span></div><div class="card-body"><div class="regime-grid">`;
      order.forEach(reg=>{
        const stocks=lc[reg]||[], m2=REG_META[reg]||{};
        h+=`<div class="regime-cell badge-${reg}">
          <div style="font-size:13px;font-weight:600;margin-bottom:4px">${m2.zh||reg} <span style="font-size:20px;font-weight:700">${stocks.length}</span></div>
          <div style="font-size:11px;opacity:.8;margin-bottom:8px">${m2.desc||''}</div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">
            ${stocks.slice(0,6).map(s=>`<span style="font-size:10px;background:rgba(255,255,255,0.25);padding:1px 6px;border-radius:10px;font-weight:500">${s.symbol}</span>`).join('')}
            ${stocks.length>6?`<span style="font-size:10px;opacity:.6">+${stocks.length-6}</span>`:''}
          </div>
        </div>`;
      });
      h+=`</div></div></div>`;
    }

    h+=aiBox(
      `Top10 平均 RS ${p2(avg(leaders,'rs_score'),1)}，平均动量 ${p2(avg(leaders,'momentum_score'),1)}，平均健康度 ${p2(avg(leaders,'trend_health'),1)}，平均 LeaderScore ${p2(avg(leaders,'leader_score'),1)}。`,
      `${leaders.filter(s=>s.trade_action==='BUY'||s.trade_action==='ADD').map(s=>s.symbol).join('、')||'暂无'} 处于买入/加仓信号区间。`,
      `领导股整体${avg(leaders,'trend_health')>=65?'趋势健康，适合持有':'趋势减弱，注意控制风险'}。`,
      `重点跟踪 ${leaders.slice(0,3).map(s=>s.symbol).join('、')} 的走势与成交量变化。`
    );
    $('s-leader').innerHTML=h;
    setTimeout(()=>{
      bindStockPreviewRows('#s-leader','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'lb-stock-preview');
      const e1=$('cw-rs-mom');
      if(e1){if(charts.rsMom)charts.rsMom.destroy();
        charts.rsMom=new Chart(e1,{type:'scatter',data:{datasets:[{label:'Top10',data:leaders.map(s=>({x:s.rs_score||0,y:s.momentum_score||0})),backgroundColor:PALETTE,pointRadius:8,pointHoverRadius:11}]},
          options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${leaders[ctx.dataIndex]?.symbol}  RS:${p2(ctx.parsed.x,1)}  MOM:${p2(ctx.parsed.y,2)}%`}}},
            scales:{x:{title:{display:true,text:'RS Score (0-100)',font:{size:10}},min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},
                    y:{title:{display:true,text:'Momentum Score (0-100)',font:{size:10}},min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}}}
          }});}
      const e2=$('cw-health');
      if(e2){if(charts.health)charts.health.destroy();
        const sorted=[...leaders].sort((a,b)=>(b.trend_health||0)-(a.trend_health||0));
        charts.health=new Chart(e2,{type:'bar',data:{labels:sorted.map(s=>s.symbol),datasets:[{label:'健康度',data:sorted.map(s=>s.trend_health||0),backgroundColor:sorted.map(s=>scCol(s.trend_health||0)),borderRadius:4}]},
          options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},x:{ticks:{font:{size:11}},grid:{display:false}}}}});}
    },80);
  }

  // ── Tab 3: Watchlist ──────────────────────────────────
  if (tab==='watchlist') {
    const wl=DATA.watchlist||[];
    if(!wl.length){$('s-watchlist').innerHTML='<div class="loading">暂无数据</div>';return;}
    const leaderSyms=new Set((DATA.leaderboard||[]).map(s=>s.symbol));
    const overlap=wl.filter(s=>leaderSyms.has(s.symbol)).length;
    const overlapPct=wl.length?Math.round(overlap/wl.length*100):0;
    const overlapColor=overlapPct<30?'var(--green)':'var(--red)';

    let h=`<div style="display:flex;gap:8px;margin-bottom:1rem;flex-wrap:wrap;font-size:12px">
      <span style="padding:4px 12px;border-radius:20px;background:var(--bg2)">候选池：Rank 11–100</span>
      <span style="padding:4px 12px;border-radius:20px;background:var(--bg2)">与LeaderBoard重叠：<strong style="color:${overlapColor}">${overlapPct}%</strong>（目标&lt;30%）</span>
    </div>`;

    h+=`<div class="card"><div class="card-head">Watchlist Top20 — 潜在领导股
      <span class="sub">0.40×Mom + 0.30×TH + 0.20×RankVel + 0.10×MomAccel</span>
    </div><div class="card-body"><div class="tbl-wrap"><table>
      <thead><tr>
        <th>当前#</th><th>代码 / 板块</th><th>晋升分</th>
        <th>排名变化<br><span style="font-weight:400;font-size:10px">5日 / 20日</span></th>
        <th>排名速度</th><th>动量加速</th><th>健康度</th><th>操作</th>
      </tr></thead><tbody>`;

    wl.forEach(s=>{
      const rv=s.rank_velocity||50, rvc=rv>55?'var(--green)':rv<45?'var(--red)':'var(--text3)', rvi=rv>55?'↑':rv<45?'↓':'→';
      const ma=s.mom_acceleration||50, mac=ma>55?'var(--green)':ma<45?'var(--red)':'var(--text3)', mai=ma>55?'⚡':ma<45?'📉':'→';
      const d5=s.rank_delta_5d||0, d20=s.rank_delta_20d||0;
      const d5c=d5>0?'var(--green)':d5<0?'var(--red)':'var(--text3)';
      const d20c=d20>0?'var(--green)':d20<0?'var(--red)':'var(--text3)';
      const isLeader=leaderSyms.has(s.symbol);
      h+=`<tr data-symbol="${s.symbol}"${isLeader?' style="opacity:0.55"':''}>
        <td style="color:var(--text3);font-weight:600">${s.rank}</td>
        <td><strong>${s.symbol}</strong>${isLeader?' <span style="font-size:9px;color:var(--amber)">★Leader</span>':''}
          <br><span style="font-size:10px;color:var(--text2)">${s.name||''}</span>
          <br><span class="pill" style="font-size:9px">${s.sector||'—'}</span></td>
        <td><span style="font-weight:700;color:${scCol(s.promotion_score||0)};font-size:14px">${p2(s.promotion_score,1)}</span>${scBar(s.promotion_score||0,'55px')}</td>
        <td><span style="color:${d5c}">${d5>0?'+'+d5:d5===0?'—':d5}</span> <span style="color:var(--text3)">/</span> <span style="color:${d20c}">${d20>0?'+'+d20:d20===0?'—':d20}</span></td>
        <td style="color:${rvc}">${rvi} <span style="font-size:11px">${p2(rv,0)}</span></td>
        <td style="color:${mac}">${mai} <span style="font-size:11px">${p2(ma,0)}</span></td>
        <td>${p2(s.trend_health,0)} ${scBar(s.trend_health||0,'45px')}</td>
        <td>${badge(s.trade_action||'HOLD')}</td>
      </tr>`;
    });
    h+=`</tbody></table></div></div></div>`;
    h+=`<div class="card"><div class="card-head">个股预览 <span class="sub">hover / tap 行切换</span></div><div class="card-body"><div id="wl-stock-preview"></div></div></div>`;
    h+=`<div class="card"><div class="card-head">晋升分排行</div><div class="card-body">
      <div class="cwrap" style="height:220px"><canvas id="cw-promo"></canvas></div>
    </div></div>`;

    const tp2=wl.filter(s=>(s.promotion_score||0)>=60);
    const rising=wl.filter(s=>(s.rank_velocity||50)>60).map(s=>s.symbol);
    h+=aiBox(
      `Watchlist ${wl.length} 只（Rank 11-100），晋升分≥60 共 ${tp2.length} 只，排名上升：${rising.slice(0,5).join('、')||'暂无'}。`,
      `与Leader Board重叠率 ${overlapPct}%（${overlapPct<30?'✅达标':'⚠️偏高'}）。排名速度高+动量加速 = 真正的潜在领导股。`,
      `${tp2.length>0?`重点关注 ${tp2.slice(0,3).map(s=>s.symbol).join('、')}，有望晋升 Top10。`:'历史快照积累中，1-2周后 Rank Velocity 将显示真实数据。'}`,
      tp2.length>0?`跟踪 ${tp2.slice(0,3).map(s=>s.symbol).join('、')} 排名变化，突破前高可考虑建仓`:'继续观察，等待历史数据积累'
    );
    $('s-watchlist').innerHTML=h;
    setTimeout(()=>{
      bindStockPreviewRows('#s-watchlist','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'wl-stock-preview');
      const el=$('cw-promo'); if(!el)return;
      if(charts.promo)charts.promo.destroy();
      const top15=[...wl].sort((a,b)=>(b.promotion_score||0)-(a.promotion_score||0)).slice(0,15);
      charts.promo=new Chart(el,{type:'bar',data:{
        labels:top15.map(s=>s.symbol),
        datasets:[{label:'晋升分',data:top15.map(s=>s.promotion_score||0),backgroundColor:top15.map(s=>scCol(s.promotion_score||0)),borderRadius:4}]
      },options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
        scales:{y:{min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},x:{ticks:{font:{size:11}},grid:{display:false}}}}});
    },80);
  }

  // ── Tab 4: Positions & Exit ───────────────────────────
  if (tab==='positions') {
    const bt=DATA.backtest;
    if(!bt){$('s-positions').innerHTML='<div class="error">backtest.json 未加载，请刷新或检查 GitHub Actions。</div>';return;}
    const vr=bt?.backtest?.results?.layer_d?.variant_results;
    const e1=vr?.E1_AUDITED_G4_MINHOLD10;
    if(!e1){$('s-positions').innerHTML='<div class="error">E1 variant 数据缺失。</div>';return;}

    // ── 日期元数据 ─────────────────────────────────────────
    const sv=e1.sample_validity||{};
    const simEndDate=sv.simulation_end_date||'—';          // 回测结束日
    const btAsOf=bt.generated_at_display||bt.generated_at||'—'; // backtest.json 生成时间
    const lbAsOf=DATA.market?.data_date||'—';              // leaderboard 数据日期
    // 日期错配：sim_end_date 与 leaderboard 日期超过 1 天
    const dateMismatch = (simEndDate!=='—' && lbAsOf!=='—' && simEndDate!==lbAsOf);

    const allTrades=e1.trades||[];
    const simEnd=allTrades.filter(t=>t.is_sim_end);
    const recentClosed=allTrades.filter(t=>!t.is_sim_end).slice(-5).reverse();
    const leaders=DATA.leaderboard||[];

    let h=`<div class="frozen-banner">
      <strong>E1_AUDITED_G4_MINHOLD10 (frozen)</strong> &nbsp;·&nbsp;
      Gate v2.1: slope + leadership &nbsp;·&nbsp;
      Exit: LS &lt; 60 → EXIT，MinHold 10 days &nbsp;·&nbsp;
      T-day signal, T+1 adverse execution
    </div>`;

    // ── 日期标注与错配警告 ─────────────────────────────────
    h+=`<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;font-size:12px">
      <span style="padding:4px 12px;border-radius:20px;background:var(--bg2)">
        Backtest as-of: <strong>${simEndDate}</strong>
      </span>
      <span style="padding:4px 12px;border-radius:20px;background:var(--bg2)">
        Leader Score as-of: <strong>${lbAsOf}</strong>
      </span>
      ${dateMismatch?`<span style="padding:4px 12px;border-radius:20px;background:rgba(226,75,74,0.12);color:var(--red);font-weight:600">
        ⚠️ DATE MISMATCH — LS from leaderboard may not match model positions
      </span>`:''}
    </div>`;

    // ── SIM_END 说明 ───────────────────────────────────────
    h+=`<div style="background:rgba(55,138,221,0.07);border:.5px solid rgba(55,138,221,0.25);border-radius:var(--radius);padding:8px 14px;font-size:12px;margin-bottom:12px;color:var(--text2)">
      ℹ️ <strong>E1 Model Positions</strong> — 以下为 E1 回测在模拟结束日（${simEndDate}）仍未平仓的模型仓位（SIM_END）。
      这不是用户实际持仓。OOS 阶段将由每日 E1 forward portfolio 文件替代。
    </div>`;

    // ── 持仓表 ─────────────────────────────────────────────
    h+=`<div class="card"><div class="card-head">E1 Model Positions <span class="sub">As of: ${simEndDate}</span></div><div class="card-body">`;
    if(simEnd.length>0){
      const posRows=simEnd.map(t=>{
        const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';
        const days=t.holding_days||0, minhold=Math.max(0,10-days);
        const lbEntry=leaders.find(s=>s.symbol===t.symbol);
        const curLS=lbEntry?.leader_score||t.leader_score_entry||0;
        const lsStale=dateMismatch?` <span style="font-size:10px;color:var(--red)">STALE</span>`:'';
        const exitStatus=curLS<60
          ?`<span class="badge-exit">EXIT</span>`
          :`<span class="badge-hold">HOLD</span>`;
        return `<tr data-symbol="${t.symbol}">
          <td><strong>${t.symbol}</strong></td>
          <td>${t.entry_date}</td>
          <td>${p2(t.entry_price||0)}</td>
          <td>${p2(t.exit_price||0)}</td>
          <td style="${rc}">${ret>=0?'+':''}${p2(ret)}%</td>
          <td>${days}</td>
          <td>${minhold>0?minhold+'d left':'✓ OK'}</td>
          <td style="color:${scCol(curLS)}">${p2(curLS,1)}${lsStale}</td>
          <td>${exitStatus}</td>
        </tr>`;
      }).join('');
      h+=`<div class="tbl-wrap"><table>
        <thead><tr><th>Symbol</th><th>Entry date</th><th>Entry $</th><th>Model exit $</th>
        <th>Return</th><th>Days held</th><th>MinHold</th>
        <th>LS ${dateMismatch?'(STALE)':'(current)'}</th><th>Signal</th></tr></thead>
        <tbody>${posRows}</tbody>
      </table></div>`;
    } else {
      h+=`<div style="padding:20px;color:var(--text2);text-align:center">
        模拟期内无未平仓仓位。OOS 阶段持仓将在此显示。
      </div>`;
    }
    h+=`</div></div>`;

    // ── 最近平仓 ───────────────────────────────────────────
    if(recentClosed.length>0){
      const recentRows=recentClosed.map(t=>{
        const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';
        return `<tr data-symbol="${t.symbol}">
          <td><strong>${t.symbol}</strong></td>
          <td>${t.entry_date}</td><td>${t.exit_date||'—'}</td>
          <td style="${rc}">${ret>=0?'+':''}${p2(ret)}%</td>
          <td>${t.holding_days||0}</td>
          <td style="font-size:11px;color:var(--text2)">${t.exit_reason||''}</td>
        </tr>`;
      }).join('');
      h+=`<div class="card"><div class="card-head">Recent closed trades (last 5)</div><div class="card-body">
        <div class="tbl-wrap"><table>
          <thead><tr><th>Symbol</th><th>Entry</th><th>Exit</th><th>Return</th><th>Days</th><th>Exit reason</th></tr></thead>
          <tbody>${recentRows}</tbody>
        </table></div>
      </div></div>`;
    }

    h+=`<p class="note" style="margin-top:8px">
      Days held 仅供参考。Exit signal: LS &lt; 60 → EXIT，T日确认 T+1执行。MinHold 10天保护期内不提前退出。
      LS 数值来自 leaderboard.json（${lbAsOf}），回测快照来自 backtest.json（${simEndDate}）。
    </p>`;
    h+=`<div class="card"><div class="card-head">个股预览 <span class="sub">hover / tap 持仓或平仓行切换</span></div><div class="card-body"><div id="pos-stock-preview"></div></div></div>`;
    $('s-positions').innerHTML=h;
    setTimeout(()=>{
      // 优先绑定持仓行；若无持仓，绑定最近平仓行
      const root=$('s-positions');
      const posRows=root?root.querySelectorAll('tr[data-symbol]'):[];
      if(posRows.length){
        bindStockPreviewRows('#s-positions','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'pos-stock-preview');
      }
    },80);
  }

  // ── Tab 5: Research & Backtest ────────────────────────
  if (tab==='research') {
    const bt=DATA.backtest, tlog=DATA.tradelog;
    if(!bt){$('s-research').innerHTML='<div class="error">backtest.json 未加载，请刷新或检查 GitHub Actions。</div>';return;}
    const vr=bt?.backtest?.results?.layer_d?.variant_results;
    const e1=vr?.E1_AUDITED_G4_MINHOLD10;
    if(!e1){$('s-research').innerHTML='<div class="error">E1 数据缺失。</div>';return;}

    const e1rPanel = renderE1RResearchPanel(vr);

    const pc=bt?.backtest?.results?.layer_d?.period_comparison||{};
    const pA=pc['A_2023_11_TO_2024_12']?.variants?.E1_AUDITED_G4_MINHOLD10||{};
    const pB=pc['B_2024_12_TO_2026_06']?.variants?.E1_AUDITED_G4_MINHOLD10||{};

    function impliedSpxReturn(row){
      const e1Ret=Number(row?.total_return_pct), alpha=Number(row?.alpha_pct);
      const src=row?.spx_total_return_pct;
      if(src!==null&&src!==undefined&&src!=='') return {value:src,implied:false};
      if(Number.isFinite(e1Ret)&&Number.isFinite(alpha)) return {value:e1Ret-alpha,implied:true};
      return {value:null,implied:false};
    }
    function fmtSpx(row){
      const r=impliedSpxReturn(row);
      if(r.value===null||r.value===undefined||r.value==='') return '—';
      return `${fmt(r.value)}${r.implied?' *':''}`;
    }

    const trades=(tlog?.trades||e1.trades||[]).slice(-20).reverse();
    const tradeRows=trades.map(t=>{
      const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';
      return `<tr>
        <td><strong>${t.symbol}</strong></td>
        <td>${t.entry_date}</td><td>${t.exit_date||'—'}</td>
        <td>${p2(t.entry_price||0)}</td><td>${p2(t.exit_price||0)}</td>
        <td style="${rc}">${ret>=0?'+':''}${p2(ret)}%</td>
        <td>${t.holding_days||0}</td>
        <td style="font-size:11px;color:var(--text2)">${t.exit_reason||''}</td>
        <td>${t.is_sim_end?'<span class="badge-sim">SIM</span>':''}</td>
      </tr>`;
    }).join('');

    const eqCurve=e1.equity_curve||[], spxCurve=e1.spx_curve||[];
    const e1rFormal=DATA.e1rFormal||{}, e1rCurve=e1rFormal.equity_curve||[];
    const oosRowsForNote=(DATA.oosEquity?.curve||[]);
    const oosLatestDate=oosRowsForNote.length ? (oosRowsForNote[oosRowsForNote.length-1].date||'—') : '—';

    // Lifecycle 统计迁入
    const lc=DATA.lifecycle||{}, regOrder=['Expansion','Mature','Speculative','Broken'];
    const lcStats=regOrder.map(r=>({reg:r,n:(lc[r]||[]).length,zh:REG_META[r]?.zh||r}));

    let h=e1rPanel + `<div class="frozen-banner">
      <strong>E1_AUDITED_G4_MINHOLD10 — 正式冻结 2026-06-16</strong> &nbsp;·&nbsp;
      Gate v2.1: slope + leadership &nbsp;·&nbsp;
      Shock 已排除（2025-10-10 SNDK 路径依赖）&nbsp;·&nbsp;
      样本内不再修改
    </div>`;

    h+=`<div class="grid-4" style="margin-bottom:1rem">
      <div class="mc"><div class="mc-label">Full return</div><div class="mc-val" style="color:var(--green)">${fmt(e1.total_return_pct)}</div></div>
      <div class="mc"><div class="mc-label">Max drawdown</div><div class="mc-val" style="color:var(--red)">${p2(e1.max_drawdown_pct)}%</div></div>
      <div class="mc"><div class="mc-label">Profit factor</div><div class="mc-val">${p2(e1.profit_factor)}</div></div>
      <div class="mc"><div class="mc-label">Sharpe</div><div class="mc-val">${p2(e1.sharpe_ratio)}</div></div>
      <div class="mc"><div class="mc-label">Win rate</div><div class="mc-val">${p2(e1.win_rate_pct)}%</div></div>
      <div class="mc"><div class="mc-label">Trades</div><div class="mc-val">${e1.number_of_trades||0}</div></div>
      <div class="mc"><div class="mc-label">Avg hold</div><div class="mc-val">${p2(e1.avg_holding_days,1)}d</div></div>
      <div class="mc"><div class="mc-label">Exposure</div><div class="mc-val">${p2(e1.exposure_pct)}%</div></div>
    </div>`;

    if(eqCurve.length>1){
      h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Equity curve — E1 vs E1-R vs SPX (indexed to 100)</div><div class="card-body">
        <div class="cwrap" style="height:220px"><canvas id="cw-equity"></canvas></div>
        <div class="muted" style="font-size:12px;margin-top:.5rem">Equity includes SIM_END open positions marked to market. Backtest ends: ${e1.sample_validity?.simulation_end_date||'—'} · OOS latest: ${oosLatestDate} · E1-R OOS tracking: not yet completed.</div>
      </div></div>`;
    }

    // Stage 3.8E-1: removed old period table from this tab.

    if(lcStats.some(r=>r.n>0)){
      h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">个股趋势生命周期分布 <span class="sub">Top50 当前象限</span></div><div class="card-body">
        <div class="regime-grid">`;
      lcStats.forEach(({reg,n,zh})=>{
        const stocks=lc[reg]||[];
        h+=`<div class="regime-cell badge-${reg}">
          <div style="font-size:13px;font-weight:600;margin-bottom:4px">${zh} <span style="font-size:20px;font-weight:700">${n}</span></div>
          <div style="font-size:11px;opacity:.8;margin-bottom:6px">${REG_META[reg]?.desc||''}</div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">
            ${stocks.slice(0,5).map(s=>`<span style="font-size:10px;background:rgba(255,255,255,0.25);padding:1px 6px;border-radius:10px;font-weight:500">${s.symbol}</span>`).join('')}
            ${stocks.length>5?`<span style="font-size:10px;opacity:.6">+${stocks.length-5}</span>`:''}
          </div>
        </div>`;
      });
      h+=`</div></div></div>`;
    }

    h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Trade log — recent 20 trades</div><div class="card-body">
      <div class="tbl-wrap"><table>
        <thead><tr><th>Symbol</th><th>Entry</th><th>Exit</th><th>Entry $</th><th>Exit $</th><th>Return</th><th>Days</th><th>Exit reason</th><th>SIM?</th></tr></thead>
        <tbody>${tradeRows}</tbody>
      </table></div>
    </div></div>`;

    // Stage 3.8E-1: keep only market context below the trade table.
    const nativeMarket = DATA.market || {};
    const nativeMarketState =
      nativeMarket.market_state ||
      nativeMarket.state ||
      nativeMarket.regime ||
      nativeMarket.current_regime ||
      nativeMarket.market_regime ||
      nativeMarket.trend_state ||
      '—';
    const nativeMarketDate =
      nativeMarket.data_date ||
      nativeMarket.date ||
      nativeMarket.status_date ||
      nativeMarket.generated_at_display ||
      nativeMarket.generated_at ||
      '—';
    const nativeMarketScore =
      nativeMarket.market_score ??
      nativeMarket.score ??
      nativeMarket.total_score ??
      '—';
    const nativeLeadership =
      nativeMarket.leadership_count ??
      nativeMarket.leadership ??
      nativeMarket.leaders_count ??
      '—';

    h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Market State</div><div class="card-body">
      <div class="grid-4">
        <div class="mc"><div class="mc-label">State</div><div class="mc-val">${nativeMarketState}</div></div>
        <div class="mc"><div class="mc-label">Data date</div><div class="mc-val">${nativeMarketDate}</div></div>
        <div class="mc"><div class="mc-label">Market score</div><div class="mc-val">${nativeMarketScore}</div></div>
        <div class="mc"><div class="mc-label">Leadership</div><div class="mc-val">${nativeLeadership}</div></div>
      </div>
      <div class="muted" style="font-size:12px;margin-top:.5rem">
        Stage 3.8E-1 cleanup: Trade Log is followed only by Market State. E1/E1R strategy logic is unchanged.
      </div>
    </div></div>`;


    // Stage 3.8E-1: removed OOS note below trade table.

    // Stage 3.8E-1: removed archived E2 note below trade table.

    h+=`<p class="note">执行模型：T日收盘信号 → T+1逆向成交（BUY at high, EXIT at low）· 单边成本 0.10% · 最大持仓 3</p>`;
    $('s-research').innerHTML=h;

    if(eqCurve.length>1){
      setTimeout(()=>{
        const el=$('cw-equity'); if(!el)return;
        if(charts.equity)charts.equity.destroy();

        const e1Start=eqCurve[0]||1, spxStart=spxCurve[0]||1, e1rStart=e1rCurve[0]||1;
        const e1I=eqCurve.map(v=>parseFloat(((v/e1Start)*100).toFixed(2)));
        const spxI=spxCurve.map(v=>parseFloat(((v/spxStart)*100).toFixed(2)));
        const e1rI=e1rCurve.map(v=>parseFloat(((v/e1rStart)*100).toFixed(2)));

        const buildEquityDateLabels = (n) => {
          const sv = e1.sample_validity || {};
          const startDate = sv.simulation_start_date || e1.simulation_start_date || null;
          const endDate = sv.simulation_end_date || e1.simulation_end_date || null;

          if(!startDate || !endDate || n <= 1){
            return Array.from({length:n}, (_, i) => String(i));
          }

          const startMs = new Date(startDate + "T00:00:00Z").getTime();
          const endMs = new Date(endDate + "T00:00:00Z").getTime();

          if(!Number.isFinite(startMs) || !Number.isFinite(endMs) || endMs <= startMs){
            return Array.from({length:n}, (_, i) => String(i));
          }

          return Array.from({length:n}, (_, i) => {
            const t = startMs + (endMs - startMs) * i / (n - 1);
            return new Date(t).toISOString().slice(0, 10);
          });
        };

        const btLabels = buildEquityDateLabels(eqCurve.length);

        const oosRows = (DATA.oosEquity?.curve || [])
          .filter(r => r && r.date && r.equity != null);

        const oosDates = oosRows.map(r => String(r.date));
        const extraOosDates = oosDates.filter(d => !btLabels.includes(d));
        const labels = btLabels.concat(extraOosDates);

        const padAfter = labels.length - btLabels.length;
        const pad = n => Array.from({length:n}, () => null);

        const e1BacktestData = e1I.concat(pad(padAfter));
        const spxData = spxI.concat(pad(padAfter));
        const e1rData = e1rI.concat(pad(Math.max(0, labels.length - e1rI.length)));

        // Extend SPX benchmark through OOS using Market Overview SPX chart.
        // This keeps SPX buy & hold comparable with E1 OOS forward.
        const spxAnchor = spxI[spxI.length-1] || 100;
        const spxIx = DATA.market?.indices?.SPX || {};
        const spxChartDates = spxIx.chart_dates || [];
        const spxChartPrices = spxIx.chart_prices || [];
        const btEndDate = e1.sample_validity?.simulation_end_date || labels[btLabels.length-1];

        if(spxChartDates.length && spxChartPrices.length && btEndDate){
          let baseIdx = spxChartDates.findIndex(d => String(d) >= String(btEndDate));
          if(baseIdx < 0) baseIdx = spxChartDates.length - 1;

          const baseClose = Number(spxChartPrices[baseIdx] || 0);
          if(baseClose > 0){
            spxData[btLabels.length-1] = spxAnchor;
            labels.forEach((d, idx) => {
              if(idx < btLabels.length) return;
              const j = spxChartDates.indexOf(String(d));
              if(j >= 0){
                spxData[idx] = parseFloat(((Number(spxChartPrices[j] || 0) / baseClose) * spxAnchor).toFixed(2));
              }
            });
          }
        }

        const e1Anchor = e1I[e1I.length-1] || 100;
        const oosStartEquity = Number(oosRows[0]?.equity || 0) || 1;
        const oosForwardData = Array.from({length:labels.length}, () => null);

        if(oosRows.length){
          oosForwardData[btLabels.length-1] = e1Anchor;
          oosRows.forEach(r => {
            const idx = labels.indexOf(String(r.date));
            if(idx >= 0){
              oosForwardData[idx] = parseFloat(((Number(r.equity || 0) / oosStartEquity) * e1Anchor).toFixed(2));
            }
          });
        }

        const oosStartDate = oosDates[0] || null;
        const oosStartIndex = oosStartDate ? labels.indexOf(oosStartDate) : -1;

        const shortDate = v => String(v).slice(2, 7);

        const ds=[
          {label:'E1 backtest',data:e1BacktestData,borderColor:'#1D9E75',backgroundColor:'rgba(29,158,117,0.06)',borderWidth:2,pointRadius:0,tension:0.2,fill:true},
          {label:'SPX buy & hold',data:spxData,borderColor:'#888',backgroundColor:'transparent',borderWidth:1.5,borderDash:[4,3],pointRadius:0,tension:0.2},
        ];

        if(oosRows.length){
          ds.splice(1,0,{label:'E1 OOS forward',data:oosForwardData,borderColor:'#1D9E75',backgroundColor:'transparent',borderWidth:2,borderDash:[6,4],pointRadius:0,tension:0.2,spanGaps:false});
        }

        if(e1rI.length>1){
          ds.splice(oosRows.length?2:1,0,{label:'E1-R backtest',data:e1rData,borderColor:'#D4537E',backgroundColor:'transparent',borderWidth:2,pointRadius:0,tension:0.2});
        }

        const oosLinePlugin = {
          id:'oosStartLine',
          afterDraw(chart){
            if(oosStartIndex < 0) return;
            const {ctx, chartArea, scales} = chart;
            if(!chartArea || !scales?.x) return;
            const x = scales.x.getPixelForValue(oosStartIndex);
            ctx.save();
            ctx.beginPath();
            ctx.setLineDash([4,4]);
            ctx.strokeStyle = 'rgba(255,255,255,0.45)';
            ctx.lineWidth = 1;
            ctx.moveTo(x, chartArea.top);
            ctx.lineTo(x, chartArea.bottom);
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = 'rgba(255,255,255,0.65)';
            ctx.font = '10px sans-serif';
            ctx.fillText('OOS start', x + 6, chartArea.top + 12);
            ctx.restore();
          }
        };

        charts.equity=new Chart(el,{type:'line',data:{
          labels,
          datasets:ds
        },options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
          plugins:{
            legend:{labels:{font:{size:10},boxWidth:10,padding:8}},
            tooltip:{callbacks:{title:items=>labels[items[0].dataIndex]||''}}
          },
          scales:{
            x:{
              display:true,
              ticks:{
                font:{size:10},
                maxTicksLimit:8,
                callback:function(value){
                  return shortDate(this.getLabelForValue(value));
                }
              },
              grid:{display:false}
            },
            y:{ticks:{font:{size:10},callback:v=>v.toFixed(0)},grid:{color:'rgba(128,128,128,0.1)'}}
          }
        },plugins:[oosLinePlugin]});
      },80);
    }
  }

} // end render()

loadAll();

/* === E1R_V0_2_DASHBOARD_MODULE_STAGE_3_4_CLEAN_INTEGRATION === */
(function () {
  "use strict";

  const E1R_V02_PATHS = {
    status: "../exports/e1r_v0_2_status.json",
    oosSummary: "../exports/oos_e1r_v0_2_summary.json",
    sidecar: "../exports/oos_e1r_v0_2_sidecar.json",
    positions: "../exports/oos_e1r_v0_2_positions.json",
    orders: "../exports/oos_e1r_v0_2_orders.json",
    oosEquity: "../exports/oos_e1r_v0_2_equity_curve.json",
    lifecycle: "../exports/oos_e1r_v0_2_sidecar_lifecycle.json",
    turnover: "../exports/oos_e1r_v0_2_sidecar_turnover.json",
    backtestSummary: "../exports/e1r_v0_2_backtest_summary.json",
    backtestEquity: "../exports/e1r_v0_2_backtest_equity_curve.json"
  };

  const E1R_V02_CLASSES = {
    statusCard: "e1r-oos-card",
    equityCard: "e1r-oos-equity-card",
    backtestCard: "e1r-backtest-card",
    grid: "e1r-oos-grid"
  };

  function e1rEscapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function e1rNumber(value, digits = 2) {
    const num = Number(value);
    if (!Number.isFinite(num)) return "N/A";
    return num.toLocaleString(undefined, { maximumFractionDigits: digits, minimumFractionDigits: digits });
  }

  function e1rPercent(value, digits = 2) {
    const num = Number(value);
    if (!Number.isFinite(num)) return "N/A";
    const scaled = Math.abs(num) <= 1 ? num * 100 : num;
    return `${scaled.toFixed(digits)}%`;
  }

  function e1rPick(obj, keys, fallback = "N/A") {
    for (const key of keys) {
      if (obj && Object.prototype.hasOwnProperty.call(obj, key) && obj[key] !== null && obj[key] !== undefined && obj[key] !== "") {
        return obj[key];
      }
    }
    return fallback;
  }

  function e1rAsArray(payload) {
    if (Array.isArray(payload)) return payload;
    if (!payload || typeof payload !== "object") return [];
    for (const key of ["records", "data", "items", "rows", "equity_curve", "curve", "positions", "orders", "trades"]) {
      if (Array.isArray(payload[key])) return payload[key];
    }
    return [];
  }

  function e1rLatest(payload) {
    const arr = e1rAsArray(payload);
    if (arr.length) return arr[arr.length - 1] || {};
    if (payload && typeof payload === "object") {
      return payload.latest || payload.summary || payload.status || payload;
    }
    return {};
  }

  async function e1rFetchJson(path) {
    try {
      const sep = path.includes("?") ? "&" : "?";
      const response = await fetch(`${path}${sep}_=${Date.now()}`, { cache: "no-store" });
      if (!response.ok) {
        return { ok: false, path, status: response.status, data: null };
      }
      return { ok: true, path, status: response.status, data: await response.json() };
    } catch (error) {
      return { ok: false, path, status: "FETCH_ERROR", data: null, error: String(error && error.message ? error.message : error) };
    }
  }

  function e1rFindTarget(preferredIds) {
    for (const id of preferredIds) {
      const el = document.getElementById(id);
      if (el) return el;
    }

    const candidates = [
      "[data-tab-content='market']",
      "[data-tab-content='market-overview']",
      "[data-tab-content='research']",
      "[data-tab-content='research-backtest']",
      ".tab-content.active",
      ".content",
      "main",
      "body"
    ];

    for (const selector of candidates) {
      const el = document.querySelector(selector);
      if (el) return el;
    }

    return document.body;
  }

  function e1rCreateOrGetPanel(id, title, targetIds, className) {
    let panel = document.getElementById(id);
    if (panel) return panel;

    const target = e1rFindTarget(targetIds);
    panel = document.createElement("section");
    panel.id = id;
    panel.className = className || E1R_V02_CLASSES.statusCard;
    panel.setAttribute("data-e1r-v02-panel", "true");

    const header = document.createElement("div");
    header.className = "e1r-v02-panel-header";
    header.innerHTML = `<h3>${e1rEscapeHtml(title)}</h3><span class="e1r-v02-badge">paper tracking</span>`;

    const body = document.createElement("div");
    body.className = "e1r-v02-panel-body";
    body.setAttribute("data-e1r-v02-body", id);

    panel.appendChild(header);
    panel.appendChild(body);
    target.appendChild(panel);

    return panel;
  }

  function e1rMetric(label, value) {
    return `<div class="e1r-v02-metric"><span>${e1rEscapeHtml(label)}</span><strong>${e1rEscapeHtml(value)}</strong></div>`;
  }

  function e1rRenderUnavailable(panel, title, result) {
    const body = panel.querySelector("[data-e1r-v02-body]");
    body.innerHTML = `
      <div class="e1r-v02-note">
        ${e1rEscapeHtml(title)} unavailable: ${e1rEscapeHtml(result.status || "missing export")}
      </div>
    `;
  }

  function e1rRenderStatus(statusResult, summaryResult, sidecarResult) {
    const panel = e1rCreateOrGetPanel(
      "e1r-v02-status-panel",
      "E1R v0.2 Market / OOS Status",
      ["market-overview", "marketOverview", "market", "overview", "research-backtest"],
      E1R_V02_CLASSES.statusCard
    );

    if (!statusResult.ok && !summaryResult.ok) {
      e1rRenderUnavailable(panel, "E1R v0.2 status", statusResult);
      return;
    }

    const status = e1rLatest(statusResult.data);
    const summary = e1rLatest(summaryResult.data);
    const sidecar = e1rLatest(sidecarResult.data);

    const statusDate = e1rPick(status, ["status_date", "latest_date", "date", "as_of"], e1rPick(summary, ["status_date", "latest_date", "date", "as_of"]));
    const marketState = e1rPick(status, ["market_state", "state", "regime", "e1r_market_state"]);
    const coreActive = e1rPick(status, ["core_active", "is_core_active"], e1rPick(summary, ["core_active", "is_core_active"]));
    const sidecarActive = e1rPick(status, ["sidecar_active", "is_sidecar_active"], e1rPick(sidecar, ["sidecar_active", "is_sidecar_active"]));
    const selectedCount = e1rPick(status, ["sidecar_selected_count", "selected_count"], e1rPick(sidecar, ["selected_count", "sidecar_selected_count"], "0"));
    const trackingMode = e1rPick(status, ["tracking_mode", "execution_mode", "mode"], e1rPick(summary, ["tracking_mode", "execution_mode", "mode"], "PAPER_TRACKING_NO_REAL_EXECUTION"));

    const body = panel.querySelector("[data-e1r-v02-body]");
    body.innerHTML = `
      <div class="${E1R_V02_CLASSES.grid}">
        ${e1rMetric("Status date", statusDate)}
        ${e1rMetric("Market state", marketState)}
        ${e1rMetric("Core active", coreActive)}
        ${e1rMetric("Sidecar active", sidecarActive)}
        ${e1rMetric("Sidecar selected", selectedCount)}
        ${e1rMetric("Mode", trackingMode)}
      </div>
      <div class="e1r-v02-note">E1R v0.2 is shown as paper tracking only. No broker execution is connected from this dashboard module.</div>
    `;
  }

  function e1rRenderBacktest(summaryResult, equityResult) {
    const panel = e1rCreateOrGetPanel(
      "e1r-v02-backtest-panel",
      "E1R v0.2 5Y Backtest",
      ["research-backtest", "research", "backtest", "market-overview"],
      E1R_V02_CLASSES.backtestCard
    );

    if (!summaryResult.ok && !equityResult.ok) {
      e1rRenderUnavailable(panel, "E1R v0.2 backtest", summaryResult);
      return;
    }

    const summary = e1rLatest(summaryResult.data);
    const equityRows = e1rAsArray(equityResult.data);
    const latest = equityRows.length ? equityRows[equityRows.length - 1] : {};

    const totalReturn = e1rPick(summary, ["total_return", "return", "strategy_return"], e1rPick(latest, ["total_return", "return"]));
    const spxReturn = e1rPick(summary, ["spx_return", "benchmark_return"]);
    const alpha = e1rPick(summary, ["alpha", "excess_return"]);
    const maxDd = e1rPick(summary, ["max_drawdown", "max_dd"]);
    const sharpe = e1rPick(summary, ["sharpe", "sharpe_ratio"]);
    const pf = e1rPick(summary, ["profit_factor", "pf"]);
    const sidecarDays = e1rPick(summary, ["sidecar_active_days", "sidecar_days"]);

    const body = panel.querySelector("[data-e1r-v02-body]");
    body.innerHTML = `
      <div class="${E1R_V02_CLASSES.grid}">
        ${e1rMetric("Total return", typeof totalReturn === "number" ? e1rPercent(totalReturn) : totalReturn)}
        ${e1rMetric("SPX return", typeof spxReturn === "number" ? e1rPercent(spxReturn) : spxReturn)}
        ${e1rMetric("Alpha", typeof alpha === "number" ? e1rPercent(alpha) : alpha)}
        ${e1rMetric("MaxDD", typeof maxDd === "number" ? e1rPercent(maxDd) : maxDd)}
        ${e1rMetric("Sharpe", typeof sharpe === "number" ? e1rNumber(sharpe) : sharpe)}
        ${e1rMetric("Profit factor", typeof pf === "number" ? e1rNumber(pf) : pf)}
        ${e1rMetric("Sidecar days", sidecarDays)}
        ${e1rMetric("Equity rows", equityRows.length)}
      </div>
    `;
  }

  function e1rRenderOosEquity(equityResult, lifecycleResult, turnoverResult) {
    const panel = e1rCreateOrGetPanel(
      "e1r-v02-oos-equity-panel",
      "E1R v0.2 Forward / OOS Equity",
      ["positions-exit", "positions", "research-backtest", "research", "market-overview"],
      E1R_V02_CLASSES.equityCard
    );

    if (!equityResult.ok) {
      e1rRenderUnavailable(panel, "E1R v0.2 OOS equity", equityResult);
      return;
    }

    const rows = e1rAsArray(equityResult.data);
    const latest = rows.length ? rows[rows.length - 1] : e1rLatest(equityResult.data);
    const lifecycle = e1rLatest(lifecycleResult.data);
    const turnover = e1rLatest(turnoverResult.data);

    const latestDate = e1rPick(latest, ["date", "status_date", "as_of"]);
    const equity = e1rPick(latest, ["equity", "combined_equity", "portfolio_value"]);
    const coreEquity = e1rPick(latest, ["core_equity"]);
    const sidecarEquity = e1rPick(latest, ["sidecar_equity"]);
    const mtmStatus = e1rPick(latest, ["mtm_status", "sidecar_mtm_status"], e1rPick(lifecycle, ["lifecycle_status"], "N/A"));
    const turnoverCount = e1rPick(turnover, ["turnover", "turnover_count", "changed_count"], "N/A");

    const body = panel.querySelector("[data-e1r-v02-body]");
    body.innerHTML = `
      <div class="${E1R_V02_CLASSES.grid}">
        ${e1rMetric("Latest date", latestDate)}
        ${e1rMetric("Combined equity", typeof equity === "number" ? e1rNumber(equity) : equity)}
        ${e1rMetric("Core equity", typeof coreEquity === "number" ? e1rNumber(coreEquity) : coreEquity)}
        ${e1rMetric("Sidecar equity", typeof sidecarEquity === "number" ? e1rNumber(sidecarEquity) : sidecarEquity)}
        ${e1rMetric("MTM / Lifecycle", mtmStatus)}
        ${e1rMetric("Turnover", turnoverCount)}
        ${e1rMetric("Rows", rows.length)}
      </div>
    `;
  }

  async function e1rRenderAll() {
    /*
     * Stage 3.8E-1:
     * Standalone E1R v0.2 panels are disabled.
     * Future E1R display integration must happen inside native Research & Backtest render flow.
     */
    window.__E1R_V02_STANDALONE_PANELS_DISABLED_STAGE_3_8E1__ = true;
    return;
    if (!document || !document.body) return;

    const [
      statusResult,
      summaryResult,
      sidecarResult,
      positionsResult,
      ordersResult,
      oosEquityResult,
      lifecycleResult,
      turnoverResult,
      backtestSummaryResult,
      backtestEquityResult
    ] = await Promise.all([
      e1rFetchJson(E1R_V02_PATHS.status),
      e1rFetchJson(E1R_V02_PATHS.oosSummary),
      e1rFetchJson(E1R_V02_PATHS.sidecar),
      e1rFetchJson(E1R_V02_PATHS.positions),
      e1rFetchJson(E1R_V02_PATHS.orders),
      e1rFetchJson(E1R_V02_PATHS.oosEquity),
      e1rFetchJson(E1R_V02_PATHS.lifecycle),
      e1rFetchJson(E1R_V02_PATHS.turnover),
      e1rFetchJson(E1R_V02_PATHS.backtestSummary),
      e1rFetchJson(E1R_V02_PATHS.backtestEquity)
    ]);

    e1rRenderStatus(statusResult, summaryResult, sidecarResult);
    e1rRenderBacktest(backtestSummaryResult, backtestEquityResult);
    e1rRenderOosEquity(oosEquityResult, lifecycleResult, turnoverResult);

    window.__E1R_V02_DASHBOARD_LAST_RESULT__ = {
      status: statusResult.ok,
      oosSummary: summaryResult.ok,
      sidecar: sidecarResult.ok,
      positions: positionsResult.ok,
      orders: ordersResult.ok,
      oosEquity: oosEquityResult.ok,
      lifecycle: lifecycleResult.ok,
      turnover: turnoverResult.ok,
      backtestSummary: backtestSummaryResult.ok,
      backtestEquity: backtestEquityResult.ok
    };
  }

  function e1rInit() {
    if (window.__E1R_V02_DASHBOARD_INITIALIZED__) return;
    window.__E1R_V02_DASHBOARD_INITIALIZED__ = true;
    e1rRenderAll();
  }

  window.E1RV02Dashboard = {
    init: e1rInit,
    renderAll: e1rRenderAll,
    paths: E1R_V02_PATHS
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", e1rInit);
  } else {
    e1rInit();
  }
})();
/* === END E1R_V0_2_DASHBOARD_MODULE_STAGE_3_4_CLEAN_INTEGRATION === */