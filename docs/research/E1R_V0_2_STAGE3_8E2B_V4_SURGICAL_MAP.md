# Stage 3.8E-2B-v4 Surgical Map

Generated At: `2026-07-08T06:03:44.322617+00:00`
HEAD: `171b252`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Strategy logic changed: `False`
- Exports changed: `False`

## Section

- Lines: `640` - `760`
- KEEP logic lines: `36`
- Replaceable UI candidate lines: `45`
- Template blocks: `8`

## Template Blocks

- lines `639`-`641` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`
- lines `643`-`643` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`
- lines `657`-`662` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`
- lines `665`-`668` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`
- lines `669`-`669` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`
- lines `738`-`747` old_header=`False` old_cards=`True` equity=`False` trade_log=`False` market_state=`False`
- lines `750`-`753` old_header=`False` old_cards=`False` equity=`True` trade_log=`False` market_state=`False`
- lines `759`-`760` old_header=`False` old_cards=`False` equity=`False` trade_log=`False` market_state=`False`

## KEEP Logic Lines

- line `646` `KEEP_LOGIC` terms ``: `if(recentClosed.length>0){`
- line `647` `KEEP_LOGIC` terms ``: `const recentRows=recentClosed.map(t=>{`
- line `648` `KEEP_LOGIC` terms ``: `const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';`
- line `667` `KEEP_POSSIBLE_LOGIC` terms `lbAsOf,simEndDate`: `LS 数值来自 leaderboard.json（${lbAsOf}），回测快照来自 backtest.json（${simEndDate}）。`
- line `671` `KEEP_LOGIC` terms ``: `setTimeout(()=>{`
- line `673` `KEEP_LOGIC` terms ``: `const root=$('s-positions');`
- line `674` `KEEP_LOGIC` terms ``: `const posRows=root?root.querySelectorAll('tr[data-symbol]'):[];`
- line `675` `KEEP_LOGIC` terms ``: `if(posRows.length){`
- line `676` `KEEP_LOGIC` terms ``: `bindStockPreviewRows('#s-positions','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'pos-stock-preview');`
- line `682` `KEEP_LOGIC` terms ``: `if (tab==='research') {`
- line `683` `KEEP_LOGIC` terms ``: `const bt=DATA.backtest, tlog=DATA.tradelog;`
- line `685` `KEEP_LOGIC` terms `vr`: `const vr=bt?.backtest?.results?.layer_d?.variant_results;`
- line `686` `KEEP_LOGIC` terms `vr,e1`: `const e1=vr?.E1_AUDITED_G4_MINHOLD10;`
- line `687` `KEEP_LOGIC` terms `e1`: `if(!e1){$('s-research').innerHTML='<div class="error">E1 数据缺失。</div>';return;}`
- line `689` `KEEP_LOGIC` terms `vr,e1`: `const e1rPanel = renderE1RResearchPanel(vr);`
- line `691` `KEEP_LOGIC` terms ``: `const pc=bt?.backtest?.results?.layer_d?.period_comparison||{};`
- line `696` `KEEP_LOGIC` terms `e1`: `const e1Ret=Number(row?.total_return_pct), alpha=Number(row?.alpha_pct);`
- line `697` `KEEP_LOGIC` terms ``: `const src=row?.spx_total_return_pct;`
- line `698` `KEEP_LOGIC` terms ``: `if(src!==null&&src!==undefined&&src!=='') return {value:src,implied:false};`
- line `699` `KEEP_LOGIC` terms `e1`: `if(Number.isFinite(e1Ret)&&Number.isFinite(alpha)) return {value:e1Ret-alpha,implied:true};`
- line `700` `KEEP_LOGIC` terms ``: `return {value:null,implied:false};`
- line `703` `KEEP_LOGIC` terms ``: `const r=impliedSpxReturn(row);`
- line `704` `KEEP_LOGIC` terms ``: `if(r.value===null||r.value===undefined||r.value==='') return '—';`
- line `705` `KEEP_LOGIC` terms ``: `return `${fmt(r.value)}${r.implied?' *':''}`;`
- line `708` `KEEP_LOGIC` terms `trades,e1`: `const trades=(tlog?.trades||e1.trades||[]).slice(-20).reverse();`
- line `709` `KEEP_LOGIC` terms `trades`: `const tradeRows=trades.map(t=>{`
- line `710` `KEEP_LOGIC` terms ``: `const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';`
- line `722` `KEEP_LOGIC` terms `eqCurve,spxCurve,e1`: `const eqCurve=e1.equity_curve||[], spxCurve=e1.spx_curve||[];`
- line `723` `KEEP_LOGIC` terms `e1rCurve,e1,DATA.e1rFormal`: `const e1rFormal=DATA.e1rFormal||{}, e1rCurve=e1rFormal.equity_curve||[];`
- line `724` `KEEP_LOGIC` terms `oosRows,DATA.oosEquity`: `const oosRowsForNote=(DATA.oosEquity?.curve||[]);`
- line `725` `KEEP_LOGIC` terms `oosLatestDate,oosRows`: `const oosLatestDate=oosRowsForNote.length ? (oosRowsForNote[oosRowsForNote.length-1].date||'—') : '—';`
- line `728` `KEEP_LOGIC` terms `lc`: `const lc=DATA.lifecycle||{}, regOrder=['Expansion','Mature','Speculative','Broken'];`
- line `729` `KEEP_LOGIC` terms `lcStats,lc,REG_META`: `const lcStats=regOrder.map(r=>({reg:r,n:(lc[r]||[]).length,zh:REG_META[r]?.zh||r}));`
- line `731` `KEEP_LOGIC` terms `e1`: `let h=e1rPanel + `<div class="frozen-banner">`
- line `749` `KEEP_LOGIC` terms `eqCurve`: `if(eqCurve.length>1){`
- line `758` `KEEP_LOGIC` terms `lcStats,lc`: `if(lcStats.some(r=>r.n>0)){`

## Replaceable UI Candidate Lines

- line `641` `REPLACEABLE_UI_CANDIDATE` terms ``: `</div>`;`
- line `643` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`</div></div>`;`
- line `649` `REPLACEABLE_UI_CANDIDATE` terms ``: `return `<tr data-symbol="${t.symbol}">`
- line `650` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td><strong>${t.symbol}</strong></td>`
- line `651` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${t.entry_date}</td><td>${t.exit_date||'—'}</td>`
- line `652` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td style="${rc}">${ret>=0?'+':''}${p2(ret)}%</td>`
- line `653` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${t.holding_days||0}</td>`
- line `654` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td style="font-size:11px;color:var(--text2)">${t.exit_reason||''}</td>`
- line `657` `REPLACEABLE_UI_CANDIDATE` terms `trades`: `h+=`<div class="card"><div class="card-head">Recent closed trades (last 5)</div><div class="card-body">`
- line `658` `REPLACEABLE_UI_CANDIDATE` terms ``: `<div class="tbl-wrap"><table>`
- line `659` `REPLACEABLE_UI_CANDIDATE` terms ``: `<thead><tr><th>Symbol</th><th>Entry</th><th>Exit</th><th>Return</th><th>Days</th><th>Exit reason</th></tr></thead>`
- line `660` `REPLACEABLE_UI_CANDIDATE` terms ``: `<tbody>${recentRows}</tbody>`
- line `661` `REPLACEABLE_UI_CANDIDATE` terms ``: `</table></div>`
- line `662` `REPLACEABLE_UI_CANDIDATE` terms ``: `</div></div>`;`
- line `665` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`<p class="note" style="margin-top:8px">`
- line `669` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`<div class="card"><div class="card-head">个股预览 <span class="sub">hover / tap 持仓或平仓行切换</span></div><div class="card-body"><div id="pos-stock-preview"></div></div></div>`;`
- line `684` `REPLACEABLE_UI_CANDIDATE` terms ``: `if(!bt){$('s-research').innerHTML='<div class="error">backtest.json 未加载，请刷新或检查 GitHub Actions。</div>';return;}`
- line `692` `REPLACEABLE_UI_CANDIDATE` terms ``: `const pA=pc['A_2023_11_TO_2024_12']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- line `693` `REPLACEABLE_UI_CANDIDATE` terms ``: `const pB=pc['B_2024_12_TO_2026_06']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- line `711` `REPLACEABLE_UI_CANDIDATE` terms ``: `return `<tr>`
- line `712` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td><strong>${t.symbol}</strong></td>`
- line `713` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${t.entry_date}</td><td>${t.exit_date||'—'}</td>`
- line `714` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${p2(t.entry_price||0)}</td><td>${p2(t.exit_price||0)}</td>`
- line `715` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td style="${rc}">${ret>=0?'+':''}${p2(ret)}%</td>`
- line `716` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${t.holding_days||0}</td>`
- line `717` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td style="font-size:11px;color:var(--text2)">${t.exit_reason||''}</td>`
- line `718` `REPLACEABLE_UI_CANDIDATE` terms ``: `<td>${t.is_sim_end?'<span class="badge-sim">SIM</span>':''}</td>`
- line `732` `REPLACEABLE_UI_CANDIDATE` terms ``: `<strong>E1_AUDITED_G4_MINHOLD10 — 正式冻结 2026-06-16</strong> &nbsp;·&nbsp;`
- line `736` `REPLACEABLE_UI_CANDIDATE` terms ``: `</div>`;`
- line `738` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`<div class="grid-4" style="margin-bottom:1rem">`
- line `739` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Full return</div><div class="mc-val" style="color:var(--green)">${fmt(e1.total_return_pct)}</div></div>`
- line `740` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Max drawdown</div><div class="mc-val" style="color:var(--red)">${p2(e1.max_drawdown_pct)}%</div></div>`
- line `741` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Profit factor</div><div class="mc-val">${p2(e1.profit_factor)}</div></div>`
- line `742` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Sharpe</div><div class="mc-val">${p2(e1.sharpe_ratio)}</div></div>`
- line `743` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Win rate</div><div class="mc-val">${p2(e1.win_rate_pct)}%</div></div>`
- line `744` `REPLACEABLE_UI_CANDIDATE` terms `trades,e1`: `<div class="mc"><div class="mc-label">Trades</div><div class="mc-val">${e1.number_of_trades||0}</div></div>`
- line `745` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Avg hold</div><div class="mc-val">${p2(e1.avg_holding_days,1)}d</div></div>`
- line `746` `REPLACEABLE_UI_CANDIDATE` terms `e1`: `<div class="mc"><div class="mc-label">Exposure</div><div class="mc-val">${p2(e1.exposure_pct)}%</div></div>`
- line `747` `REPLACEABLE_UI_CANDIDATE` terms ``: `</div>`;`
- line `750` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">Equity curve — E1 vs E1-R vs SPX (indexed to 100)</div><div class="card-body">`
- line `751` `REPLACEABLE_UI_CANDIDATE` terms ``: `<div class="cwrap" style="height:220px"><canvas id="cw-equity"></canvas></div>`
- line `752` `REPLACEABLE_UI_CANDIDATE` terms `oosLatestDate,e1`: `<div class="muted" style="font-size:12px;margin-top:.5rem">Equity includes SIM_END open positions marked to market. Backtest ends: ${e1.sample_validity?.simulation_end_date||'—'} · OOS latest: ${oosLatestDate} · E1-R OOS tracking: not yet completed.</div>`
- line `753` `REPLACEABLE_UI_CANDIDATE` terms ``: `</div></div>`;`
- line `759` `REPLACEABLE_UI_CANDIDATE` terms ``: `h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">个股趋势生命周期分布 <span class="sub">Top50 当前象限</span></div><div class="card-body">`
- line `760` `REPLACEABLE_UI_CANDIDATE` terms ``: `<div class="regime-grid">`;`

## Recommended Patch Rule

- Do not delete the full old E1 header block.
- Preserve all KEEP_LOGIC and KEEP_POSSIBLE_LOGIC lines.
- Replace only the template block that visibly renders old E1 summary/card UI.
- Do not touch the equity curve template block.
- Do not touch Trade Log.
- Do not touch Market State.

