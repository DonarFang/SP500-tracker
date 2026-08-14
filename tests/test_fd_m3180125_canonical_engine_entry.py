from dataclasses import replace
from datetime import date, timedelta
import unittest

from e1r_engine.capped_atr_stop import ENTRY_METADATA_KEY, VARIANT_ID
from e1r_engine.contracts import DailyBar, MarketSnapshot, RegimeRecord
from e1r_engine.core import E1RCoreEngine
from e1r_engine.state import AccountState


def series(symbol: str, slope: float) -> dict[str, DailyBar]:
    del symbol
    start = date(2025, 1, 1)
    output = {}
    for index in range(500):
        day = (start + timedelta(days=index)).isoformat()
        close = 100.0 * ((1.0 + slope) ** index)
        output[day] = DailyBar(
            date=day,
            open=close - 0.2,
            high=close + 1.0,
            low=close - 1.0,
            close=close,
            volume=1000.0,
        )
    return output


class CanonicalEngineEntryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.history = {
            "SPX": series("SPX", 0.0020),
            "NDX": series("NDX", 0.0022),
            "SOX": series("SOX", 0.0025),
            "AAPL": series("AAPL", 0.0100),
        }
        for index in range(10):
            symbol = f"S{index}"
            self.history[symbol] = series(symbol, 0.0005 + index * 0.0002)
        self.day = sorted(self.history["SPX"])[-1]
        self.snapshot = MarketSnapshot(
            date=self.day,
            universe=["AAPL"] + [f"S{index}" for index in range(10)],
            prices_by_symbol={
                symbol: rows[self.day]
                for symbol, rows in self.history.items()
                if symbol not in {"SPX", "NDX", "SOX"}
            },
            indices={
                item: self.history[item][self.day]
                for item in ("SPX", "NDX", "SOX")
            },
            regime=None,
            history_by_symbol=self.history,
        )

    def test_one_step_owns_full_decision(self) -> None:
        account = replace(
            AccountState.empty(self.day),
            metadata={"strategy_variant": VARIANT_ID},
        )
        result = E1RCoreEngine().step(self.snapshot, account)
        self.assertEqual(result.decision_trace.market_regime, "UPTREND")
        self.assertTrue(result.decision_trace.inputs["canonical_engine_entry"])
        self.assertEqual(
            [(row["rank"], row["symbol"]) for row in result.decision_trace.metadata["reference_top3"]],
            [(1, "AAPL"), (2, "S9"), (3, "S8")],
        )
        buys = [row for row in result.order_intents if row.intent_type == "BUY"]
        self.assertEqual([row.symbol for row in buys], ["AAPL"])
        self.assertIn(ENTRY_METADATA_KEY, buys[0].metadata)

    def test_external_regime_is_rejected(self) -> None:
        snapshot = replace(
            self.snapshot,
            regime=RegimeRecord(date=self.day, spx_regime="UPTREND"),
        )
        with self.assertRaisesRegex(ValueError, "external Regime"):
            E1RCoreEngine().step(snapshot, AccountState.empty(self.day))


if __name__ == "__main__":
    unittest.main()
