# Nifty 50 Evening Tally — 2026-06-01

**Run boundary:** post-market after 17:00 IST  
**Market-open verification:** **OPEN**. June 1, 2026 was not shown as an NSE trading holiday in the 2026 holiday references, and NSE’s own market page showed NIFTY 50 at **23,382.60** at **01-Jun-2026 15:30**, confirming a traded session. ([nseindia.com](https://www.nseindia.com/resources/exchange-communication-holidays/?utm_source=openai))

## Actual Post-Market Data

| Item | Morning report | Actual / final | Tally |
|---|---:|---:|---|
| Previous close | 23,547.75 | 23,547.75 | Hit |
| Open | 23,654.50 | 23,654.50 | Hit |
| High | Not forecast as point value | 23,733.70 | Inside expected range |
| Low | Not forecast as point value | 23,357.95 | Inside expected range; broke desk range |
| Close | Direction: near open / conditional range | 23,382.60 | Miss; closed below open |
| Actual day range | — | 375.75 points | Moderate-wide |
| India VIX | 16.19 reference | about 16.49–16.54 close/latest | VIX stayed elevated and rose modestly |

Nifty opened at **23,654.50**, made **23,733.70 / 23,357.95**, and closed at **23,382.60**, down **165.15 points / 0.70%** from the previous close and **271.90 points / 1.15%** below the open. India VIX was reported around **16.49–16.54** after the close; I use **16.54** as the tally reference because both Upstox and Business Standard reported that final level, while Business Upturn’s table showed **16.49**. ([etnownews.com](https://www.etnownews.com/markets/stock-market-closing-on-monday-june-1-sensex-down-508-points-nifty-below-23400-key-factors-behind-the-surge-closing-bell-article-154441214/amp?utm_source=openai))

## Section-wise Audit

| Section | Score | Audit |
|---|---:|---|
| Header reference prices | 96/100 | Previous close and open were accurate. |
| Market summary | 68/100 | Gap-up, wide CPR, elevated VIX, and fragile setup were correct; however, the leading “range / mean-reversion first” framing understated the eventual downside break. |
| Key levels | 86/100 | Strong. The day rejected below CPR upper area, broke immediate support and previous low, then bottomed almost exactly near **S1 23,354.07**; actual low was **23,357.95**. |
| Expected range | 82/100 | Expected range **23,293–24,016** contained the full actual range, but it was very wide versus the actual **375.75-point** move. |
| Actionable desk range | 52/100 | Upside boundary held, but downside failed: actual low **23,357.95** was below the **23,480** lower desk boundary. |
| Close vs open direction | 25/100 | Miss. Morning expected **near open / conditional range**; actual close was clearly **below open**. |
| Probability model | 45/100 | Leading scenario was sideways at 40%, but the day resolved bearish. Bearish probability was only 29%, though bearish triggers were clearly defined. |
| Factor scoring | 68/100 | FII pressure, elevated VIX, and fragile macro risk were useful. “Supportive global cues” was too soft versus the actual weak-cue/geopolitical pressure narrative reported after close. ([etnownews.com](https://www.etnownews.com/markets/stock-market-closing-on-monday-june-1-sensex-down-508-points-nifty-below-23400-key-factors-behind-the-surge-closing-bell-article-154441214/amp)) |
| Scenario mapping | 72/100 | Sideways leading case failed, but bearish trigger logic worked well: break below **23,613 → 23,547/23,485** led toward **S1 23,354**, nearly matching the day low. |
| Trader-specific guidance | 71/100 | Option buyers and futures traders had useful breakdown triggers; non-directional/range sellers needed strict adherence to the “avoid fast breaks” guardrail. |
| Risk invalidations | 86/100 | Excellent: the report explicitly warned that sustained break below **23,485** would invalidate range/buy-dip behaviour. |

## Key Level Outcome

- **Immediate resistance 23,744–23,872:** not accepted; actual high **23,733.70** stopped just below it.
- **CPR 23,613.09–23,743.78:** early rejection/failed hold; downside bias strengthened after loss of the lower CPR/support band.
- **Immediate support 23,613–23,550:** broken.
- **Previous close 23,547.75:** broken.
- **Previous day low 23,484.75 / breakdown 23,485:** broken; this correctly activated the bearish scenario.
- **S1 23,354.07:** highly accurate support marker; actual low **23,357.95**, only **3.88 points** above S1.

## Scenario Tally

| Scenario | Morning probability | Actual result | Hit? |
|---|---:|---|---|
| Bullish | 31% | Failed; no acceptance above 23,872–23,900 | No |
| Bearish | 29% | Triggered below 23,613 / 23,547 / 23,485 and moved to S1 zone | Secondary hit |
| Sideways | 40% | Failed; 23,500–23,880 range broke on downside | No |

**Leading scenario hit:** **No**.  
**Best-mapped scenario:** **Bearish case**, even though it was not the highest-probability case.

## Institutional / Macro Context

Final institutional data became available after the session: FIIs net sold about **₹3,912 crore**, while DIIs net bought about **₹5,109 crore** on June 1. This confirms that the morning report’s “FII selling but DII-cushioned” risk framing remained directionally relevant, though the day still closed weak. ([moneycontrol.com](https://www.moneycontrol.com/news/business/markets/fiis-net-sell-shares-worth-rs-3-912-crore-diis-net-buy-rs-5-109-crore-on-june-1-13937779.html))

Market breadth and sector context were also weak: Upstox reported **40 NIFTY50 decliners versus 10 gainers**, with FMCG, PSU Bank, Realty, Auto, and Consumer Durables among the weaker sectors, while IT, Media, and Metal were the main gainers. ([upstox.com](https://upstox.com/news/market-news/stocks/market-wrap-june-1-nifty-50-ends-at-23-382-sensex-dips-508-pts-smi-ds-nifty-bank-underperform-hul-top-laggard/article-194595/))

## Trader Plan Usefulness

| Trader type | Score | Tally |
|---|---:|---|
| Option non-directional seller | 60/100 | Range-selling thesis was vulnerable after the downside break; the “avoid during fast breaks / exit tested side” guardrail was essential. |
| Option directional seller | 62/100 | Call-selling on failed upside would have been acceptable, but the ideal rejection zone was not cleanly reached. |
| Option buyer | 82/100 | Best guidance: “puts only below 23,485” aligned with the actual breakdown and move toward S1. |
| Future intraday trader | 84/100 | Strong: shorts below 23,613 / 23,485 had clear targets at 23,550, 23,485, and 23,354. |

## Confidence Calibration

Morning overall confidence was **62%**. Final assessment: confidence was broadly reasonable for a conditional day, but the **leading sideways probability was over-weighted** relative to the bearish risk created by elevated VIX + heavy prior FII selling + failed gap-up. Direction confidence at **54%** was appropriately modest, but the report still classified the desk interpretation as **Range-selling day**, which was not the final realized regime.

## Bounded Auto-Healing Update

Processed bounded calibration only; **no core skill logic rewritten**.

Allowed updates recorded:

1. **Rolling hit-rate update:** mark expected range contained = true; direction hit = false; leading scenario hit = false; bearish secondary trigger hit = true.
2. **Failure tags added:** `sideways_leading_scenario_failed`, `actionable_range_downside_breached`, `near_open_direction_missed`, `gap_up_failed`, `bearish_secondary_scenario_worked`.
3. **Confidence offsets, bounded within ±3 points for the day:**
   - Probability model range-bias offset: **-2**
   - Global/macro supportive-cue confidence offset: **-1**
   - Institutional-flow bearish-risk confidence offset: **+1**
   - Key-level precision confidence offset: **+1**
4. **Source reliability note:** prefer final post-close sources for VIX; if sources differ by small amounts, store a VIX range and use the most corroborated final close.
5. **No promotion proposal:** one observation only; promotion rule requires at least five comparable failures before proposing a skill-rule change.

**Overall tally grade:** **70/100** — reference data and levels were strong; expected range contained the day; downside risk was well mapped, but the leading sideways/range classification and close-vs-open direction missed.
