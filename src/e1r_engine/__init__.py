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

__all__ = [
    "CanonicalRegimeGenerator",
    "CanonicalRegimeTimeline",
    "RegimeDecision",
    "contracts",
]
