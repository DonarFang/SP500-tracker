# 2026-08-24 Forward Replay after Parity REDUCE Update

## Status

`PASS_FORWARD_REPLAY_BUSINESS_ACCEPTANCE`

## Authority and scope

- Source authority: `9bbeee0a2543afccbb87b2380e73b46f39015114`
- Seed boundary: 2026-06-16 normal EOD
- Forward interval: 2026-06-17 through 2026-08-21 (46 trading days)
- Updated artifact: official Forward runtime, including the Dashboard-read equity curve
- Dashboard code unchanged; it reads the official Forward equity curve directly
- 5Y, seed, Live, and Forward price data unchanged

## Business effect

- Old REDUCE count: 37
- New effective REDUCE count: 5
- REDUCE signals held at the 0.5-unit minimum: 32
- Old final equity: 288908.33
- Replayed final equity: 283083.53
- Replayed final cash: 93598.47
- Final positions: BAX, ETSY, MPC

## Dashboard continuity

- 5Y boundary: 2026-06-16
- First Forward date: 2026-06-17
- Latest Forward date: 2026-08-21
- No SIM_END replay and no curve reset
