# E1-R Candidate Forward Return Diagnostic

Status: `DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE`
Raw candidates: 5564
Enriched candidates: 5564
Dedup candidates (5 trading-day gap): 2469

## Dedup Forward Return Summary

| Entry Type | Count | 5D Avg | 5D Excess | 10D Avg | 10D Excess | 20D Avg | 20D Excess | 30D Avg | 30D Excess |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E1R_UPTREND_CONFIRMED | 1060 | 0.987% | 0.608% | 2.062% | 1.335% | 3.413% | 2.219% | 4.225% | 2.508% |
| E1R_UPTREND_EMERGING | 1409 | 0.709% | 0.488% | 1.088% | 0.573% | 2.201% | 1.142% | 2.566% | 0.901% |
| ALL | 2469 | 0.828% | 0.539% | 1.505% | 0.900% | 2.719% | 1.603% | 3.274% | 1.588% |

## Lead Time vs First E1 Entry

Positive lead days means the E1-R candidate appeared before or on the first E1 trade entry date for the same symbol.

| Entry Type | N | Avg Trading Days | Median Trading Days | % Before/Same E1 Entry |
|---|---:|---:|---:|---:|
| E1R_UPTREND_CONFIRMED | 300 | 21.86 | 3.0 | 59.0% |
| E1R_UPTREND_EMERGING | 213 | 15.37 | 17 | 62.0% |
| ALL | 513 | 19.17 | 5 | 60.2% |

Interpretation: this report validates candidate alpha only. It does not authorize E1-R execution logic.