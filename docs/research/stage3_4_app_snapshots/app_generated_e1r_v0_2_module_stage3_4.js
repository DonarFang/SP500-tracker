/* === E1R_V0_2_DASHBOARD_MODULE_STAGE_3_4_CLEAN_INTEGRATION === */
(function () {
  "use strict";

  const E1R_V02_PATHS = {
    status: "exports/e1r_v0_2_status.json",
    oosSummary: "exports/oos_e1r_v0_2_summary.json",
    sidecar: "exports/oos_e1r_v0_2_sidecar.json",
    positions: "exports/oos_e1r_v0_2_positions.json",
    orders: "exports/oos_e1r_v0_2_orders.json",
    oosEquity: "exports/oos_e1r_v0_2_equity_curve.json",
    lifecycle: "exports/oos_e1r_v0_2_sidecar_lifecycle.json",
    turnover: "exports/oos_e1r_v0_2_sidecar_turnover.json",
    backtestSummary: "exports/e1r_v0_2_backtest_summary.json",
    backtestEquity: "exports/e1r_v0_2_backtest_equity_curve.json"
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
