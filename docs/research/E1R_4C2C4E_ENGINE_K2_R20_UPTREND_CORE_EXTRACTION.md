# K2-R20 Uptrend Core Extraction

## Decision

`PASS_UPTREND_CORE_EXTRACTION`

## Unit validation

- Tests run: 7
- Tests passed: 7
- Result: PASS

## Extracted pure logic

- Candidate filtering
- Candidate ranking
- Selected BUY finalization
- BUY order payload construction

## Preserved legacy orchestration

- Daily timeline loop
- Existing `continue` behavior
- Skip-reason mutation
- `buy_orders` append
- Pending-order handoff
- T+1 price resolution
- Position sizing
- Cash and holding mutation
- REDUCE and EXIT execution

## Golden-window equivalence

- Window: 2021-06-01 through 2021-12-31
- R19 result hash: `213a9394f7163f2c8a486f935d7de3401b6b0fc3e72d9c0ff244b07bdcee35c3`
- R20 result hash: `213a9394f7163f2c8a486f935d7de3401b6b0fc3e72d9c0ff244b07bdcee35c3`
- Result hash match: `True`
- TP01–TP04 count match: `True`
- Actual counts: `{"TP01_PRE_RANK_CANDIDATES": 150, "TP02_POST_RANK_CANDIDATES": 150, "TP03_SELECTED_BUY_FINALIZED": 10, "TP04_BUY_ORDER_INTENT_CREATED": 10}`
- Total trace records: `832`
- Null trace IDs: `0`

## Next stage

`K2-R21-UPTREND-CORE-CONSUMER-INTEGRATION`
