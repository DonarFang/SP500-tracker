/**
 * SP500 Trend Decision Support Cockpit — app.js v2.0
 * 5 tabs: Market Overview / Leader Board / Watchlist / Positions & Exit / Research & Backtest
 */

const EXPORTS_BASE = 'https://donarfang.github.io/SP500-tracker/exports';
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

let DATA = {market:null,leaderboard:null,watchlist:null,lifecycle:null,health:null,backtest:null,tradelog:null};
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

async function fetchJ(name) {
  const r = await fetch(`${EXPORTS_BASE}/${name}.json?t=${Date.now()}`);
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
    const [wl,lc,dh,bt,tlog] = await Promise.all([
      fetchJ('watchlist').catch(()=>({watchlist:[]})),
      fetchJ('lifecycle').catch(()=>({regimes:{}})),
      fetchJ('data_health').catch(()=>null),
      fetchJ('backtest').catch(()=>null),
      fetchJ('trade_log').catch(()=>null),
    ]);
    DATA.watchlist=wl.watchlist||[]; DATA.lifecycle=lc.regimes||{};
    DATA.health=dh; DATA.backtest=bt; DATA.tradelog=tlog;

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

// ═══════════════════════════════════════════════════════
// render dispatcher
// ═══════════════════════════════════════════════════════
function render(tab) {

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
      h+=`<tr>
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
      h+=`<tr${isLeader?' style="opacity:0.55"':''}>
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
        return `<tr>
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
        return `<tr>
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
    $('s-positions').innerHTML=h;
  }

  // ── Tab 5: Research & Backtest ────────────────────────
  if (tab==='research') {
    const bt=DATA.backtest, tlog=DATA.tradelog;
    if(!bt){$('s-research').innerHTML='<div class="error">backtest.json 未加载，请刷新或检查 GitHub Actions。</div>';return;}
    const vr=bt?.backtest?.results?.layer_d?.variant_results;
    const e1=vr?.E1_AUDITED_G4_MINHOLD10;
    if(!e1){$('s-research').innerHTML='<div class="error">E1 数据缺失。</div>';return;}

    const pc=bt?.backtest?.results?.layer_d?.period_comparison||{};
    const pA=pc['A_2023_11_TO_2024_12']?.variants?.E1_AUDITED_G4_MINHOLD10||{};
    const pB=pc['B_2024_12_TO_2026_06']?.variants?.E1_AUDITED_G4_MINHOLD10||{};

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

    // Lifecycle 统计迁入
    const lc=DATA.lifecycle||{}, regOrder=['Expansion','Mature','Speculative','Broken'];
    const lcStats=regOrder.map(r=>({reg:r,n:(lc[r]||[]).length,zh:REG_META[r]?.zh||r}));

    let h=`<div class="frozen-banner">
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
      h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Equity curve — E1 vs SPX (indexed to 100)</div><div class="card-body">
        <div class="cwrap" style="height:220px"><canvas id="cw-equity"></canvas></div>
      </div></div>`;
    }

    h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Period comparison</div><div class="card-body">
      <div class="tbl-wrap"><table>
        <thead><tr><th>Period</th><th>E1 return</th><th>SPX</th><th>Alpha</th><th>MaxDD</th><th>PF</th><th>Sharpe</th><th>Trades</th></tr></thead>
        <tbody>
          <tr><td>A (Nov '23 – Dec '24)</td>
            <td style="color:var(--green)">${fmt(pA.total_return_pct)}</td><td>${fmt(pA.spx_total_return_pct)}</td>
            <td style="color:${parseFloat(pA.alpha_pct||0)>=0?'var(--green)':'var(--red)'}">${fmt(pA.alpha_pct)}</td>
            <td>${p2(pA.max_drawdown_pct)}%</td><td>${p2(pA.profit_factor)}</td><td>${p2(pA.sharpe_ratio)}</td><td>${pA.number_of_trades||0}</td></tr>
          <tr><td>B (Dec '24 – Jun '26)</td>
            <td style="color:var(--green)">${fmt(pB.total_return_pct)}</td><td>${fmt(pB.spx_total_return_pct)}</td>
            <td style="color:${parseFloat(pB.alpha_pct||0)>=0?'var(--green)':'var(--red)'}">${fmt(pB.alpha_pct)}</td>
            <td>${p2(pB.max_drawdown_pct)}%</td><td>${p2(pB.profit_factor)}</td><td>${p2(pB.sharpe_ratio)}</td><td>${pB.number_of_trades||0}</td></tr>
          <tr style="font-weight:600"><td>Full (Nov '23 – Jun '26)</td>
            <td style="color:var(--green)">${fmt(e1.total_return_pct)}</td><td>${fmt(e1.spx_total_return_pct)}</td>
            <td style="color:${parseFloat(e1.alpha_pct||0)>=0?'var(--green)':'var(--red)'}">${fmt(e1.alpha_pct)}</td>
            <td>${p2(e1.max_drawdown_pct)}%</td><td>${p2(e1.profit_factor)}</td><td>${p2(e1.sharpe_ratio)}</td><td>${e1.number_of_trades||0}</td></tr>
        </tbody>
      </table></div>
    </div></div>`;

    // Lifecycle stats migrated here
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

    h+=`<div class="oos-banner">
      <strong>OOS log — 从 2026-06-16 起</strong> &nbsp;·&nbsp;
      只追加不回写 &nbsp;·&nbsp;
      至少积累 6个月或 20 笔完整交易后才做第一次验收 &nbsp;·&nbsp;
      OOS 期间 E1 参数冻结
    </div>`;
    h+=`<div class="arch-banner">
      <strong>E2 Dynamic Exit — 已归档</strong> &nbsp;·&nbsp;
      V2 全面失败（Full −21.9%，MaxDD 51.1%，PF 0.83）&nbsp;·&nbsp;
      不开发 E3 &nbsp;·&nbsp; 修改须建立新候选版本，不覆盖 E1 基准
    </div>`;
    h+=`<p class="note">执行模型：T日收盘信号 → T+1逆向成交（BUY at high, EXIT at low）· 单边成本 0.10% · 最大持仓 3</p>`;
    $('s-research').innerHTML=h;

    if(eqCurve.length>1){
      setTimeout(()=>{
        const el=$('cw-equity'); if(!el)return;
        if(charts.equity)charts.equity.destroy();
        const e1Start=eqCurve[0]||1, spxStart=spxCurve[0]||1;
        const e1I=eqCurve.map(v=>parseFloat(((v/e1Start)*100).toFixed(2)));
        const spxI=spxCurve.map(v=>parseFloat(((v/spxStart)*100).toFixed(2)));
        charts.equity=new Chart(el,{type:'line',data:{
          labels:eqCurve.map((_,i)=>i),
          datasets:[
            {label:'E1 strategy',data:e1I,borderColor:'#1D9E75',backgroundColor:'rgba(29,158,117,0.06)',borderWidth:2,pointRadius:0,tension:0.2,fill:true},
            {label:'SPX buy & hold',data:spxI,borderColor:'#888',backgroundColor:'transparent',borderWidth:1.5,borderDash:[4,3],pointRadius:0,tension:0.2},
          ]
        },options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
          plugins:{legend:{labels:{font:{size:10},boxWidth:10,padding:8}}},
          scales:{x:{display:false},y:{ticks:{font:{size:10},callback:v=>v.toFixed(0)},grid:{color:'rgba(128,128,128,0.1)'}}}
        }});
      },80);
    }
  }

} // end render()

loadAll();
