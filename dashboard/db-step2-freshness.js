/* db-step2-freshness-v1: browser-clock check independent of Live generation. */
(function () {
  'use strict';
  function expectedDate(calendar, now) {
    const today = now.toISOString().slice(0, 10);
    if (today < calendar.coverage_start || today > calendar.coverage_end) throw Error('交易日历已超出覆盖范围');
    const closed = new Set([...calendar.full_day_closures, ...(calendar.extraordinary_full_day_closures || [])]);
    let day = new Date(today + 'T00:00:00Z');
    for (let i = 0; i < 15; i++, day = new Date(day.getTime() - 86400000)) {
      const d = day.toISOString().slice(0, 10), w = day.getUTCDay();
      if (w !== 0 && w !== 6 && !closed.has(d) && now.getTime() >= day.getTime() + 86400000 + 45 * 60000) {
        if (d < calendar.coverage_start) throw Error('交易日历缺少所需日期');
        return d;
      }
    }
    throw Error('无法确定应更新交易日');
  }
  if (typeof module !== 'undefined') { module.exports = {expectedDate}; return; }
  const banner = document.createElement('div');
  banner.id = 'db-step2-status'; banner.setAttribute('role', 'status');
  banner.style.cssText = 'position:sticky;top:0;z-index:10000;padding:14px 20px;font:600 15px/1.6 sans-serif;border-bottom:3px solid #b45309;white-space:pre-wrap';
  document.body.prepend(banner);
  let busy = false;
  function show(text, ok) {
    banner.textContent = text; banner.style.background = ok ? '#dcfce7' : '#fef3c7';
    banner.style.color = ok ? '#14532d' : '#7c2d12';
  }
  async function read(path) {
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 15000);
    try {
      const r = await fetch(new URL('../' + path + '?db_step2=' + Date.now(), document.baseURI), {cache:'no-store',signal:controller.signal});
      if (!r.ok) throw Error('HTTP ' + r.status);
      const bytes = await r.arrayBuffer();
      return {bytes, value:JSON.parse(new TextDecoder().decode(bytes))};
    } finally { clearTimeout(timer); }
  }
  async function hash(bytes) {
    return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), b => b.toString(16).padStart(2,'0')).join('');
  }
  async function check() {
    if (busy) return; busy = true;
    show('Live：正在核验公开数据。核验完成前，请勿将旧建议视为今日操作指令。', false);
    try {
      const root = 'exports/official/FD-M3180125-SP500-TOP3-engine/live/';
      const [cal, state, rec, market] = await Promise.all([
        read('config/live_calendar/us_equity_calendar_v1.0.json'), read(root+'runtime/current/runtime_state.json'),
        read(root+'runtime/current/latest_recommendations.json'), read(root+'runtime/current/latest_market_status.json')]);
      const now = new Date(), expected = expectedDate(cal.value, now), actual = state.value.last_committed_market_date;
      if (typeof actual !== 'string' || actual < expected) throw Error('数据过期：应至少更新至 '+expected+'，实际为 '+(actual || '未知'));
      if (actual > now.toISOString().slice(0,10) || rec.value.signal_date !== actual || market.value.date !== actual) throw Error('公开数据日期不一致');
      if (state.value.status !== 'ACTIVE' || rec.value.recommendation_only !== true) throw Error('Live 状态异常');
      const manifest = (await read(root+'runtime/daily/'+actual+'/manifest.json')).value;
      if (manifest.validation_status !== 'PASS' || manifest.market_date !== actual ||
          (await hash(rec.bytes)) !== manifest.files['engine_recommendations.json']) throw Error('建议与当日验证记录不一致');
      if ((await hash(market.bytes)) !== manifest.files['market_status.json']) throw Error('行情状态与当日验证记录不一致');
      show('Live 数据已核验｜信号日 '+actual+'｜建议执行日 '+rec.value.expected_execution_date+'｜核验时间 '+now.toLocaleTimeString()+'\n每日更新检查期限：台湾时间 08:45；此状态不代表已经成交。',true);
    } catch (e) {
      show('⚠ Live 更新异常或尚未核验：'+e.message+'\n下面可能是旧建议，请勿视为当前交易指令。',false);
    } finally {busy = false;}
  }
  check(); setInterval(check, 60000); window.addEventListener('focus',check);
  window.addEventListener('online',check);
})();
