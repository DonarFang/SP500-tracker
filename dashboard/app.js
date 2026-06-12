/**
 * SP500 Trend Decision Support Cockpit — app.js v1.3 Rev.2
 */

const EXPORTS_BASE = 'https://donarfang.github.io/SP500-tracker/exports';
const PALETTE = ['#378ADD','#1D9E75','#D85A30','#7F77DD','#BA7517','#D4537E','#639922','#5DCAA5','#E24B4A','#EF9F27'];
const TS_COLOR = {'Strong Expansion':'#1D9E75','Healthy Trend':'#378ADD','Mature Trend':'#BA7517','Weakening Trend':'#D85A30','Broken Trend':'#993C1D'};
const TS_ZH    = {'Strong Expansion':'强势扩张','Healthy Trend':'健康趋势','Mature Trend':'趋势成熟','Weakening Trend':'趋势减弱','Broken Trend':'趋势破坏'};
const REG_META = {
  Expansion:  {zh:'扩张期',desc:'高TH+高动量 — 最佳持有',cls:'badge-Expansion'},
  Mature:     {zh:'成熟期',desc:'高TH+低动量 — 观察减速',cls:'badge-Mature'},
  Speculative:{zh:'投机期',desc:'低TH+高动量 — 短线机会',cls:'badge-Speculative'},
  Broken:     {zh:'破坏期',desc:'低TH+低动量 — 规避风险',cls:'badge-Broken'},
};
const IDX_ICONS = {SPX:'📊',NDX:'💻',VIX:'😨',SOX:'🔬'};

let DATA = {market:null,leaderboard:null,watchlist:null,trades:null,lifecycle:null,health:null};
let charts = {};
let selectedStock = null;

const $  = id => document.getElementById(id);
const p2 = (v,d=2) => parseFloat(v||0).toFixed(d);
const sgn = v => v>=0?'+':'';
const badge = a => `<span class="badge badge-${a}">${a}</span>`;
const tsBadge = s => { const zh=TS_ZH[s]||s,col=TS_COLOR[s]||'#888'; return `<span style="font-size:10px;padding:2px 7px;border-radius:10px;background:${col}20;color:${col};font-weight:600">${zh}</span>`; };
const scCol  = s => s>=75?'#1D9E75':s>=50?'#378ADD':s>=30?'#BA7517':'#D85A30';
const scBar  = (s,w='80px') => `<div class="score-wrap" style="width:${w}"><div class="score-bar" style="width:${Math.min(s,100)}%;background:${scCol(s)}"></div></div>`;
const avg    = (arr,k) => arr.length ? arr.reduce((a,x)=>a+(parseFloat(x[k])||0),0)/arr.length : 0;
const aiBox  = (obs,rsn,con,act) => `<div class="ai-box">
  <div class="ai-row"><strong>📊 Observation</strong>：${obs}</div>
  <div class="ai-row"><strong>🧠 Reasoning</strong>：${rsn}</div>
  <div class="ai-row"><strong>✅ Conclusion</strong>：${con}</div>
  <div class="ai-row"><strong>⚡ Action</strong>：${act}</div></div>`;

async function fetchJ(name) {
  const r = await fetch(`${EXPORTS_BASE}/${name}.json?t=${Date.now()}`);
  if (!r.ok) throw new Error(`${name}.json: HTTP ${r.status}`);
  return r.json();
}

async function loadAll() {
  ['market','leader','trades','lifecycle','watchlist'].forEach(t=>{
    const el=$('s-'+t); if(el) el.innerHTML='<div class="loading"><span class="spin"></span>加载中...</div>';
  });
  $('uptime').textContent='加载中...';
  try {
    const [mkt,lb,tr,wl,lc,dh] = await Promise.all([
      fetchJ('market_state'), fetchJ('leaderboard'), fetchJ('trade_actions'),
      fetchJ('watchlist'), fetchJ('lifecycle'), fetchJ('data_health').catch(()=>null),
    ]);
    DATA.market=mkt.market; DATA.leaderboard=lb.leaders||[];
    DATA.trades=tr.stocks||[]; DATA.watchlist=wl.watchlist||[];
    DATA.lifecycle=lc.regimes||{}; DATA.health=dh;
    $('uptime').textContent='数据时间：'+(mkt.generated_at_display||mkt.generated_at||'未知');
    ['market','leader','trades','lifecycle','watchlist'].forEach(t=>render(t));
  } catch(e) {
    ['market','leader','trades','lifecycle','watchlist'].forEach(t=>{
      const el=$('s-'+t);
      if(el) el.innerHTML=`<div class="error"><strong>数据加载失败</strong><br>${e.message}<br><br>请先运行 GitHub Actions → 初始化历史数据。</div>`;
    });
  }
}

