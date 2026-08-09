"""
Standalone E1R Engine package.

Backtest, paper and future live execution must share one Core Engine.
CanonicalRegimeGenerator is the single Engine Regime-generation module.
"""

from e1r_engine.canonical_regime import (
    CanonicalRegimeGenerator,
    CanonicalRegimeTimeline,
    RegimeDecision,
)
from e1r_engine.capped_atr_stop import (
    DISPLAY_NAME as CAPPED_ATR_DISPLAY_NAME,
    VARIANT_ID as CAPPED_ATR_VARIANT_ID,
)

__all__ = [
    "CanonicalRegimeGenerator",
    "CanonicalRegimeTimeline",
    "RegimeDecision",
    "CAPPED_ATR_VARIANT_ID",
    "CAPPED_ATR_DISPLAY_NAME",
    "contracts",
]
