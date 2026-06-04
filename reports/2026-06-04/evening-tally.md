# Nifty 50 Evening Tally - 2026-06-04

**Run boundary:** Post-market after 17:00 IST  
**Market status:** **OPEN - tally executed.**

## 1. Actual Post-Market Data Used

| Item | Actual |
|---|---:|
| Previous close | 23,405.60 |
| Open | 23,282.45 |
| High | 23,465.30 |
| Low | 23,247.30 |
| Close | 23,416.55 |
| Day range | 218.00 pts |
| Close vs open | **Above open** by 134.10 pts |
| Close vs previous close | +10.95 pts / +0.05% |
| India VIX close | 15.89, down 2.41% |

Sources used in the original tally: Nifty OHLC from NewsArena India, VIX/macro context from Business Standard, and holiday/status checks from NSE.

## 2. Trader Audit Table

| Item | Predicted | Actual | Deviation / Result | Verdict | Auto-heal action |
|---|---:|---:|---:|---|---|
| VIX Risk Envelope | 22,924 - 23,641 | 23,247.30 - 23,465.30 | Contained, but very broad | Risk-only pass | Do not score as precision. Keep as volatility boundary only. |
| Expected Day Range | 23,155 - 23,505 | 23,247.30 - 23,465.30 | High edge error 39.70; low edge error 92.30 | **Precision miss** | Score edge precision separately from containment; add low-edge miss tag. |
| Expected High Zone | 23,420 - 23,505 | 23,465.30 | Inside zone; zone width 85 pts | Directionally right, too wide | Penalize visible high zones above 60 pts unless confidence is lowered. |
| Expected Low Zone | 23,155 - 23,225 | 23,247.30 | 22.30 pts above zone; zone width 70 pts | Tolerance hit, too wide | Penalize wide low zone and keep practical target width near 30-50 pts. |
| Tail Expansion Zones | 23,525 - 23,650 / 23,030 - 23,150 | Not needed | Duplicated high/low risk information | Remove from visible report | Keep tail levels internal for invalidation only. |
| Long Trigger | Above 23,375, SL 23,318, T1 23,445, T2 23,525 | Triggered; T1 hit; T2 not hit | T1 RR 1.23; T2 RR 2.63 | Mixed | Flag target-1 RR below preferred 1.50 threshold. |
| Short Trigger | Below 23,215, SL 23,285, T1 23,155, T2 23,075 | Not triggered | No short trade | Neutral | No penalty for non-triggered short, but record setup quality. |
| Close vs Open Direction | Close above open | Close above open | Correct | **Hit** | Keep binary direction scoring. |

## 3. Corrected Section Scores

| Section | Corrected score | Reason |
|---|---:|---|
| Header/reference prices | 92% | Open and prior references were usable. |
| VIX risk envelope | 60% | It contained the day but was not a tradable precision forecast. |
| Expected Day Range | 52% | Containment passed, but low edge missed the +/-50 target. |
| Expected High/Low Zones | 68% | High was good, low was close, but both zones were too wide. |
| Close vs open direction | 100% | Binary direction was correct. |
| Opening execution map | 62% | Long worked to T1, but T1 RR was weak and T2 failed. |
| Trader-specific guidance | 64% | Useful only after trigger confirmation; non-directional context needed more caution. |
| Overall corrected tally | **64%** | Better than a miss, but not an 86/100 day. |

## 4. Calibration / Auto-Healing Applied

Bounded calibration was updated with the following failure tags:

- `expected_day_range_precision_miss`
- `expected_range_low_edge_miss`
- `expected_high_zone_too_wide`
- `expected_low_zone_too_wide`
- `target1_rr_below_preferred`

The morning agent will now receive the calibration file before generating the next report, so these misses influence confidence and range construction. This is bounded auto-healing only: it updates scoring, calibration offsets, report structure, and quality gates; it does not rewrite CPR math, remove risk controls, or chase yesterday's exact result.

## 5. Desk Conclusion

June 4 should be recorded as a **mixed-quality report**: direction correct, high zone useful, low zone acceptable but imprecise, broad VIX envelope not tradable, and long execution only partially attractive because target-1 reward was too low.