function go(name,btn){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on')); btn.classList.add('on');
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on')); $('s-'+name).classList.add('on');
}

function selectStock(sym){ selectedStock=sym; render('trades'); }

// ═══════════════════════════════════════════════════════
// render dispatcher
// ═══════════════════════════════════════════════════════
function render(tab) {
  if (!DATA.market && tab==='market') return;

  // ── Tab 1: Market Regime Dashboard ──────────────────
  if (tab==='market') {
    const m=DATA.market||{}, idx=m.indices||{}, sc=m.market_score||0, bd=m.score_breakdown||{};
    const scC=sc>=80?'#1D9E75':sc>=60?'#BA7517':'#D85A30';
    const dh=DATA.health;

    // Data health banner
    let hb='';
    if(dh){
      const st=dh.data_status, col=st==='PASS'?'var(--green)':st==='WARN'?'var(--amber)':'var(--red)';
      const ic=st==='PASS'?'✅':st==='WARN'?'⚠️':'❌';
      hb=`<div style="background:${col}15;border:.5px solid ${col}40;border-radius:var(--radius);padding:.6rem 1rem;margin-bottom:1rem;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px">
        <span>${ic} 数据质量 <strong style="color:${col}">${st}</strong> · 成分股 ${dh.universe_count||0} 只 · 有效 ${dh.valid_symbols||0} 只 · 覆盖率 ${dh.history_coverage_pct||0}% · 最新 ${dh.latest_data_date||'—'}</span>
        <span style="color:var(--text3)">${dh.generated_at_display||''}</span>
      </div>`;
    }

    let h=hb;

    // Market Score + State + Leadership
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
        <div style="font-size:10px;color:var(--text2);margin-top:.4rem">${sc>=80?'80-100 = Risk-On':sc>=60?'60-79 = Neutral':'0-59 = Risk-Off'}</div>
      </div>
      <div class="mc" style="text-align:center">
        <div class="mc-label">领涨确认</div>
        <div style="font-size:28px;margin:.3rem 0">${m.leadership_confirmed?'✅':'⚠️'}</div>
        <div style="font-size:12px;font-weight:600;color:${m.leadership_confirmed?'var(--green)':'var(--amber)'}">${m.leadership_confirmed?'Leadership Confirmed':'Leadership Unconfirmed'}</div>
        <div style="font-size:10px;color:var(--text2);margin-top:.3rem">SPX & NDX & SOX > MA50</div>
      </div>
    </div>`;

    // Score breakdown
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

    // Four indices cards
    h+=`<div class="card"><div class="card-head">四大指数实时概览</div><div class="card-body"><div class="grid-4">`;
    ['SPX','NDX','VIX','SOX'].forEach(code=>{
      const ix=idx[code]||{}, av=ix.available!==false, cp=av?ix.change_pct||0:0, cc=cp>=0?'var(--green)':'var(--red)';
      if(code==='VIX'){
        h+=`<div style="background:var(--bg2);border-radius:var(--radius);padding:.85rem">
          <div style="font-size:11px;color:var(--text2);margin-bottom:6px">${IDX_ICONS[code]} ${ix.name||code}</div>
          <div style="font-size:22px;font-weight:700;color:${ix.vix_color||'var(--text)'}">${av?p2(ix.price,2):'N/A'}</div>
          <div style="font-size:11px;margin-top:4px;display:flex;justify-content:space-between">
            <span style="color:${cc}">${sgn(cp)}${p2(cp,2)}%</span>
            <span style="color:${ix.vix_color||'var(--text2)'}">${ix.vix_state||''}</span>
          </div>
          <div style="font-size:10px;color:var(--text3);margin-top:4px">趋势：${ix.vix_trend||'—'}</div>
        </div>`;
      } else {
        h+=`<div style="background:var(--bg2);border-radius:var(--radius);padding:.85rem">
          <div style="font-size:11px;color:var(--text2);margin-bottom:6px">${IDX_ICONS[code]} ${ix.name||code}</div>
          <div style="font-size:22px;font-weight:700">${av?parseFloat(ix.price||0).toLocaleString(undefined,{maximumFractionDigits:0}):'N/A'}</div>
          <div style="font-size:11px;margin-top:4px;display:flex;justify-content:space-between">
            <span style="color:${cc}">${sgn(cp)}${p2(cp,2)}%</span>
            <span style="color:${ix.trend_color||'var(--text2)'};font-size:10px">${ix.trend||''}</span>
          </div>
          <div style="font-size:10px;color:var(--text3);margin-top:4px">MA20:${av?parseFloat(ix.ma20||0).toLocaleString(undefined,{maximumFractionDigits:0}):'—'} MA50:${av?parseFloat(ix.ma50||0).toLocaleString(undefined,{maximumFractionDigits:0}):'—'}</div>
        </div>`;
      }
    });
    h+=`</div></div></div>`;

    // Relative strength tags
    const tp=idx.tech_premium, sp=idx.sox_premium;
    if(tp!==undefined||sp!==undefined){
      h+=`<div style="display:flex;gap:8px;margin-bottom:1rem;flex-wrap:wrap">`;
      if(tp!==undefined) h+=`<span style="font-size:12px;padding:5px 14px;border-radius:20px;background:var(--bg2)">💻 ${idx.tech_premium_signal} &nbsp;<strong style="color:${tp>=0?'var(--green)':'var(--red)'}">${sgn(tp)}${p2(tp,2)}%</strong> vs SPX 20日</span>`;
      if(sp!==undefined) h+=`<span style="font-size:12px;padding:5px 14px;border-radius:20px;background:var(--bg2)">🔬 ${idx.sox_premium_signal} &nbsp;<strong style="color:${sp>=0?'var(--green)':'var(--red)'}">${sgn(sp)}${p2(sp,2)}%</strong> vs SPX 20日</span>`;
      h+=`</div>`;
    }

    // SPX chart + sector doughnut
    h+=`<div class="grid-2">
      <div class="card" style="margin-bottom:0"><div class="card-head">标普500 趋势 <span class="sub">距MA50 ${sgn(m.pct_above_ma50)}${p2(m.pct_above_ma50)}%</span></div><div class="card-body">
        <div class="cwrap" style="height:200px"><canvas id="cw-spx"></canvas></div>
      </div></div>
      <div class="card" style="margin-bottom:0"><div class="card-head">领涨板块 Top10</div><div class="card-body">
        <div id="sec-legend" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;font-size:10px;color:var(--text2)"></div>
        <div class="cwrap" style="height:160px"><canvas id="cw-sector"></canvas></div>
      </div></div>
    </div><br>`;

    // A/D + AI
    h+=`<div class="mc" style="margin-bottom:1rem"><div class="mc-label">涨跌家数</div>
      <div class="mc-val"><span style="color:var(--green)">${m.advance_count||'-'}</span><span style="color:var(--text3);font-size:14px"> / </span><span style="color:var(--red)">${m.decline_count||'-'}</span></div>
      <div class="mc-sub">A/D Ratio: ${p2(m.advance_decline,2)}</div>
    </div>`;

    const vix=idx['VIX']||{};
    h+=aiBox(
      `Market Score ${sc}，SPX ${parseFloat(m.spx_close||0).toLocaleString()}，VIX ${vix.available?p2(vix.price,1)+'（'+vix.vix_state+'）':'N/A'}，涨跌比 ${m.advance_count}:${m.decline_count}。`,
      `${m.leadership_confirmed?'三指数均位于MA50上方，Leadership Confirmed。':'Leadership Unconfirmed，等待指数收复MA50。'}${idx.tech_premium!==undefined?' NDX相对SPX 20日：'+(idx.tech_premium>=0?'+':'')+p2(idx.tech_premium,2)+'%。':''}`,
      `${m.state_icon||'🟡'} ${m.state_zh||'中性观望'}，${sc>=80?'适合持有趋势强势股。':sc>=60?'谨慎操作，控制仓位。':'防御为主，等待信号改善。'}`,
      sc>=80?'持有 Leader Board 前5名，止损设于MA20下方':sc>=60?'减少新仓，保留核心持仓':'减仓或空仓，等待 Market Score ≥ 60'
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
      const rc=s.rs_percentile>=70?'var(--green)':s.rs_percentile>=40?'var(--amber)':'var(--red)';
      h+=`<tr>
        <td style="color:var(--text3);font-weight:500">${s.rank}</td>
        <td><div class="stock-symbol">${s.symbol}</div><div class="stock-name">${s.name||''}</div></td>
        <td><span class="pill">${s.sector||'—'}</span></td>
        <td style="color:${rc};font-weight:600">${p2(s.rs_percentile,1)}</td>
        <td style="color:${(s.momentum_score||0)>=0?'var(--green)':'var(--red)'};font-weight:500">${sgn(s.momentum_score)}${p2((s.momentum_score||0)*100,2)}%</td>
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
    h+=aiBox(
      `Top10 平均 RS ${p2(avg(leaders,'rs_percentile'),1)}%，平均健康度 ${p2(avg(leaders,'trend_health'),1)}，平均 LeaderScore ${p2(avg(leaders,'leader_score'),1)}。`,
      `${leaders.filter(s=>s.trade_action==='BUY'||s.trade_action==='ADD').map(s=>s.symbol).join('、')||'暂无'} 处于买入/加仓信号区间。`,
      `领导股整体${avg(leaders,'trend_health')>=65?'趋势健康，适合持有':'趋势减弱，注意控制风险'}。`,
      `重点跟踪 ${leaders.slice(0,3).map(s=>s.symbol).join('、')} 的走势与成交量变化。`
    );
    $('s-leader').innerHTML=h;
    setTimeout(()=>{
      const e1=$('cw-rs-mom');
      if(e1){if(charts.rsMom)charts.rsMom.destroy();
        charts.rsMom=new Chart(e1,{type:'scatter',data:{datasets:[{label:'Top10',data:leaders.map(s=>({x:s.rs_percentile||0,y:(s.momentum_score||0)*100})),backgroundColor:PALETTE,pointRadius:8,pointHoverRadius:11}]},
          options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${leaders[ctx.dataIndex]?.symbol}  RS:${p2(ctx.parsed.x,1)}  MOM:${p2(ctx.parsed.y,2)}%`}}},
            scales:{x:{title:{display:true,text:'RS 百分位',font:{size:10}},min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},
                    y:{title:{display:true,text:'动量 (%)',font:{size:10}},ticks:{font:{size:10},callback:v=>v+'%'},grid:{color:'rgba(128,128,128,0.1)'}}}
          }});}
      const e2=$('cw-health');
      if(e2){if(charts.health)charts.health.destroy();
        const sorted=[...leaders].sort((a,b)=>(b.trend_health||0)-(a.trend_health||0));
        charts.health=new Chart(e2,{type:'bar',data:{labels:sorted.map(s=>s.symbol),datasets:[{label:'健康度',data:sorted.map(s=>s.trend_health||0),backgroundColor:sorted.map(s=>scCol(s.trend_health||0)),borderRadius:4}]},
          options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},x:{ticks:{font:{size:11}},grid:{display:false}}}}});}
    },80);
  }

  // ── Tab 3: Trade Dashboard ────────────────────────────
  if (tab==='trades') {
    const stocks=DATA.trades||[];
    if(!stocks.length){$('s-trades').innerHTML='<div class="loading">暂无数据</div>';return;}
    const sym=selectedStock||stocks[0]?.symbol; selectedStock=sym;
    const s=stocks.find(x=>x.symbol===sym)||stocks[0];
    let h=`<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:1rem">
      ${stocks.map(x=>`<button onclick="selectStock('${x.symbol}')" style="font-size:11px;padding:4px 10px;border:.5px solid var(--border2);background:${x.symbol===sym?'var(--text)':'none'};color:${x.symbol===sym?'var(--bg)':'var(--text2)'};border-radius:20px;cursor:pointer;font-family:var(--font)">${x.symbol}</button>`).join('')}
    </div>`;
    h+=`<div class="card"><div class="card-head">
        <span><strong>${s.symbol}</strong> &nbsp;${s.name||''}&nbsp;<span class="pill">${s.sector||''}</span></span>
        <span class="badge badge-${s.trade_action||'HOLD'}" style="font-size:12px;padding:4px 12px">${s.trade_action||'HOLD'} ${s.action_label||''}</span>
      </div><div class="card-body">
      <div class="grid-3" style="margin-bottom:1rem">
        <div class="mc"><div class="mc-label">现价</div><div class="mc-val">$${p2(s.price)}</div></div>
        <div class="mc"><div class="mc-label">健康度</div><div class="mc-val" style="color:${scCol(s.trend_health||0)}">${p2(s.trend_health,0)}</div>${scBar(s.trend_health||0)}</div>
        <div class="mc"><div class="mc-label">RS 百分位</div><div class="mc-val">${p2(s.rs_percentile,1)}</div></div>
      </div>
      <div class="cwrap" style="height:280px"><canvas id="cw-price"></canvas></div>
    </div></div>`;
    h+=`<div class="card"><div class="card-head">动量斜率 <span class="sub">S5=${sgn(s.slope5)}${p2((s.slope5||0)*100,2)}% · S10=${sgn(s.slope10)}${p2((s.slope10||0)*100,2)}% · S20=${sgn(s.slope20)}${p2((s.slope20||0)*100,2)}%</span></div><div class="card-body">
      <div class="tbl-wrap"><table><thead><tr><th>5日斜率</th><th>10日斜率</th><th>20日斜率</th><th>动量综合</th><th>动量加速</th></tr></thead><tbody><tr>
        ${['slope5','slope10','slope20'].map(k=>`<td style="color:${(s[k]||0)>=0?'var(--green)':'var(--red)'};font-weight:500">${sgn(s[k])}${p2((s[k]||0)*100,3)}%</td>`).join('')}
        <td style="font-weight:600;color:${(s.momentum_score||0)>=0?'var(--green)':'var(--red)'}">${sgn(s.momentum_score)}${p2((s.momentum_score||0)*100,3)}%</td>
        <td style="color:${(s.momentum_accel||0)>=0?'var(--green)':'var(--red)'}">${sgn(s.momentum_accel)}${p2((s.momentum_accel||0)*100,3)}%</td>
      </tr></tbody></table></div>
    </div></div>`;
    h+=`<div class="card"><div class="card-head">均线结构与回撤</div><div class="card-body">
      <div class="tbl-wrap"><table><thead><tr><th>现价</th><th>MA20</th><th>MA50</th><th>MA200</th><th>MA20斜率</th><th>回撤</th><th>波动率</th></tr></thead><tbody><tr>
        <td style="font-weight:600">$${p2(s.price)}</td>
        <td style="color:${s.above_ma20?'var(--green)':'var(--red)'}">${s.above_ma20?'↑':'↓'} $${p2(s.ma20)}</td>
        <td style="color:${s.above_ma50?'var(--green)':'var(--red)'}">${s.above_ma50?'↑':'↓'} $${p2(s.ma50)}</td>
        <td style="color:${s.above_ma200?'var(--green)':'var(--red)'}">${s.above_ma200?'↑':'↓'} $${p2(s.ma200)}</td>
        <td style="color:${(s.ma20_slope||0)>=0?'var(--green)':'var(--red)'}">${sgn(s.ma20_slope)}${p2((s.ma20_slope||0)*100,3)}%/日</td>
        <td style="color:${(s.drawdown_pct||0)<8?'var(--green)':(s.drawdown_pct||0)<15?'var(--amber)':'var(--red)'}">${p2(s.drawdown_pct)}%</td>
        <td style="color:var(--text2)">${p2(s.volatility)}%</td>
      </tr></tbody></table></div>
    </div></div>`;
    h+=aiBox(
      `${s.symbol} 现价 $${p2(s.price)}，${s.above_ma20?'位于MA20上方':'跌破MA20'}，${s.above_ma50?'MA50支撑有效':'MA50失守'}。回撤 ${p2(s.drawdown_pct)}%，波动率 ${p2(s.volatility)}%。`,
      `动量${(s.momentum_score||0)>=0?'向上':'向下'}，趋势状态 <strong>${TS_ZH[s.trend_state]||s.trend_state}</strong>，健康度 ${p2(s.trend_health,0)}/100。`,
      `信号：<strong>${s.trade_action} ${s.action_label}</strong> — ${s.action_description||''}`,
      s.action_description||'按信号执行，严守止损纪律。'
    );
    $('s-trades').innerHTML=h;
    setTimeout(()=>{
      const el=$('cw-price');
      if(!el||!s.chart_dates?.length)return;
      if(charts.price)charts.price.destroy();
      charts.price=new Chart(el,{type:'line',data:{labels:s.chart_dates.map(d=>d.slice(5)),datasets:[
        {label:'价格',data:s.chart_prices,borderColor:'#378ADD',backgroundColor:'rgba(55,138,221,0.05)',borderWidth:2,pointRadius:0,tension:0.2,fill:true},
        {label:'MA20',data:s.chart_ma20,borderColor:'#1D9E75',borderWidth:1.5,pointRadius:0,borderDash:[4,3],fill:false},
        {label:'MA50',data:s.chart_ma50,borderColor:'#BA7517',borderWidth:1.5,pointRadius:0,borderDash:[6,3],fill:false},
      ]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
        plugins:{legend:{labels:{font:{size:10},boxWidth:10,padding:8}}},
        scales:{x:{ticks:{font:{size:10},maxTicksLimit:10},grid:{display:false}},
                y:{ticks:{font:{size:10},callback:v=>'$'+parseFloat(v).toFixed(0)},grid:{color:'rgba(128,128,128,0.1)'}}}
      }});
    },80);
  }

  // ── Tab 4: Trend Lifecycle ────────────────────────────
  if (tab==='lifecycle') {
    const lc=DATA.lifecycle||{}, order=['Expansion','Mature','Speculative','Broken'];
    if(!Object.keys(lc).length){$('s-lifecycle').innerHTML='<div class="loading">暂无数据</div>';return;}
    let h='<div class="regime-grid">';
    order.forEach(reg=>{
      const stocks=lc[reg]||[], m=REG_META[reg]||{};
      h+=`<div class="regime-cell badge-${reg}">
        <div style="font-size:13px;font-weight:600;margin-bottom:4px">${m.zh||reg} <span style="font-size:20px;font-weight:700">${stocks.length}</span></div>
        <div style="font-size:11px;opacity:.8;margin-bottom:8px">${m.desc||''}</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px">
          ${stocks.slice(0,8).map(s=>`<span style="font-size:10px;background:rgba(255,255,255,0.25);padding:1px 6px;border-radius:10px;font-weight:500">${s.symbol}</span>`).join('')}
          ${stocks.length>8?`<span style="font-size:10px;opacity:.6">+${stocks.length-8}</span>`:''}
        </div>
      </div>`;
    });
    h+='</div>';
    h+=`<div class="card"><div class="card-head">动量象限图 <span class="sub">X: RS百分位 · Y: 动量加速度</span></div><div class="card-body">
      <div class="cwrap" style="height:360px"><canvas id="cw-regime"></canvas></div>
    </div></div>`;
    const all=order.flatMap(r=>(lc[r]||[]).map(s=>({...s,regime:r})));
    h+=`<div class="card"><div class="card-head">Top50 象限归属</div><div class="card-body"><div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>代码</th><th>板块</th><th>象限</th><th>健康度</th><th>RS%</th><th>动量</th><th>操作</th></tr></thead><tbody>
      ${all.slice(0,30).map(s=>`<tr>
        <td style="color:var(--text3)">${s.rank||'—'}</td>
        <td><strong>${s.symbol}</strong><br><span style="font-size:10px;color:var(--text2)">${s.name||''}</span></td>
        <td><span class="pill">${s.sector||'—'}</span></td>
        <td><span class="badge badge-${s.regime}">${REG_META[s.regime]?.zh||s.regime}</span></td>
        <td>${p2(s.trend_health,0)} ${scBar(s.trend_health||0,'45px')}</td>
        <td style="color:${(s.rs_percentile||0)>=70?'var(--green)':'var(--text2)'}">${p2(s.rs_percentile,1)}</td>
        <td style="color:${(s.momentum_score||0)>=0?'var(--green)':'var(--red)'}">${sgn(s.momentum_score)}${p2((s.momentum_score||0)*100,2)}%</td>
        <td>${badge(s.trade_action||'HOLD')}</td>
      </tr>`).join('')}
      </tbody></table></div></div></div>`;
    const expN=(lc['Expansion']||[]).length, brkN=(lc['Broken']||[]).length;
    h+=aiBox(
      `Top50 中扩张期 ${expN} 只，成熟期 ${(lc['Mature']||[]).length} 只，投机期 ${(lc['Speculative']||[]).length} 只，破坏期 ${brkN} 只。`,
      `${expN>brkN?'扩张期占优，市场趋势健康。':'破坏期偏多，市场承压。'}`,
      `${expN>=4?'趋势扩张阶段，适合持有 Expansion 区间股票。':'趋势动能不足，防御为主。'}`,
      expN>=4?'持有 Expansion 个股，止损设于 MA20 下方':'控制仓位，等待 Expansion ≥ 4 只'
    );
    $('s-lifecycle').innerHTML=h;
    setTimeout(()=>{
      const el=$('cw-regime'); if(!el)return;
      if(charts.regime)charts.regime.destroy();
      const rCol={Expansion:'#1D9E75',Mature:'#378ADD',Speculative:'#BA7517',Broken:'#D85A30'};
      const zp={id:'rz',afterDraw(ch){
        const{ctx:c,chartArea:{left,right,top,bottom},scales:{x,y}}=ch;
        const cx=x.getPixelForValue(50),cy=y.getPixelForValue(0);
        c.save();c.strokeStyle='rgba(128,128,128,0.25)';c.lineWidth=1;c.setLineDash([4,4]);
        c.beginPath();c.moveTo(cx,top);c.lineTo(cx,bottom);c.stroke();
        c.beginPath();c.moveTo(left,cy);c.lineTo(right,cy);c.stroke();
        c.setLineDash([]);c.font='10px -apple-system,sans-serif';c.fillStyle='rgba(128,128,128,0.4)';
        c.textAlign='left';c.fillText('趋势初段',cx+4,top+14);c.textAlign='right';c.fillText('扩张期',cx-4,top+14);
        c.textAlign='left';c.fillText('破坏期',cx+4,bottom-6);c.textAlign='right';c.fillText('过热期',cx-4,bottom-6);
        c.restore();
      }};
      charts.regime=new Chart(el,{type:'scatter',plugins:[zp],data:{datasets:order.map(reg=>{
        const pts=(lc[reg]||[]).map(s=>({x:s.rs_percentile||0,y:s.momentum_accel||0,label:s.symbol}));
        return{label:REG_META[reg]?.zh||reg,data:pts,backgroundColor:rCol[reg],pointRadius:7,pointHoverRadius:10,_pts:pts};
      })},options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{font:{size:11},boxWidth:10,padding:8}},tooltip:{callbacks:{label:ctx=>{const p=ctx.dataset._pts[ctx.dataIndex];return `${p.label}  RS:${p2(p.x,1)}  加速:${sgn(p.y)}${p2(p.y*100,2)}%`;}}}},
        scales:{x:{title:{display:true,text:'RS 百分位',font:{size:11}},min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},
                y:{title:{display:true,text:'动量加速度',font:{size:11}},ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}}}
      }});
    },80);
  }

  // ── Tab 5: Watchlist ──────────────────────────────────
  if (tab==='watchlist') {
    const wl=DATA.watchlist||[];
    if(!wl.length){$('s-watchlist').innerHTML='<div class="loading">暂无数据</div>';return;}
    let h=`<div class="card"><div class="card-head">Watchlist — Rank 11–30 潜在领导股 <span class="sub">PromotionScore = 0.4×RankVelocity + 0.3×TH + 0.2×MomAccel + 0.1×Pullback</span></div><div class="card-body"><div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>代码</th><th>板块</th><th>晋升分</th><th>健康度</th><th>RS%</th><th>趋势状态</th><th>排名速度</th><th>操作</th></tr></thead><tbody>`;
    wl.forEach(s=>{
      const rvc=(s.rank_velocity||0)>0?'var(--green)':(s.rank_velocity||0)<0?'var(--red)':'var(--text3)';
      const rvi=(s.rank_velocity||0)>0?'↑':(s.rank_velocity||0)<0?'↓':'—';
      h+=`<tr>
        <td style="color:var(--text3)">${s.rank}</td>
        <td><strong>${s.symbol}</strong><br><span style="font-size:10px;color:var(--text2)">${s.name||''}</span></td>
        <td><span class="pill">${s.sector||'—'}</span></td>
        <td><span style="font-weight:700;color:${scCol(s.promotion_score||0)}">${p2(s.promotion_score,1)}</span>${scBar(s.promotion_score||0,'50px')}</td>
        <td>${p2(s.trend_health,0)} ${scBar(s.trend_health||0,'45px')}</td>
        <td style="color:${(s.rs_percentile||0)>=70?'var(--green)':'var(--text2)'}">${p2(s.rs_percentile,1)}</td>
        <td>${tsBadge(s.trend_state||'')}</td>
        <td style="color:${rvc};font-weight:500">${rvi} ${p2(Math.abs(s.rank_velocity||0)*100,1)}%</td>
        <td>${badge(s.trade_action||'HOLD')}</td>
      </tr>`;
    });
    h+=`</tbody></table></div></div></div>`;
    h+=`<div class="card"><div class="card-head">晋升概率排行</div><div class="card-body"><div class="cwrap" style="height:240px"><canvas id="cw-promo"></canvas></div></div></div>`;
    const tp2=wl.filter(s=>(s.promotion_score||0)>=60);
    h+=aiBox(
      `Watchlist ${wl.length} 只（Rank 11-30），晋升分≥60 共 ${tp2.length} 只：${tp2.map(s=>s.symbol).join('、')||'暂无'}。`,
      '晋升分高的股票具备上升排名速度和健康趋势结构，是下一轮强势股的潜在来源。',
      `${tp2.length>0?`重点关注 ${tp2.slice(0,3).map(s=>s.symbol).join('、')}，有望晋升 Top10。`:'暂无高晋升概率股票，耐心等待。'}`,
      tp2.length>0?`密切跟踪 ${tp2.slice(0,3).map(s=>s.symbol).join('、')}，突破前高可考虑建仓`:'继续观察，等待晋升信号出现'
    );
    $('s-watchlist').innerHTML=h;
    setTimeout(()=>{
      const el=$('cw-promo'); if(!el)return;
      if(charts.promo)charts.promo.destroy();
      const top15=[...wl].sort((a,b)=>(b.promotion_score||0)-(a.promotion_score||0)).slice(0,15);
      charts.promo=new Chart(el,{type:'bar',data:{labels:top15.map(s=>s.symbol),datasets:[{label:'晋升分',data:top15.map(s=>s.promotion_score||0),backgroundColor:top15.map(s=>scCol(s.promotion_score||0)),borderRadius:4}]},
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{min:0,max:100,ticks:{font:{size:10}},grid:{color:'rgba(128,128,128,0.1)'}},x:{ticks:{font:{size:11}},grid:{display:false}}}}});
    },80);
  }
} // end render()

loadAll();
