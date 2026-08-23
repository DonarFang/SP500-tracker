# FD-M3180125 Parity Repair Contract v1.0

Status: `PARITY-STEP-2 SHADOW ONLY`

This implementation is limited to the four user-approved corrections:

1. Build a versioned Yahoo-adjusted Live price store. It is not activated by
   Parity-step-2; `FD_M3180125_LIVE_PRICE_MODE=ADJUSTED_ACCEPTED` is required.
2. Exclude `QQQ`, `SOXX`, and `VIXY` from the Live stock catalogue and all
   risk-increasing eligibility paths. Existing holdings, files, and snapshots
   are not rewritten.
3. Apply the shared `0.5 unit` minimum REDUCE gate to Forward and Live Engine
   decisions. EXIT remains available.
4. Persist optional recommendation/signal/origin linkage on confirmed Live
   transaction events and replay Cycle size from confirmed transactions only.

Frozen invariants:

- no 5Y execution or rewrite;
- no Forward or Live history rewrite;
- no NTAP/HPE ledger rewrite;
- no broker connection or automatic execution;
- no change to Regime, Market State/Gate, ranking, Top3, ATR parameters,
  execution priority, max-three positions, Forward fractional execution, or
  Live manual whole-share execution;
- legacy transaction fingerprints are unchanged because absent optional fields
  are omitted from their canonical payloads;
- any unsupported state or out-of-bound Live REDUCE must HOLD for manual
  reconciliation.
