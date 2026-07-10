"""
Standalone E1R Engine package.

Architecture rule:
Backtest, forward test / paper tracking, and future live trading must call the
same E1R Core Engine. Mode-specific code may adapt data, execution,
persistence, and reporting only; it must not fork trading logic.
"""

__all__ = [
    "contracts",
]
