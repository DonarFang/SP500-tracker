/* === E1R_V0_2_STAGE3_8B_RESEARCH_BACKTEST_REFACTOR === */
(function () {
  "use strict";

  const RB38B_PATHS = {
    backtest: "../exports/backtest.json",
    tradeLog: "../exports/trade_log.json",
    e1rStatus: "../exports/e1r_v0_2_status.json",
    e1rBacktestSummary: "../exports/e1r_v0_2_backtest_summary.json",
    e1rBacktestEquity: "../exports/e1r_v0_2_backtest_equity_curve.json",
    e1OosSummary: "../exports/oos_summary.json",
    e1OosPositions: "../exports/oos_positions.json",
    e1OosTrades: "../exports/oos_trades.json",
    e1OosEquity: "../exports/oos_equity_curve.json",
    e1OosOrders: "../exports/oos_orders.json",
    e1rOosSummary: "../exports/oos_e1r_v0_2_summary.json",
    e1rOosSidecar: "../exports/oos_e1r_v0_2_sidecar.json",
    e1rOosPositions: "../exports/oos_e1r_v0_2_positions.json",
    e1rOosOrders: "../exports/oos_e1r_v0_2_orders.json",
    e1rOosEquity: "../exports/oos_e1r_v0_2_equity_curve.json",
    e1rOosLifecycle: "../exports/oos_e1r_v0_2_sidecar_lifecycle.json",
    e1rOosTurnover: "../exports/oos_e1r_v0_2_sidecar_turnover.json",
    marketState: "../exports/market_state.json",
    marketRegimeOptional: "../exports/market_regime.json"
  };

  const RB38B_VARIANTS = {
    e1: "E1_AUDITED_G4_MINHOLD10",
    e1r: "E1R_REGIME_AWARE_V0_2",
    spx: "SPX"
  };

  const RB38B_LEGACY_HEADINGS = [
    "E1-R Research Summary",
    "Period comparison",
    "E1R v0.2 Market / OOS Status",
    "E1R v0.2 5Y Backtest",
    "E1R v0.2 Forward / OOS Equity",
    "E2 Dynamic Exit"
  ];

  function rb38bEscape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function rb38bNum(value, digits = 2) {
    const n = Number(value);
    if (!Number.isFinite(n)) return "N/A";
    return n.toLocaleString(undefined, {
      maximumFractionDigits: digits,
      minimumFractionDigits: digits
    });
  }

  function rb38bPct(value, digits = 2) {
    const n = Number(value);
    if (!Number.isFinite(n)) return "N/A";
    const scaled = Math.abs(n) <= 1 ? n * 100 : n;
    const sign = scaled > 0 ? "+" : "";
    return `${sign}${scaled.toFixed(digits)}%`;
  }

  function rb38bPick(obj, keys, fallback = null) {
    if (!obj || typeof obj !== "object") return fallback;
    for (const key of keys) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const v = obj[key];
        if (v !== null && v !== undefined && v !== "") return v;
      }
    }
    return fallback;
  }

  function rb38bArray(payload) {
    if (Array.isArray(payload)) return payload;
    if (!payload || typeof payload !== "object") return [];
    for (const key of ["rows", "records", "data", "items", "equity_curve", "curve", "positions", "orders", "trades"]) {
      if (Array.isArray(payload[key])) return payload[key];
    }
    return [];
  }

  function rb38bLatest(payload) {
    const arr = rb38bArray(payload);
    if (arr.length) return arr[arr.length - 1] || {};
    if (payload && typeof payload === "object") {
      return payload.latest || payload.summary || payload.status || payload.v0_2 || payload;
    }
    return {};
  }

  async function rb38bFetchJson(path, optional = false) {
    try {
      const sep = path.includes("?") ? "&" : "?";
      const res = await fetch(`${path}${sep}_=${Date.now()}`, { cache: "no-store" });
      if (!res.ok) return { ok: false, optional, path, status: res.status, data: null };
      return { ok: true, optional, path, status: res.status, data: await res.json() };
    } catch (error) {
      return {
        ok: false,
        optional,
        path,
        status: "FETCH_ERROR",
        data: null,
        error: String(error && error.message ? error.message : error)
      };
    }
  }

  function rb38bDeepFind(obj, predicate, path = "$", depth = 0, maxDepth = 12, out = []) {
    if (depth > maxDepth || out.length > 200) return out;
    try {
      if (predicate(obj, path)) out.push({ value: obj, path });
    } catch (_) {}

    if (Array.isArray(obj)) {
      for (let i = 0; i < Math.min(obj.length, 5000); i += 1) {
        rb38bDeepFind(obj[i], predicate, `${path}[${i}]`, depth + 1, maxDepth, out);
      }
    } else if (obj && typeof obj === "object") {
      for (const [key, value] of Object.entries(obj)) {
        rb38bDeepFind(value, predicate, `${path}.${key}`, depth + 1, maxDepth, out);
      }
    }
    return out;
  }

  function rb38bFindVariant(payload, variantName) {
    const hits = rb38bDeepFind(payload, (obj) => {
      if (!obj || typeof obj !== "object" || Array.isArray(obj)) return false;
      const name = rb38bPick(obj, ["variant", "name", "strategy", "strategy_variant", "id", "variant_id"]);
      if (name === variantName) return true;
      try {
        return JSON.stringify(obj).slice(0, 2000).includes(variantName);
      } catch (_) {
        return false;
      }
    });
    return hits.length ? hits[0].value : null;
  }

  function rb38bFindSummary(payload, variantName) {
    if (!payload) return {};
    if (payload.v0_2 && variantName === RB38B_VARIANTS.e1r) return payload.v0_2;
    const variant = rb38bFindVariant(payload, variantName);
    if (variant) return variant;
    if (payload.summary && typeof payload.summary === "object") return payload.summary;
    if (payload.latest && typeof payload.latest === "object") return payload.latest;
    return payload && typeof payload === "object" ? payload : {};
  }

  function rb38bNormalizeEquityRows(rows, options = {}) {
    const out = [];
    const equityKeys = options.equityKeys || [
      "equity",
      "combined_equity",
      "portfolio_value",
      "strategy_equity",
      "value",
      "nav",
      "balance",
      "close"
    ];

    for (const row of rows || []) {
      if (!row || typeof row !== "object") continue;

      const date = rb38bPick(row, ["date", "status_date", "as_of", "timestamp", "datetime", "day"]);
      let equity = null;

      for (const key of equityKeys) {
        const v = rb38bPick(row, [key]);
        if (Number.isFinite(Number(v))) {
          equity = Number(v);
          break;
        }
      }

      if (!date || !Number.isFinite(Number(equity))) continue;

      out.push({
        ...row,
        date: String(date).slice(0, 10),
        equity: Number(equity)
      });
    }

    return out.sort((a, b) => String(a.date).localeCompare(String(b.date)));
  }

  function rb38bFindEquitySeries(payload, options = {}) {
    const candidates = [];

    const isRows = (arr) => {
      if (!Array.isArray(arr) || arr.length < 1) return false;
      const sample = arr.slice(0, Math.min(20, arr.length));
      let score = 0;
      for (const row of sample) {
        if (!row || typeof row !== "object") continue;
        const keys = Object.keys(row).map(String);
        if (keys.some(k => ["date", "status_date", "as_of", "timestamp", "datetime", "day"].includes(k))) score += 2;
        if (keys.some(k => k.toLowerCase().includes("equity") || ["portfolio_value", "nav", "balance", "value"].includes(k))) score += 3;
      }
      return score >= Math.min(4, sample.length * 2);
    };

    rb38bDeepFind(payload, (obj, path) => {
      if (Array.isArray(obj) && isRows(obj)) {
        const rows = rb38bNormalizeEquityRows(obj, options);
        if (rows.length) {
          candidates.push({
            path,
            rows,
            rowCount: rows.length,
            score: rows.length + (String(path).toLowerCase().includes("equity") ? 1000 : 0)
          });
        }
      }
      return false;
    }, "$", 0, 12, []);

    candidates.sort((a, b) => b.score - a.score);
    return candidates.length ? candidates[0].rows : [];
  }

  function rb38bSeriesReturn(rows) {
    if (!rows || rows.length < 2) return null;
    const first = Number(rows[0].equity);
    const last = Number(rows[rows.length - 1].equity);
    if (!Number.isFinite(first) || !Number.isFinite(last) || first === 0) return null;
    return (last / first) - 1;
  }

  function rb38bMetric(summary, aliases) {
    return rb38bPick(summary, aliases, null);
  }

  function rb38bIndexSeries(rows, base = 100) {
    if (!rows || rows.length < 1) return [];
    const first = Number(rows[0].equity);
    if (!Number.isFinite(first) || first === 0) return [];
    return rows.map(row => ({
      x: row.date,
      y: Number((Number(row.equity) / first * base).toFixed(4))
    })).filter(row => row.x && Number.isFinite(row.y));
  }

  function rb38bFindResearchHost() {
    const existing = document.getElementById("rb38b-research-backtest-refactor");
    if (existing && existing.parentElement) return existing.parentElement;

    const active = document.querySelector(".tab-content.active, .tab-pane.active, [data-tab-content].active");
    if (active) return active;

    const textNeedles = ["E1_AUDITED_G4_MINHOLD10", "Period comparison", "Trade log", "E1-R Research Summary"];
    const candidates = Array.from(document.querySelectorAll("section, article, div, main"));
    for (const needle of textNeedles) {
      const hit = candidates.find(el => {
        const text = el.textContent || "";
        return text.includes(needle) && text.length < 80000 && el !== document.body;
      });
      if (hit) {
        let node = hit;
        for (let i = 0; i < 4 && node.parentElement && node.parentElement !== document.body; i += 1) {
          if ((node.parentElement.textContent || "").includes(needle) && (node.parentElement.textContent || "").length < 120000) {
            node = node.parentElement;
          }
        }
        return node.parentElement || node;
      }
    }

    return document.querySelector("main") || document.body;
  }

  function rb38bFindFirstLegacyBlock() {
    const candidates = Array.from(document.querySelectorAll("h1,h2,h3,h4,section,article,div"));
    for (const phrase of RB38B_LEGACY_HEADINGS) {
      const hit = candidates.find(el => {
        const text = (el.textContent || "").trim();
        return text.includes(phrase) && text.length < 30000 && el !== document.body;
      });
      if (hit) return rb38bClosestBlock(hit);
    }
    return null;
  }

  function rb38bClosestBlock(el) {
    let node = el;
    for (let i = 0; i < 6 && node && node.parentElement && node.parentElement !== document.body; i += 1) {
      const cls = String(node.className || "").toLowerCase();
      const id = String(node.id || "").toLowerCase();
      const tag = String(node.tagName || "").toLowerCase();
      const textLen = (node.textContent || "").length;
      if (
        tag === "section" ||
        tag === "article" ||
        cls.includes("card") ||
        cls.includes("panel") ||
        cls.includes("section") ||
        id.includes("research") ||
        id.includes("backtest") ||
        (textLen > 100 && textLen < 25000)
      ) {
        return node;
      }
      node = node.parentElement;
    }
    return el;
  }

  function rb38bHideLegacyBlocks(root) {
    const protectedRoot = document.getElementById("rb38b-research-backtest-refactor");
    const candidates = Array.from(document.querySelectorAll("section, article, div"));

    for (const el of candidates) {
      if (!el || el === document.body || el === root || el === protectedRoot || (protectedRoot && protectedRoot.contains(el))) continue;

      const text = (el.textContent || "").trim();
      if (!text || text.length > 60000) continue;

      const matches = RB38B_LEGACY_HEADINGS.some(phrase => text.includes(phrase));
      if (!matches) continue;

      const block = rb38bClosestBlock(el);
      if (!block || block === document.body || block === protectedRoot || (protectedRoot && protectedRoot.contains(block))) continue;
      block.classList.add("rb38b-hidden-legacy");
      block.setAttribute("data-rb38b-hidden-reason", "replaced-by-stage-3-8b-unified-research-backtest-layout");
    }
  }

  function rb38bEnsureRoot() {
    let root = document.getElementById("rb38b-research-backtest-refactor");
    if (root) return root;

    const host = rb38bFindResearchHost();
    const firstLegacy = rb38bFindFirstLegacyBlock();

    root = document.createElement("section");
    root.id = "rb38b-research-backtest-refactor";
    root.className = "rb38b-shell";
    root.setAttribute("data-stage", "3.8B");
    root.innerHTML = `
      <div class="rb38b-loading">
        <strong>Research & Backtest</strong>
        <span>Loading unified E1 / E1R / SPX view…</span>
      </div>
    `;

    if (firstLegacy && firstLegacy.parentElement) {
      firstLegacy.parentElement.insertBefore(root, firstLegacy);
    } else {
      host.appendChild(root);
    }

    return root;
  }

  function rb38bRenderCurve(data) {
    const datasets = [
      { label: "E1 historical frozen", data: rb38bIndexSeries(data.e1HistRows), borderWidth: 2, tension: 0.2 },
      { label: "E1 forward paper", data: rb38bIndexSeries(data.e1ForwardRows), borderWidth: 2, borderDash: [6, 4], tension: 0.2 },
      { label: "E1R v0.2 historical frozen", data: rb38bIndexSeries(data.e1rHistRows), borderWidth: 2, tension: 0.2 },
      { label: "E1R v0.2 forward paper", data: rb38bIndexSeries(data.e1rForwardRows), borderWidth: 2, borderDash: [6, 4], tension: 0.2 },
      { label: "SPX buy & hold", data: rb38bIndexSeries(data.spxRows), borderWidth: 2, borderDash: [3, 3], tension: 0.2 }
    ].filter(ds => Array.isArray(ds.data) && ds.data.length > 1);

    const status = datasets.length ? `${datasets.length} series loaded` : "No plottable equity series found";

    return `
      <section class="rb38b-card rb38b-curve-card">
        <div class="rb38b-card-head">
          <div>
            <h2>Equity Curve — E1 vs E1R v0.2 vs SPX</h2>
            <p>Historical frozen research segment + forward paper-tracking segment. Strategy logic unchanged.</p>
          </div>
          <span class="rb38b-badge">${rb38bEscape(status)}</span>
        </div>
        <div class="rb38b-chart-wrap">
          <canvas id="rb38b-equity-curve-canvas" height="120"></canvas>
        </div>
        <div class="rb38b-footnote">
          Historical E1R v0.2 data is a frozen research artifact. Forward tracking is the primary validation source.
        </div>
      </section>
    `;
  }

  function rb38bMountChart(data) {
    const canvas = document.getElementById("rb38b-equity-curve-canvas");
    if (!canvas || typeof Chart === "undefined") return;

    if (window.__RB38B_CHART__) {
      try { window.__RB38B_CHART__.destroy(); } catch (_) {}
    }

    const datasets = [
      { label: "E1 historical frozen", data: rb38bIndexSeries(data.e1HistRows), borderWidth: 2, tension: 0.2 },
      { label: "E1 forward paper", data: rb38bIndexSeries(data.e1ForwardRows), borderWidth: 2, borderDash: [6, 4], tension: 0.2 },
      { label: "E1R v0.2 historical frozen", data: rb38bIndexSeries(data.e1rHistRows), borderWidth: 2, tension: 0.2 },
      { label: "E1R v0.2 forward paper", data: rb38bIndexSeries(data.e1rForwardRows), borderWidth: 2, borderDash: [6, 4], tension: 0.2 },
      { label: "SPX buy & hold", data: rb38bIndexSeries(data.spxRows), borderWidth: 2, borderDash: [3, 3], tension: 0.2 }
    ].filter(ds => Array.isArray(ds.data) && ds.data.length > 1);

    if (!datasets.length) return;

    window.__RB38B_CHART__ = new Chart(canvas.getContext("2d"), {
      type: "line",
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        parsing: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { display: true },
          tooltip: { callbacks: { title(items) { return items && items.length ? items[0].raw.x : ""; } } }
        },
        scales: {
          x: { type: "category", ticks: { maxTicksLimit: 8 }, grid: { display: false } },
          y: { title: { display: true, text: "Indexed to 100" }, ticks: { callback: value => Number(value).toFixed(0) } }
        }
      }
    });
  }

  function rb38bSummaryRows(data) {
    const e1HistReturn = rb38bMetric(data.e1Summary, ["total_return", "full_return", "return", "strategy_return"]);
    const e1rHistReturn = rb38bMetric(data.e1rSummary, ["total_return", "full_return", "return", "strategy_return"]);
    const spxHistReturn = rb38bMetric(data.e1Summary, ["spx_return", "benchmark_return"]);
    const e1ForwardReturn = rb38bSeriesReturn(data.e1ForwardRows);
    const e1rForwardReturn = rb38bSeriesReturn(data.e1rForwardRows);
    const spxReturn = rb38bSeriesReturn(data.spxRows);

    return [
      ["Status", "Frozen benchmark + paper tracking", "Frozen research candidate + paper tracking", "Benchmark"],
      ["Historical return", rb38bPct(e1HistReturn), rb38bPct(e1rHistReturn), rb38bPct(spxHistReturn ?? spxReturn)],
      ["Forward return", rb38bPct(e1ForwardReturn), rb38bPct(e1rForwardReturn), "N/A"],
      ["MaxDD", rb38bPct(rb38bMetric(data.e1Summary, ["max_drawdown", "max_dd"])), rb38bPct(rb38bMetric(data.e1rSummary, ["max_drawdown", "max_dd"])), "N/A"],
      ["Sharpe", rb38bNum(rb38bMetric(data.e1Summary, ["sharpe", "sharpe_ratio"])), rb38bNum(rb38bMetric(data.e1rSummary, ["sharpe", "sharpe_ratio"])), "N/A"],
      ["Profit factor", rb38bNum(rb38bMetric(data.e1Summary, ["profit_factor", "pf"])), rb38bNum(rb38bMetric(data.e1rSummary, ["profit_factor", "pf"])), "N/A"],
      ["Trades", rb38bEscape(rb38bMetric(data.e1Summary, ["trades", "trade_count"]) ?? "N/A"), rb38bEscape(rb38bMetric(data.e1rSummary, ["trades", "trade_count"]) ?? "N/A"), "N/A"],
      ["Forward rows", rb38bEscape(data.e1ForwardRows.length), rb38bEscape(data.e1rForwardRows.length), "N/A"],
      ["Last update", rb38bEscape(data.e1LastDate || "N/A"), rb38bEscape(data.e1rLastDate || "N/A"), rb38bEscape(data.spxLastDate || "N/A")]
    ];
  }

  function rb38bRenderSummary(data) {
    const rows = rb38bSummaryRows(data).map(row => `
      <tr>
        <th>${rb38bEscape(row[0])}</th>
        <td>${row[1]}</td>
        <td>${row[2]}</td>
        <td>${row[3]}</td>
      </tr>
    `).join("");

    return `
      <section class="rb38b-card">
        <div class="rb38b-card-head">
          <div>
            <h2>Strategy Summary Comparison</h2>
            <p>E1 and E1R v0.2 are compared side by side. Forward metrics update from paper-tracking exports.</p>
          </div>
          <span class="rb38b-badge rb38b-badge-warn">No strategy logic changes</span>
        </div>
        <div class="rb38b-table-wrap">
          <table class="rb38b-table rb38b-summary-table">
            <thead>
              <tr>
                <th>Metric</th>
                <th>E1</th>
                <th>E1R v0.2</th>
                <th>SPX</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
        <div class="rb38b-footnote">
          Historical 3Y/5Y results are research / in-sample evidence. Forward paper tracking is the main validation path.
        </div>
      </section>
    `;
  }

  function rb38bFindTradeRows(payload) {
    const direct = rb38bArray(payload);
    if (direct.length && direct.some(row => row && typeof row === "object" && ("symbol" in row || "ticker" in row))) return direct;

    const hits = [];
    rb38bDeepFind(payload, (obj, path) => {
      if (!Array.isArray(obj) || !obj.length) return false;
      const sample = obj.slice(0, Math.min(20, obj.length));
      let score = 0;
      for (const row of sample) {
        if (!row || typeof row !== "object") continue;
        const keys = Object.keys(row).map(k => k.toLowerCase());
        if (keys.includes("symbol") || keys.includes("ticker")) score += 2;
        if (keys.includes("entry_date") || keys.includes("exit_date") || keys.includes("date")) score += 1;
        if (keys.includes("return") || keys.includes("pnl") || keys.includes("exit_reason")) score += 1;
      }
      if (score >= 3) hits.push({ path, rows: obj, score: score + obj.length });
      return false;
    });

    hits.sort((a, b) => b.score - a.score);
    return hits.length ? hits[0].rows : [];
  }

  function rb38bNormalizeTrade(row, strategy, source) {
    if (!row || typeof row !== "object") return null;
    const symbol = rb38bPick(row, ["symbol", "ticker", "asset"]);
    if (!symbol) return null;

    return {
      strategy: rb38bPick(row, ["strategy", "variant"], strategy),
      symbol,
      entry: rb38bPick(row, ["entry_date", "entry", "open_date", "buy_date", "date"]),
      exit: rb38bPick(row, ["exit_date", "exit", "close_date", "sell_date"], rb38bPick(row, ["status"]) === "OPEN" ? "OPEN" : ""),
      entryPrice: rb38bPick(row, ["entry_price", "entry_px", "buy_price", "entry_value"]),
      exitPrice: rb38bPick(row, ["exit_price", "exit_px", "sell_price", "current_price", "mark_price"]),
      ret: rb38bPick(row, ["return", "ret", "pnl_pct", "trade_return"]),
      days: rb38bPick(row, ["days", "holding_days", "days_held"]),
      state: rb38bPick(row, ["market_state", "regime", "state"], ""),
      reason: rb38bPick(row, ["exit_reason", "reason"], ""),
      source
    };
  }

  function rb38bRenderTradeLog(data) {
    const rows = [];

    for (const row of data.e1TradeRows) {
      const normalized = rb38bNormalizeTrade(row, "E1", "Historical");
      if (normalized) rows.push(normalized);
    }
    for (const row of data.e1ForwardTradeRows) {
      const normalized = rb38bNormalizeTrade(row, "E1", "Forward");
      if (normalized) rows.push(normalized);
    }
    for (const row of data.e1rForwardTradeRows) {
      const normalized = rb38bNormalizeTrade(row, "E1R v0.2", "Forward");
      if (normalized) rows.push(normalized);
    }

    rows.sort((a, b) => String(b.exit || b.entry || "").localeCompare(String(a.exit || a.entry || "")));

    const recent = rows.slice(0, 25);

    const body = recent.length ? recent.map(row => `
      <tr>
        <td>${rb38bEscape(row.strategy)}</td>
        <td><strong>${rb38bEscape(row.symbol)}</strong></td>
        <td>${rb38bEscape(row.entry || "")}</td>
        <td>${rb38bEscape(row.exit || "OPEN")}</td>
        <td>${row.entryPrice == null ? "N/A" : rb38bNum(row.entryPrice)}</td>
        <td>${row.exitPrice == null ? "N/A" : rb38bNum(row.exitPrice)}</td>
        <td>${row.ret == null ? "N/A" : rb38bPct(row.ret)}</td>
        <td>${rb38bEscape(row.days || "")}</td>
        <td>${rb38bEscape(row.state || "")}</td>
        <td>${rb38bEscape(row.source)}</td>
        <td>${rb38bEscape(row.reason || "")}</td>
      </tr>
    `).join("") : `
      <tr><td colspan="11">No trade rows available from current exports.</td></tr>
    `;

    return `
      <section class="rb38b-card">
        <div class="rb38b-card-head">
          <div>
            <h2>Trade Log</h2>
            <p>Recent historical and paper-tracking trades. Period comparison has been removed from the main view.</p>
          </div>
          <span class="rb38b-badge">${recent.length} rows</span>
        </div>
        <div class="rb38b-table-wrap">
          <table class="rb38b-table rb38b-trade-table">
            <thead>
              <tr>
                <th>Strategy</th>
                <th>Symbol</th>
                <th>Entry</th>
                <th>Exit / Open</th>
                <th>Entry $</th>
                <th>Exit / Mark $</th>
                <th>Return</th>
                <th>Days</th>
                <th>Market state</th>
                <th>Source</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>${body}</tbody>
          </table>
        </div>
      </section>
    `;
  }

  function rb38bRenderMarketState(data) {
    const status = data.marketStatus || {};
    const market = data.marketState || {};

    const statusDate = rb38bPick(status, ["status_date", "latest_date", "date", "as_of"], rb38bPick(market, ["date", "status_date", "as_of"]));
    const marketState = rb38bPick(status, ["market_state", "state", "regime", "e1r_market_state"], rb38bPick(market, ["market_state", "state", "regime"]));
    const coreActive = rb38bPick(status, ["core_active", "is_core_active"]);
    const sidecarActive = rb38bPick(status, ["sidecar_active", "is_sidecar_active"]);
    const sidecarCount = rb38bPick(status, ["sidecar_selected_count", "selected_count"], 0);
    const mode = rb38bPick(status, ["tracking_mode", "execution_mode", "mode"], "PAPER_TRACKING_NO_REAL_EXECUTION");

    const cards = [
      ["Status date", statusDate || "N/A"],
      ["Market state", marketState || "N/A"],
      ["Core active", coreActive ?? "N/A"],
      ["Sidecar active", sidecarActive ?? "N/A"],
      ["Sidecar selected", sidecarCount ?? "N/A"],
      ["Mode", mode]
    ].map(([label, value]) => `
      <div class="rb38b-metric">
        <span>${rb38bEscape(label)}</span>
        <strong>${rb38bEscape(value)}</strong>
      </div>
    `).join("");

    return `
      <section class="rb38b-card rb38b-market-card">
        <div class="rb38b-card-head">
          <div>
            <h2>Market State</h2>
            <p>Only current market/regime context is retained below Trade Log.</p>
          </div>
          <span class="rb38b-badge">paper tracking</span>
        </div>
        <div class="rb38b-metric-grid">${cards}</div>
      </section>
    `;
  }

  function rb38bLastDate(rows) {
    return rows && rows.length ? rows[rows.length - 1].date : null;
  }

  async function rb38bLoadAll() {
    const entries = await Promise.all(Object.entries(RB38B_PATHS).map(async ([key, path]) => {
      const optional = key === "marketRegimeOptional";
      return [key, await rb38bFetchJson(path, optional)];
    }));

    const loaded = Object.fromEntries(entries);
    const payload = {};
    for (const [key, result] of Object.entries(loaded)) payload[key] = result.ok ? result.data : null;

    const e1Summary = rb38bFindSummary(payload.backtest, RB38B_VARIANTS.e1);
    const e1rSummary = rb38bFindSummary(payload.e1rBacktestSummary, RB38B_VARIANTS.e1r);

    const e1HistRows = rb38bFindEquitySeries(e1Summary);
    const e1ForwardRows = rb38bFindEquitySeries(payload.e1OosEquity);
    const e1rHistRows = rb38bFindEquitySeries(payload.e1rBacktestEquity);
    const e1rForwardRows = rb38bFindEquitySeries(payload.e1rOosEquity);

    const spxRows = rb38bFindEquitySeries(payload.backtest, {
      equityKeys: ["spx_equity", "benchmark_equity", "spx", "SPX"]
    });

    const e1TradeRows = rb38bFindTradeRows(payload.tradeLog);
    const e1ForwardTradeRows = rb38bFindTradeRows(payload.e1OosTrades).concat(rb38bFindTradeRows(payload.e1OosOrders));
    const e1rForwardTradeRows = rb38bFindTradeRows(payload.e1rOosOrders).concat(rb38bFindTradeRows(payload.e1rOosPositions));

    return {
      loaded,
      e1Summary,
      e1rSummary,
      e1HistRows,
      e1ForwardRows,
      e1rHistRows,
      e1rForwardRows,
      spxRows,
      e1TradeRows,
      e1ForwardTradeRows,
      e1rForwardTradeRows,
      marketStatus: rb38bLatest(payload.e1rStatus),
      marketState: rb38bLatest(payload.marketState || payload.marketRegimeOptional || payload.e1rOosSummary),
      e1LastDate: rb38bLastDate(e1ForwardRows) || rb38bLastDate(e1HistRows),
      e1rLastDate: rb38bLastDate(e1rForwardRows) || rb38bLastDate(e1rHistRows),
      spxLastDate: rb38bLastDate(spxRows)
    };
  }

  async function rb38bRender() {
    const root = rb38bEnsureRoot();

    try {
      const data = await rb38bLoadAll();

      root.innerHTML = `
        <div class="rb38b-title">
          <div>
            <h1>Research & Backtest</h1>
            <p>E1 and E1R v0.2 are shown together. Historical results are frozen research artifacts; forward paper tracking updates from live OOS exports.</p>
          </div>
          <div class="rb38b-policy-pill">Strategy logic frozen</div>
        </div>
        ${rb38bRenderCurve(data)}
        ${rb38bRenderSummary(data)}
        ${rb38bRenderTradeLog(data)}
        ${rb38bRenderMarketState(data)}
      `;

      rb38bMountChart(data);
      rb38bHideLegacyBlocks(root);

      window.__RB38B_LAST_RENDER__ = {
        status: "PASS",
        e1HistRows: data.e1HistRows.length,
        e1ForwardRows: data.e1ForwardRows.length,
        e1rHistRows: data.e1rHistRows.length,
        e1rForwardRows: data.e1rForwardRows.length,
        spxRows: data.spxRows.length,
        e1TradeRows: data.e1TradeRows.length,
        e1ForwardTradeRows: data.e1ForwardTradeRows.length,
        e1rForwardTradeRows: data.e1rForwardTradeRows.length,
        optionalMarketRegimeLoaded: Boolean(data.loaded.marketRegimeOptional && data.loaded.marketRegimeOptional.ok)
      };
    } catch (error) {
      root.innerHTML = `
        <section class="rb38b-card rb38b-error">
          <h2>Research & Backtest refactor failed to render</h2>
          <pre>${rb38bEscape(error && error.stack ? error.stack : error)}</pre>
        </section>
      `;
      window.__RB38B_LAST_RENDER__ = { status: "FAIL", error: String(error) };
    }
  }

  function rb38bInit() {
    if (window.__RB38B_INITIALIZED__) return;
    window.__RB38B_INITIALIZED__ = true;

    rb38bRender();
    setTimeout(rb38bRender, 1200);
    setTimeout(() => rb38bHideLegacyBlocks(document.getElementById("rb38b-research-backtest-refactor")), 2500);

    document.addEventListener("click", () => {
      setTimeout(() => {
        rb38bRender();
        rb38bHideLegacyBlocks(document.getElementById("rb38b-research-backtest-refactor"));
      }, 400);
    });

    const observer = new MutationObserver(() => {
      const root = document.getElementById("rb38b-research-backtest-refactor");
      if (root) rb38bHideLegacyBlocks(root);
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  window.RB38BResearchBacktest = {
    init: rb38bInit,
    render: rb38bRender,
    paths: RB38B_PATHS
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", rb38bInit);
  } else {
    rb38bInit();
  }
})();
/* === END E1R_V0_2_STAGE3_8B_RESEARCH_BACKTEST_REFACTOR === */
