/* Independent MRV view. No trading engine globals or decisions are changed. */
(() => {
  'use strict';
  const names = {light:'轻度', moderate:'中度', severe:'严重'};
  const esc = x => String(x ?? '—').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let current = null, cached = null, request = 0;
  const endpoint = new URL('../exports/mrv/', document.baseURI);
  async function get(name, optional=false) {
    const r = await fetch(new URL(name + '?t=' + Date.now(), endpoint), {cache:'no-store'});
    if (!r.ok) { if(optional && r.status===404)return null; throw Error(name + ' HTTP ' + r.status); }
    return r.json();
  }
  function render(data) {
    if(!current || !current.isConnected)return;
    const {status:s,prediction:p,history:h,preparation:a,error}=data;
    const now=Date.now();
    const stale=p && now>=Date.parse(p.data_ready_utc);
    const ended=p && now>=Date.parse(p.target_close_utc);
    const blocked=error || !s || s.status!=='READY' || s.model!=='J4_joint' || p?.model!=='J4_joint' || !p || s.prediction_id!==p.prediction_id;
    const state=!s&&!p&&!error?'等待首次 J4 观察':blocked?'更新受阻':stale?'已过期，等待更新':ended?'目标交易日已结束':p.evidence_class==='BEFORE_TARGET_OPEN'?'已留存开盘前预测':'补算记录，非事前预警';

    const health=s?.calendar_health||p?.calendar_health||{};
    const localCalendar=health.LOCAL;
    const calendarOverdue=localCalendar && (localCalendar.review_overdue || now>=Date.parse(localCalendar.review_due_utc));
    const cacheNames=Object.keys(health).filter(k=>health[k].calendar_mode==='CACHED');
    const annual=a||health.ANNUAL_PREPARATION;
    const next=annual?.years?.[String(annual.next_year)];
    const annualLabel=next?.available?(next.pending_changes?'已备妥，发现变更待复核':'已备妥'):next?.review_status==='FAILED'?'尚未备妥，获取或验证未通过':'等待首次检查';
    const grade=p && names[p.final_grade] ? p.final_grade : null;
    current.innerHTML=`<div class="mrv-heading"><div><span class="mrv-eyebrow">MRV · J4 · 下一交易日市场风险</span><h2>市场风险观察 · J4</h2></div><button type="button" class="mrv-refresh">刷新风险</button></div>
      <p class="mrv-status ${blocked||stale?'mrv-warning':''}" role="status">${esc(state)}${blocked?' · '+esc(error||s?.error||'尚无有效输出'):''}</p>
      ${localCalendar?`<p class="${calendarOverdue||localCalendar.pending_changes?'mrv-warning':'mrv-muted'}">事件日历：本地核实版，每14天复核。上次核实 ${esc(localCalendar.verified_utc?.slice(0,10))}；下次复核 ${esc(localCalendar.review_due_utc?.slice(0,10))}；覆盖至 ${esc(localCalendar.coverage_end)}。${localCalendar.pending_changes?' 检测到日期变更，等待核实；暂沿用原日历。':calendarOverdue?' 复核逾期，暂沿用原日历；近期改期可能尚未纳入。':''}</p>`:cacheNames.length?`<p class="mrv-warning">此记录使用旧版事件日历缓存，请等待新版每日运行。</p>`:''}
      ${annual?.preparation_enabled?`<p class="${next?.available&&!next?.pending_changes?'mrv-muted':'mrv-warning'}">跨年准备：${esc(annual.next_year)} 年事件日历${esc(annualLabel)}。每14天检查。${next?.next_attempt_utc?'下次尝试 '+esc(next.next_attempt_utc.slice(0,10))+'。':''}${next?.error?'原因：'+esc(next.error):''}</p>`:''}
      ${p?`<div class="mrv-main"><div><span class="mrv-muted">${blocked||stale?'上次记录':'T+1 风险预警'} · ${esc(p.target_date)}</span><div class="mrv-grade mrv-${esc(grade)}">${esc(names[grade]||'不可用')}</div><span class="mrv-muted">依据 T=${esc(p.feature_date)} 收盘数据</span></div><div><span class="mrv-muted">J4 原始预警</span><strong> ${esc(names[p.model_grade])}</strong></div></div>
      <p>${p.events?.length?'日历上调：'+esc(p.events.map(e=>e[1]+' '+e[0]+'（'+e[2]+'）').join(' / '))+'，最终按严重观察。':(calendarOverdue||localCalendar?.pending_changes?'现用日历未列出发布日或其下一交易日；复核逾期或变更待确认。':'目标日不在已核实的 CPI、非农、FOMC 发布日及其下一交易日窗口。')}</p>
      <p class="mrv-muted">观察模型；历史验证未达全部目标。报轻度仍可能发生中度下跌。三档概率尚未校准。</p>
      <details><summary>计算口径与来源</summary><dl><dt>非轻度分数 / 轻度门槛</dt><dd>${esc(p.score_nonmild.toFixed(6))} / ${esc(p.thresholds[0].toFixed(6))}</dd><dt>严重分数 / 严重门槛</dt><dd>${esc(p.score_severe.toFixed(6))} / ${esc(p.thresholds[1].toFixed(6))}。先判严重（严格大于），否则非轻度分数不超过轻度门槛则报轻度，其余报中度。分数不是概率。</dd><dt>留存时间（UTC）</dt><dd>${esc(p.generated_utc)}${p.is_revision?' · 修订版，首次记录保留':''}</dd><dt>风险定义</dt><dd>D=max(0,1−T+1盘中最低价/T收盘价)。严重 D&gt;2.5%；中度 1.2%&lt;D≤2.5%；轻度 D≤1.2%。</dd><dt>事件日历核验</dt><dd>${esc(JSON.stringify(health))}</dd><dt>数据</dt><dd>SPX 日线与 CBOE VIX 收盘值；BLS、Fed 发布日历。仅 T 收盘及以前价格，无盘前输入。</dd></dl></details>`:'<p>尚未生成有效风险预测。请检查每日运行证据。</p>'}
      <p><a class="mrv-muted" href="${esc(new URL('history.json',endpoint).href)}">查看 LINEAR4 历史记录（旧口径）</a></p>
      <details><summary>J4 最近首次留存记录</summary><div class="mrv-table"><table><thead><tr><th>目标日</th><th>预警</th><th>实际</th><th>记录性质</th></tr></thead><tbody>${(Array.isArray(h)?h:[]).slice(-20).reverse().map(r=>`<tr><td>${esc(r.target_date)}</td><td>${esc(names[r.final_grade])}</td><td>${esc(r.actual?names[r.actual.class]:'待成熟')}</td><td>${r.evidence_class==='BEFORE_TARGET_OPEN'?'开盘前留存':'事后补算'}</td></tr>`).join('')}</tbody></table></div></details>`;
    current.querySelector('button').addEventListener('click',load);
  }
  async function load() {
    const id=++request;
    try {const [s,p,h,a]=await Promise.all([get('j4/status.json',true),get('j4/latest.json',true),get('j4/history.json',true),get('calendar-preparation.json',true)]);if(id!==request)return; cached={status:s,prediction:p?.model==='J4_joint'?p:null,history:h,preparation:a};}
    catch(e){if(id!==request)return;cached={...(cached||{}),error:String(e)};}
    render(cached);
  }
  function mount() {
    const root=document.getElementById('s-step3-us-market');
    const grid=root?.querySelector('.d1-index-grid');
    if(!grid)return;
    if(current?.isConnected && current.parentElement===grid.parentElement)return;
    current=document.createElement('section');current.id='mrv-market-risk';current.className='card mrv-risk';current.setAttribute('aria-label','下一交易日市场风险');
    grid.insertAdjacentElement('afterend',current);current.textContent='正在加载 MRV 风险预测…';
    if(cached)render(cached);else load();
  }
  new MutationObserver(mount).observe(document.body,{subtree:true,childList:true});mount();
  setInterval(()=>{if(cached)render(cached);},60000);
})();
