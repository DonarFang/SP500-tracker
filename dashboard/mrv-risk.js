/* Independent MRV view. No trading engine globals or decisions are changed. */
(() => {
  'use strict';
  const names = {light:'轻度', moderate:'中等', severe:'严重'};
  const esc = x => String(x ?? '—').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let current = null, cached = null, request = 0;
  const endpoint = new URL('../exports/mrv/', document.baseURI);
  async function get(name, optional=false) {
    const r = await fetch(new URL(name + '?t=' + Date.now(), endpoint), {cache:'no-store'});
    if (!r.ok) { if(optional && r.status===404)return null; throw Error(name + ' HTTP ' + r.status); }
    return r.json();
  }
  function percentages(p) {
    const keys=['light','moderate','severe'];
    if (!p || keys.some(k=>!Number.isFinite(p[k]) || p[k]<0 || p[k]>1) || Math.abs(keys.reduce((s,k)=>s+p[k],0)-1)>1e-8) return null;
    const exact=keys.map(k=>p[k]*1000), vals=exact.map(Math.floor);
    const order=[0,1,2].sort((a,b)=>(exact[b]-vals[b])-(exact[a]-vals[a]));
    for(let i=0,n=1000-vals.reduce((a,b)=>a+b,0);i<n;i++) vals[order[i%3]]++;
    return keys.map((k,i)=>p[k]>0 && p[k]<.001 ? '<0.1%' : (vals[i]/10).toFixed(1)+'%');
  }
  function render(data) {
    if(!current || !current.isConnected)return;
    const {status:s,prediction:p,history:h,error}=data;
    const now=Date.now();
    const stale=p && now>=Date.parse(p.data_ready_utc);
    const ended=p && now>=Date.parse(p.target_close_utc);
    const blocked=error || !s || s.status!=='READY' || !p || s.prediction_id!==p.prediction_id;
    const state=blocked?'更新受阻':stale?'已过期，等待更新':ended?'目标交易日已结束':p.evidence_class==='BEFORE_TARGET_OPEN'?'已留存开盘前预测':'补算记录，非事前预警';
    const pct=p && percentages(p.probabilities);
    const health=s?.calendar_health||p?.calendar_health||{};
    const cacheNames=Object.keys(health).filter(k=>health[k].calendar_mode==='CACHED');
    const grade=p && names[p.final_grade] ? p.final_grade : null;
    current.innerHTML=`<div class="mrv-heading"><div><span class="mrv-eyebrow">MRV · 下一交易日市场风险</span><h2>市场风险观察</h2></div><button type="button" class="mrv-refresh">刷新风险</button></div>
      <p class="mrv-status ${blocked||stale?'mrv-warning':''}" role="status">${esc(state)}${blocked?' · '+esc(error||s?.error||'尚无有效输出'):''}</p>
      ${cacheNames.length?`<p class="mrv-warning">事件日历使用短期缓存：${esc(cacheNames.join(' / '))}；本次在线刷新未成功。最长72小时，超期停止输出。</p>`:''}
      ${p?`<div class="mrv-main"><div><span class="mrv-muted">${blocked||stale?'上次记录':'T+1 风险预警'} · ${esc(p.target_date)}</span><div class="mrv-grade mrv-${esc(grade)}">${esc(names[grade]||'不可用')}</div><span class="mrv-muted">依据 T=${esc(p.feature_date)} 收盘数据</span></div><div class="mrv-probs">${['light','moderate','severe'].map((k,i)=>`<div><span>${names[k]}概率</span><strong>${pct?esc(pct[i]):'不可用'}</strong></div>`).join('')}</div></div>
      <p>${p.events?.length?'重要数据发布日：'+esc(p.events.join(' / '))+'。按既定规则标记严重；概率仍为模型估计。':'目标日无已确认的 CPI / 非农 / FOMC 决议发布。'}</p>
      <p class="mrv-muted">概率为校准后的观察估计，严重尾部样本有限。风险等级沿用冻结 LINEAR4，不由概率重新划分。</p>
      <details><summary>计算口径与来源</summary><dl><dt>LINEAR4 原始分数 / 严重门槛</dt><dd>${esc(Number(p.score).toPrecision(7))} / ${esc(Number(p.severe_threshold).toPrecision(7))}（严格大于）</dd><dt>模型等级 / 日历调整后等级</dt><dd>${esc(names[p.model_grade])} / ${esc(names[p.final_grade])}</dd><dt>四分数</dt><dd>${esc(JSON.stringify(p.four_scores))}</dd><dt>概率模型</dt><dd>P2_BETA FINAL · ${esc(p.probability_status)}</dd><dt>留存时间（UTC）</dt><dd>${esc(p.generated_utc)}${p.is_revision?' · 修订版，首次记录保留':''}</dd><dt>风险定义</dt><dd>D=max(0,1−T+1盘中最低价/T收盘价)。严重 D≥3%；中等 1.2%&lt;D&lt;3%；轻度 D≤1.2%。</dd><dt>事件日历核验</dt><dd>${esc(JSON.stringify(health))}</dd><dt>数据</dt><dd>SPX、VIX 日线与 CBOE VIX9D/VIX3M；BLS、Fed 发布日历。仅 T 收盘及以前价格，无盘前输入。</dd></dl></details>`:'<p>尚未生成有效风险预测。请检查每日运行证据。</p>'}
      <details><summary>最近首次留存记录</summary><div class="mrv-table"><table><thead><tr><th>目标日</th><th>预警</th><th>实际</th><th>记录性质</th></tr></thead><tbody>${(Array.isArray(h)?h:[]).slice(-20).reverse().map(r=>`<tr><td>${esc(r.target_date)}</td><td>${esc(names[r.final_grade])}</td><td>${esc(r.actual?names[r.actual.class]:'待成熟')}</td><td>${r.evidence_class==='BEFORE_TARGET_OPEN'?'开盘前留存':'事后补算'}</td></tr>`).join('')}</tbody></table></div></details>`;
    current.querySelector('button').addEventListener('click',load);
  }
  async function load() {
    const id=++request;
    try {const [s,p,h]=await Promise.all([get('status.json'),get('latest.json',true),get('history.json',true)]);if(id!==request)return; cached={status:s,prediction:p,history:h};}
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
