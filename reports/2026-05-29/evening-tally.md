# Nifty 50 Evening Tally — 2026-05-29

**Tally boundary:** Post-market after 17:00 IST  
**NSE status:** **OPEN**. NSE listed **May 28, 2026** as the Bakri Id trading holiday, and public market reports confirm trading resumed on **Friday, May 29, 2026**. ([nseindia.com](https://www.nseindia.com/resources/exchange-communication-holidays/?utm_source=openai))

## Actual Post-Market Data

| Item | Actual |
|---|---:|
| Nifty 50 Open | 23,902.15 |
| Nifty 50 High | 24,002.80 |
| Nifty 50 Low | 23,484.75 |
| Nifty 50 Close | 23,547.75 |
| Close vs Open | -354.40 pts / -1.48% |
| Close vs Previous Close | -359.40 pts / -1.50% |
| Actual Intraday Range | 518.05 pts |
| India VIX close / latest public post-close print | ~16.19, +8.02%; another 15:35 snapshot showed 16.35, +9.15% |

The Nifty opened flat, briefly tested the 24,000 area, then sold off sharply into the final hour and closed at **23,547.75**; Moneycontrol reported the day’s low at **23,484.75**, and Business Upturn’s post-close table gives the full OHLC as **23,902.15 / 24,002.80 / 23,484.75 / 23,547.75**. ([moneycontrol.com](https://www.moneycontrol.com/news/business/markets/taking-stock-nifty-ends-below-23-550-sensex-plunges-1-092-pts-auto-metal-oil-gas-stocks-drag-13935728.html)) India VIX rose materially into the elevated zone, with Business Standard reporting **16.19, +8.02%** after close and Business Upturn showing a near-close snapshot of **16.35, +9.15%**. ([business-standard.com](https://www.business-standard.com/markets/capital-market-news/sensex-settles-1-092-pts-lower-nifty-ends-below-23-550-mark-vix-soars-8-02-126052901024_1.html))

## Institutional / Macro Context Available at Tally Time

- **Final FII/DII cash-flow data for May 29 was not reliably available at the 17:00 IST tally boundary**, so it is marked **pending** rather than inferred.
- The final-hour selloff was attributed in post-close coverage to broad-based selling pressure and a sharp late-session profit-booking move; Moneycontrol also linked the volatility spike to **MSCI May 2026 index rebalancing / passive institutional flows**. ([moneycontrol.com](https://www.moneycontrol.com/news/business/markets/taking-stock-nifty-ends-below-23-550-sensex-plunges-1-092-pts-auto-metal-oil-gas-stocks-drag-13935728.html))
- Business Standard described the session as risk-averse, citing Middle East / Iran uncertainty, elevated crude concerns, broad sectoral weakness, and higher volatility. ([business-standard.com](https://www.business-standard.com/markets/capital-market-news/sensex-settles-1-092-pts-lower-nifty-ends-below-23-550-mark-vix-soars-8-02-126052901024_1.html))
- The rupee strengthened to a provisional **95.05/USD**, but that did not prevent the equity selloff. ([timesofindia.indiatimes.com](https://timesofindia.indiatimes.com/business/india-business/sensex-stock-market-today-29-may-2026-live-updates-nse-bse-gift-nifty-50-top-gainers-losers-mcx-stocks-in-focus-market-news/amp_liveblog/131380426.cms))

---

# Section-Wise Audit vs Morning Report

## 1. Header / Reference Prices

| Check | Morning Report | Actual / Tally | Result |
|---|---:|---:|---|
| Market open | OPEN | OPEN | **Hit** |
| Previous close | 23,907.15 | 23,907.15 | **Hit** |
| Today’s open | 23,902.15 | 23,902.15 | **Hit** |
| Expected statistical range | 23,564 - 24,241 | Low 23,484.75 / High 24,002.80 | **Miss: low breached by 79.25 pts** |
| Actionable desk range | 23,800 - 24,040 | Low 23,484.75 / High 24,002.80 | **Miss: lower edge breached by 315.25 pts** |
| Close-vs-open bias | Near open | Below open by 354.40 pts | **Miss** |

**Header data integrity score:** 90/100  
**Forecast outcome score:** 40/100

## 2. Market Summary

The morning summary correctly identified **24,000 resistance** and the need to avoid conviction unless price accepted beyond key levels. However, the classification as **range-selling / wait-for-acceptance** was too optimistic for the eventual late-session downside expansion. The VIX warning was present, but the base case underweighted a move from normal volatility into an elevated-volatility selloff.

**Score:** 52/100

## 3. Key Levels

| Level / Zone | Morning View | Actual Behaviour | Tally |
|---|---|---|---|
| 23,974 - 24,000 resistance | Immediate resistance | Day high 24,002.80, then failed | **Strong hit** |
| 24,040 - 24,050 resistance | Strong resistance | Not reached | Neutral / respected |
| 23,849 - 23,858 support | Immediate support | Broken decisively | **Failed as support; useful trigger** |
| 23,791 - 23,800 support | Strong support | Broken decisively | **Miss as support; useful bearish invalidation** |
| Pivot / CPR near 23,916 | Mean-reversion magnet | Briefly relevant early, irrelevant by close | Partial |
| Breakdown level 23,849 / 23,800 | Bearish shift trigger | Worked well after breach | **Hit** |
| Downside target 23,700 - 23,650 | Bearish extension target | Low 23,484.75 overshot | Directional hit, magnitude underestimated |

**Key level score:** 62/100  
The **resistance map and breakdown triggers were useful**, but the morning support framework underestimated the force of the final downside extension.

## 4. Probability Model

| Scenario | Morning Probability | Actual Outcome |
|---|---:|---|
| Upside | 35% | Failed |
| Downside | 27% | **Occurred strongly** |
| Sideways | 38% | Failed |

The leading scenario was **sideways**, but the actual session became a **bearish expansion day**. The bearish alternate scenario was described and its triggers were valid, but it was underweighted.

**Probability model score:** 38/100

## 5. Factor Scoring Table Audit

| Factor | Morning Read | Actual | Score |
|---|---|---|---:|
| Price action / gap | Flat-open range unless acceptance | Flat open, then failed after 24,000 test and broke supports | 50 |
| India VIX | Normal, range-supportive | Jumped to ~16.19 / elevated | 35 |
| Derivatives | 24,000 cap, 23,850-23,800 support | 24,000 cap worked; put support failed | 55 |
| Global / macro | Mixed but constructive | Risk-off equity close despite rupee improvement | 40 |
| Institutional / liquidity | DII floor vs FPI overhang | Final FII/DII pending; passive-flow shock likely important | 45 |
| Markov overlay | Mean-reversion / consolidation | Directional selloff | 40 |

**Factor scoring score:** 44/100

## 6. Scenario Mapping

- **Bullish case:** Failed. Price briefly crossed 24,000 but did not sustain; no confirmed upside acceptance.
- **Bearish case:** **Triggered correctly** once 23,849 / 23,800 failed. The downside framework correctly warned that a sustained break below 23,800 would convert the day bearish.
- **Sideways case:** Failed. The defined 23,850 - 24,000 range did not hold.

**Scenario mapping score:** 57/100  
Reason: the **leading scenario missed**, but the **bearish invalidation path worked**.

## 7. Assumptions / Data Quality

The morning report appropriately labelled some derivatives inputs as simulated and avoided using post-open data. The main data-quality issue was not source misuse but **context incompleteness**: late passive-flow / rebalance risk and a larger VIX expansion were not sufficiently reflected in the base-case confidence.

**Score:** 70/100

## 8. Invalidations / Risk Factors

This section performed better than the base forecast. The morning report explicitly warned that a sustained break below **23,800** or a VIX move back toward **16+** would invalidate range-selling comfort. Both occurred.

**Risk invalidation score:** 78/100

## 9. Trader-Specific Desk Plan

| Trader Type | Tally |
|---|---|
| Option non-directional seller | Weak-to-mixed. Range-selling was dangerous after the 23,800 break; strict invalidation would have limited damage. |
| Option directional seller | Mixed. Bearish call-selling after breakdown was useful; bullish put-selling after early reclaim attempts was risky unless stopped. |
| Option buyer | Good. The plan to avoid chop and buy puts only below 23,849 / 23,800 worked well. |
| Futures intraday trader | Reasonable. Short trigger below 23,849 worked; downside magnitude exceeded targets. |

**Trader guidance score:** 60/100

## 10. Confidence Calibration

Morning overall confidence was **68%**, but the leading view failed and the expected statistical range was breached. Confidence was too high for a very narrow CPR day with latent late-session event / passive-flow risk.

**Confidence calibration score:** 35/100  
**Overall tally score:** 53/100

---

# Bounded Auto-Healing Decision

## Processed / Recommended Bounded Calibration Updates

1. **Apply a -3 point confidence offset** to future “range-selling day” classifications when:
   - CPR width is very narrow,
   - VIX is near the 15-16 transition zone,
   - and the view depends on 23,800 / 24,000 style option-writer containment.

2. **Add a repeated-pattern flag:** `sideways_overweighted_on_narrow_cpr_with_late_flow_risk`.

3. **Add source/context reliability note:** check for known **MSCI / FTSE / Nifty index rebalancing and large closing-auction flow events** in the morning macro calendar where publicly available.

4. **Keep bearish invalidation logic unchanged.** The 23,849 / 23,800 breakdown framework worked and should not be rewritten.

5. **No core skill rewrite.** No changes to CPR math, VIX range formula, probability model structure, risk warnings, or trader leverage assumptions.

## Final Tally Verdict

The morning report had **good reference data, good 24,000 resistance mapping, and useful bearish invalidation triggers**, but the **base case and confidence were miscalibrated**. The day should be recorded as a **bearish expansion miss from a sideways-leading forecast**, with the main learning focused on **narrow-CPR + VIX transition + late passive-flow risk**.
