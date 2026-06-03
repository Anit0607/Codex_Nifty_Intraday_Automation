# Nifty 50 Evening Tally — 2026-06-03

**Automation:** Nifty 5 PM post-market tally  
**Boundary:** Post-market after 17:00 IST  
**Market-open check:** `market_open=true`. NSE trading was confirmed by post-market Nifty 50 prints for 03 Jun 2026: Open **23,415.95**, High **23,459.65**, Low **23,151.50**, Close **23,405.60**. ([dhan.co](https://dhan.co/indices/nifty-50-share-price/))

## 1. Actual Post-Market Data

| Item | Actual |
|---|---:|
| Nifty 50 previous close | 23,483.55 |
| Nifty 50 open | 23,415.95 |
| Nifty 50 high | 23,459.65 |
| Nifty 50 low | 23,151.50 |
| Nifty 50 close | 23,405.60 |
| Actual day range | 308.15 pts |
| Close vs open | **Below open** by 10.35 pts |
| Close vs previous close | -77.95 pts / -0.33% |

Dhan’s post-market page showed the exact Nifty OHLC, while Business Standard independently reported the Nifty closing at **23,405.60**, down **77.95 points**, and noted the intraday low near **23,151.50**. ([dhan.co](https://dhan.co/indices/nifty-50-share-price/))

**India VIX:** Closed at **16.28**, up **5.99%**, with day high **16.98** and low **14.85**. Business Standard also reported India VIX up about **6%** to **16.28**. ([dhan.co](https://dhan.co/indices/india-vix-share-price/))

**Final institutional context:** FIIs were net sellers of **₹5,616.56 crore** and DIIs were net buyers of **₹5,740.89 crore** on 03 Jun 2026 in cash provisional data. ([moneycontrol.com](https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/))

**Macro/context:** Brent crude was reported near **$98.35/bbl**, USD/INR around **95.6775**, India 10-year yield around **7.025**, and HSBC India Services PMI was revised higher to **59.8** for May 2026. ([business-standard.com](https://www.business-standard.com/amp/markets/capital-market-news/benchmarks-pare-steep-losses-sensex-slides-304-points-nifty-ends-below-23-450-126060300936_1.html?isa=yes))

## 2. Header Forecast Audit

| Forecast item | Morning forecast | Actual | Verdict |
|---|---:|---:|---|
| Previous close | 23,483.55 | 23,483.55 | Hit |
| Today’s open | 23,415.95 | 23,415.95 | Hit |
| VIX risk envelope | 23,076 - 23,756 | 23,151.50 - 23,459.65 | Contained |
| Expected day range | 23,190 - 23,540 | 23,151.50 - 23,459.65 | Strict low miss, but within ±50 tolerance |
| Expected high zone | 23,465 - 23,540 | 23,459.65 | Miss by 5.35 pts only; precision hit |
| Expected low zone | 23,190 - 23,285 | 23,151.50 | Miss by 38.50 pts only; precision hit |
| Close vs open | Close below open | Close below open | Hit |

**Direction call:** Correct. The close was below the open, but only by **10.35 points**, so this is a binary hit with a thin margin.  
**Range precision:** Passed. Both high-zone and low-zone misses were within the ±50-point tolerance.  
**Range containment:** Strict primary range containment failed because the actual low was below **23,190**, but the miss was tolerance-compliant.

## 3. Section-Wise Audit

### 1. Market Summary

The morning view called for a fragile range-to-downside session, with risk of breakdown below **23,380**. Actual price broke below **23,380**, sold off toward **23,151.50**, then recovered sharply into the close. This was directionally aligned with the fragile/downside warning, though the late recovery made the close-vs-open hit narrow.  
**Score:** 82/100

### 2. Trader Key Levels

| Morning level | Actual behaviour | Verdict |
|---|---|---|
| Long above 23,460 | Actual high 23,459.65, effectively not triggered | Good filter |
| Short below 23,380 | Triggered clearly | Hit |
| Short targets 23,310 / 23,240 | Both achieved | Hit |
| Downside tail 23,160 - 23,095 | Actual low 23,151.50 entered tail zone | Hit |
| Chop zone 23,390 - 23,455 | Close returned into/near this zone | Useful late-session context |

The short trigger and downside targets worked well. The long trigger avoided a false long by less than one point.  
**Score:** 88/100

### 3. Probability Model

Morning probabilities: Upside **28%**, Downside **38%**, Sideways **34%**.  
Actual session: downside trigger and tail expansion occurred, but the close recovered to only slightly below open. The leading bearish case was the best-fitting scenario, but the final close behaved more like a bearish-to-sideways recovery day.  
**Score:** 76/100

### 4. Factor Scoring Table

The report correctly weighted FII selling, oil/rupee pressure, and VIX expansion risk as fragility drivers. Actual data confirmed continued FII selling, DII absorption, Brent near $98, USD/INR pressure, and VIX rising to 16.28. ([moneycontrol.com](https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/))  
**Score:** 80/100

### 5. Scenario Mapping

- **Bearish case:** Triggered below **23,380**, achieved **23,310**, **23,240**, and touched downside tail.
- **Bullish case:** Not triggered; actual high stayed just below long trigger.
- **Sideways case:** Not the primary intraday structure, but late recovery into the chop/mean-reversion area made the close less bearish than the intraday low.

**Score:** 86/100

### 6. Assumptions Made

The morning report correctly labelled live option-chain zones as simulated and preserved uncertainty around derivatives. Macro assumptions around RBI event risk, crude, rupee, and FII pressure were directionally useful.  
**Score:** 78/100

### 7. Invalidations / Risk Factors

The VIX spike warning was useful: VIX rose to **16.28**, near but below the stated **16.5 - 17** risk trigger. The geopolitical/crude risk framing was also validated by the reported Brent and West Asia context. ([business-standard.com](https://www.business-standard.com/amp/markets/capital-market-news/benchmarks-pare-steep-losses-sensex-slides-304-points-nifty-ends-below-23-450-126060300936_1.html?isa=yes))  
**Score:** 82/100

### 8. Trader-Specific Desk Plan

| Trader type | Audit |
|---|---|
| Option non-directional seller | Caution was appropriate; aggressive early selling would have been risky during the breakdown. Better only after late recovery. |
| Option directional seller | Failed-rise CE selling was not the main opportunity; downside trigger logic was more useful. |
| Option buyer | Put-buying below 23,380 worked well; both listed targets were achieved. |
| Futures intraday trader | Short below 23,380 with targets 23,310 / 23,240 worked well; tail management mattered. |

**Score:** 82/100

### 9. Trading Desk Interpretation

Morning classification was **Avoid / wait-and-watch day**. That was appropriate: the session had a sharp downside break, VIX expansion, tail touch, and then a large recovery. Trigger-based traders had opportunity; blind trend chasing near lows was risky.  
**Score:** 84/100

## 4. Precision and Error Metrics

| Metric | Value |
|---|---:|
| Expected high zone | 23,465 - 23,540 |
| Actual high | 23,459.65 |
| High-zone error | 5.35 pts |
| Expected low zone | 23,190 - 23,285 |
| Actual low | 23,151.50 |
| Low-zone error | 38.50 pts |
| Range precision hit | true |
| VIX envelope contained day | true |
| Strict expected range contained day | false |
| Expected range tolerance hit | true |

No `expected_high_miss`, `expected_low_miss`, or `range_precision_miss` tag is applied because both edge errors were within the ±50-point tolerance.

## 5. Bounded Auto-Healing Result

Processed only bounded calibration updates:

1. Update rolling direction-hit statistic: **hit**.
2. Update VIX-envelope containment statistic: **hit**.
3. Update expected high/low range-precision statistic: **hit**.
4. Add source reliability note: post-market Nifty OHLC, India VIX, and FII/DII data were available and internally consistent across public sources.
5. Apply a small **+1 confidence offset** to key-level/range-precision calibration only; do **not** rewrite core CPR, probability, derivatives, or trader-plan logic.

**No core skill logic rewrite recommended.**
