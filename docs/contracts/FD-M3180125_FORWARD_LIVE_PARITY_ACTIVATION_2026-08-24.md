# FD-M3180125 Forward/Live Parity Activation

Authority: `3b910bba2ab7bc4b71817a98d860c045d997cf57`

User authorization date: `2026-08-24`.

This activation makes Forward and Personal Live use the same accepted adjusted
price convention and the frozen canonical 5Y REDUCE contract. The minimum
remaining position size is `0.5 unit`; another REDUCE at that minimum is
suppressed while a valid EXIT remains available.

Forward is already replayed and active on its independent adjusted library.
Personal Live rebuilds its independent adjusted library before each ACTIVE
daily run and fails closed unless accepted evidence is CURRENT, auto-adjusted,
and production-activated.

This activation does not rewrite prior Live transactions, ledger journals,
cash-control records, account history, Forward history, or 5Y artifacts. It
does not connect a broker or enable automatic execution. `LEGACY_HOLD` remains
an explicit rollback mode but is no longer the Personal Live default.
