# Stage 3.8E-2B Structural Diff Audit

Generated At: `2026-07-08T05:44:44.572052+00:00`
Base: `c1a7e46:dashboard/app.js`
Current HEAD: `1de6bb2`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Strategy logic changed: `False`
- Exports changed: `False`

## Function Size / Range

- Before `render(tab)`: lines `267`-`985`, chars `41765`
- After `render(tab)`: lines `309`-`962`, chars `38280`
- Before `renderE1RResearchPanel`: lines `194`-`261`
- After `renderE1RResearchPanel`: lines `198`-`202`

## Old E1 Header Block Logic Lines

- Old E1 header block: lines `669`-`736`
- Non-UI / possible logic lines inside old header block: `34`

- line `671` `likely_non_ui_logic` symbols ``: `setTimeout(()=>{`
- line `673` `likely_non_ui_logic` symbols ``: `const root=$('s-positions');`
- line `674` `likely_non_ui_logic` symbols ``: `const posRows=root?root.querySelectorAll('tr[data-symbol]'):[];`
- line `675` `likely_non_ui_logic` symbols ``: `if(posRows.length){`
- line `676` `likely_non_ui_logic` symbols ``: `bindStockPreviewRows('#s-positions','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'pos-stock-preview');`
- line `682` `likely_non_ui_logic` symbols ``: `if (tab==='research') {`
- line `683` `likely_non_ui_logic` symbols ``: `const bt=DATA.backtest, tlog=DATA.tradelog;`
- line `685` `likely_non_ui_logic` symbols `vr`: `const vr=bt?.backtest?.results?.layer_d?.variant_results;`
- line `686` `likely_non_ui_logic` symbols `vr,e1`: `const e1=vr?.E1_AUDITED_G4_MINHOLD10;`
- line `687` `likely_non_ui_logic` symbols `e1`: `if(!e1){$('s-research').innerHTML='<div class="error">E1 数据缺失。</div>';return;}`
- line `689` `likely_non_ui_logic` symbols `vr,e1,e1r`: `const e1rPanel = renderE1RResearchPanel(vr);`
- line `691` `likely_non_ui_logic` symbols ``: `const pc=bt?.backtest?.results?.layer_d?.period_comparison||{};`
- line `692` `likely_non_ui_logic` symbols ``: `const pA=pc['A_2023_11_TO_2024_12']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- line `693` `likely_non_ui_logic` symbols ``: `const pB=pc['B_2024_12_TO_2026_06']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- line `695` `likely_non_ui_logic` symbols ``: `function impliedSpxReturn(row){`
- line `696` `likely_non_ui_logic` symbols `e1`: `const e1Ret=Number(row?.total_return_pct), alpha=Number(row?.alpha_pct);`
- line `697` `likely_non_ui_logic` symbols ``: `const src=row?.spx_total_return_pct;`
- line `698` `likely_non_ui_logic` symbols ``: `if(src!==null&&src!==undefined&&src!=='') return {value:src,implied:false};`
- line `699` `likely_non_ui_logic` symbols `e1`: `if(Number.isFinite(e1Ret)&&Number.isFinite(alpha)) return {value:e1Ret-alpha,implied:true};`
- line `700` `likely_non_ui_logic` symbols ``: `return {value:null,implied:false};`
- line `702` `likely_non_ui_logic` symbols ``: `function fmtSpx(row){`
- line `703` `likely_non_ui_logic` symbols ``: `const r=impliedSpxReturn(row);`
- line `704` `likely_non_ui_logic` symbols ``: `if(r.value===null||r.value===undefined||r.value==='') return '—';`
- line `705` `likely_non_ui_logic` symbols ``: `return `${fmt(r.value)}${r.implied?' *':''}`;`
- line `708` `likely_non_ui_logic` symbols `trades,e1`: `const trades=(tlog?.trades||e1.trades||[]).slice(-20).reverse();`
- line `709` `likely_non_ui_logic` symbols `trades`: `const tradeRows=trades.map(t=>{`
- line `710` `likely_non_ui_logic` symbols ``: `const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';`
- line `722` `likely_non_ui_logic` symbols `eqCurve,spxCurve,e1`: `const eqCurve=e1.equity_curve||[], spxCurve=e1.spx_curve||[];`
- line `723` `likely_non_ui_logic` symbols `e1rCurve,e1,e1r,e1rFormal,DATA.e1rFormal`: `const e1rFormal=DATA.e1rFormal||{}, e1rCurve=e1rFormal.equity_curve||[];`
- line `724` `likely_non_ui_logic` symbols `oosRows,DATA.oosEquity`: `const oosRowsForNote=(DATA.oosEquity?.curve||[]);`
- line `725` `likely_non_ui_logic` symbols `oosLatestDate,oosRows`: `const oosLatestDate=oosRowsForNote.length ? (oosRowsForNote[oosRowsForNote.length-1].date||'—') : '—';`
- line `728` `likely_non_ui_logic` symbols `lc`: `const lc=DATA.lifecycle||{}, regOrder=['Expansion','Mature','Speculative','Broken'];`
- line `729` `likely_non_ui_logic` symbols `lcStats,lc,REG_META`: `const lcStats=regOrder.map(r=>({reg:r,n:(lc[r]||[]).length,zh:REG_META[r]?.zh||r}));`
- line `731` `likely_non_ui_logic` symbols `e1,e1r`: `let h=e1rPanel + `<div class="frozen-banner">`

## Removed Non-UI Candidates From render(tab)

- Count: `34`

- `likely_non_ui_logic` symbols ``: `setTimeout(()=>{`
- `likely_non_ui_logic` symbols ``: `const root=$('s-positions');`
- `likely_non_ui_logic` symbols ``: `const posRows=root?root.querySelectorAll('tr[data-symbol]'):[];`
- `likely_non_ui_logic` symbols ``: `if(posRows.length){`
- `likely_non_ui_logic` symbols ``: `bindStockPreviewRows('#s-positions','tr[data-symbol]',r=>r.getAttribute('data-symbol'),'pos-stock-preview');`
- `likely_non_ui_logic` symbols ``: `if (tab==='research') {`
- `likely_non_ui_logic` symbols ``: `const bt=DATA.backtest, tlog=DATA.tradelog;`
- `likely_non_ui_logic` symbols `vr`: `const vr=bt?.backtest?.results?.layer_d?.variant_results;`
- `likely_non_ui_logic` symbols `vr,e1`: `const e1=vr?.E1_AUDITED_G4_MINHOLD10;`
- `likely_non_ui_logic` symbols `e1`: `if(!e1){$('s-research').innerHTML='<div class="error">E1 数据缺失。</div>';return;}`
- `likely_non_ui_logic` symbols `vr,e1,e1r`: `const e1rPanel = renderE1RResearchPanel(vr);`
- `likely_non_ui_logic` symbols ``: `const pc=bt?.backtest?.results?.layer_d?.period_comparison||{};`
- `likely_non_ui_logic` symbols ``: `const pA=pc['A_2023_11_TO_2024_12']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- `likely_non_ui_logic` symbols ``: `const pB=pc['B_2024_12_TO_2026_06']?.variants?.E1_AUDITED_G4_MINHOLD10||{};`
- `likely_non_ui_logic` symbols ``: `function impliedSpxReturn(row){`
- `likely_non_ui_logic` symbols `e1`: `const e1Ret=Number(row?.total_return_pct), alpha=Number(row?.alpha_pct);`
- `likely_non_ui_logic` symbols ``: `const src=row?.spx_total_return_pct;`
- `likely_non_ui_logic` symbols ``: `if(src!==null&&src!==undefined&&src!=='') return {value:src,implied:false};`
- `likely_non_ui_logic` symbols `e1`: `if(Number.isFinite(e1Ret)&&Number.isFinite(alpha)) return {value:e1Ret-alpha,implied:true};`
- `likely_non_ui_logic` symbols ``: `return {value:null,implied:false};`
- `likely_non_ui_logic` symbols ``: `function fmtSpx(row){`
- `likely_non_ui_logic` symbols ``: `const r=impliedSpxReturn(row);`
- `likely_non_ui_logic` symbols ``: `if(r.value===null||r.value===undefined||r.value==='') return '—';`
- `likely_non_ui_logic` symbols ``: `return `${fmt(r.value)}${r.implied?' *':''}`;`
- `likely_non_ui_logic` symbols `trades,e1`: `const trades=(tlog?.trades||e1.trades||[]).slice(-20).reverse();`
- `likely_non_ui_logic` symbols `trades`: `const tradeRows=trades.map(t=>{`
- `likely_non_ui_logic` symbols ``: `const ret=t.return_pct||0, rc=ret>=0?'color:var(--green)':'color:var(--red)';`
- `likely_non_ui_logic` symbols `eqCurve,spxCurve,e1`: `const eqCurve=e1.equity_curve||[], spxCurve=e1.spx_curve||[];`
- `likely_non_ui_logic` symbols `e1rCurve,e1,e1r,e1rFormal,DATA.e1rFormal`: `const e1rFormal=DATA.e1rFormal||{}, e1rCurve=e1rFormal.equity_curve||[];`
- `likely_non_ui_logic` symbols `oosRows,DATA.oosEquity`: `const oosRowsForNote=(DATA.oosEquity?.curve||[]);`
- `likely_non_ui_logic` symbols `oosLatestDate,oosRows`: `const oosLatestDate=oosRowsForNote.length ? (oosRowsForNote[oosRowsForNote.length-1].date||'—') : '—';`
- `likely_non_ui_logic` symbols `lc`: `const lc=DATA.lifecycle||{}, regOrder=['Expansion','Mature','Speculative','Broken'];`
- `likely_non_ui_logic` symbols `lcStats,lc,REG_META`: `const lcStats=regOrder.map(r=>({reg:r,n:(lc[r]||[]).length,zh:REG_META[r]?.zh||r}));`
- `likely_non_ui_logic` symbols `e1,e1r`: `let h=e1rPanel + `<div class="frozen-banner">`

## Symbol Count Drops

- `oosRows`: before `9`, after `7`, delta `-2`; before lines `[724, 725, 864, 867, 904, 907, 909, 927, 932]`, after lines `[841, 844, 881, 884, 886, 904, 909]`
- `lcStats`: before `3`, after `2`, delta `-1`; before lines `[729, 758, 761]`, after lines `[735, 738]`
- `lc`: before `10`, after `8`, delta `-2`; before lines `[156, 171, 448, 450, 453, 728, 729, 758, 761, 762]`, after lines `[160, 175, 490, 492, 495, 735, 738, 739]`
- `REG_META`: before `4`, after `3`, delta `-1`; before lines `[11, 453, 729, 765]`, after lines `[11, 495, 742]`
- `trades`: before `9`, after `5`, delta `-4`; before lines `[207, 238, 577, 657, 708, 709, 744, 775, 1047]`, after lines `[278, 619, 699, 752, 1024]`
- `vr`: before `7`, after `3`, delta `-4`; before lines `[194, 197, 565, 566, 685, 686, 689]`, after lines `[198, 607, 608]`
- `e1`: before `187`, after `174`, delta `-13`; before lines `[7, 19, 156, 164, 165, 166, 167, 168, 169, 175, 176, 195, 196, 197, 198, 203, 204, 205, 206, 207]`, after lines `[7, 19, 142, 143, 160, 168, 169, 170, 171, 172, 173, 179, 180, 246, 266, 267, 268, 269, 273, 274]`
- `e1r`: before `154`, after `151`, delta `-3`; before lines `[7, 19, 156, 164, 165, 166, 167, 168, 169, 175, 176, 195, 196, 197, 198, 203, 204, 205, 206, 207]`, after lines `[7, 19, 142, 143, 160, 168, 169, 170, 171, 172, 173, 179, 180, 246, 267, 269, 273, 274, 275, 276]`
- `e1rFormal`: before `5`, after `4`, delta `-1`; before lines `[19, 156, 176, 196, 723]`, after lines `[19, 160, 180, 722]`
- `DATA.e1rFormal`: before `3`, after `2`, delta `-1`; before lines `[176, 196, 723]`, after lines `[180, 722]`

## Interpretation

- The key question is whether the removed block contained `const` / `let` / derived arrays that later code still references.
- If yes, the correct fix is to restore those non-UI lines, not to keep adding one-off variables after each runtime error.

## Recommended Next Step

- Review this audit output first.
- Then choose either a surgical restore of missing non-UI setup or a clean reapply from `c1a7e46` with a narrower patch.

