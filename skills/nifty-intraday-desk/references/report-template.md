# Report Template

Produce every section. Add a confidence score to every major section.

## Header

```text
Nifty 50 Intraday Desk Report
Analysis Date: YYYY-MM-DD
Mode: LIVE or BACKTEST
Generated At: YYYY-MM-DD HH:MM IST

Reference Prices:
Previous Close: XXXX.XX
Today's Open: XXXX.XX

VIX Risk Envelope: XXXX - XXXX
VIX Envelope Confidence: XX%

Expected Day Range: XXXX - XXXX
Expected Range Confidence: XX%

Expected High Zone: XXXX - XXXX
Expected Low Zone: XXXX - XXXX
Range Precision Confidence: XX%

Opening Execution Map:
No-Trade / Chop Zone: XXXX - XXXX
Long Trigger: Above XXXX, SL XXXX, targets XXXX / XXXX
Short Trigger: Below XXXX, SL XXXX, targets XXXX / XXXX
Execution Confidence: XX%

Close vs Open Direction:
Expected Direction: Close above open / Close below open
Direction Confidence: XX%

Overall Report Confidence: XX%
```

After `Overall Report Confidence`, go directly to `## 1. Market Summary`.
Do not add a `Data boundary note`, `Reference note`, or any extra explanatory
paragraph between the header and Section 1.

The `Opening Execution Map` is the master trade plan. Every later entry, stop,
target, booking, and invalidation level must match this map unless the report
explicitly labels a level as an extension beyond target 2. Do not create separate
exit targets in trader-specific sections.

## 1. Market Summary

Maximum five lines. Include opening character, CPR position, VIX tone, probable behaviour, main directional risk, and whether the day favours trend/range/conditional breakout.

End with:

```text
Section Confidence: XX%
```

## 2. Trader Key Levels

Show only decision levels a trader can act on. Keep this section to six rows or fewer.
Do not list raw CPR, Pivot, R1, R2, S1, S2, previous high, previous low, or previous
close unless that level is directly selected as the trigger or target. Use those
calculations in the backend, not as visible table clutter.
Show entry, SL, targets, and RR in the same row so the trader does not need to
cross-reference sections.

```text
Plan | Entry / Zone | SL | T1 | T2 | RR to T1 / T2 | Action
Long | Above XXXX | XXXX | XXXX | XXXX | X.XX / X.XX | Enter only after acceptance
Short | Below XXXX | XXXX | XXXX | XXXX | X.XX / X.XX | Enter only after acceptance
No-trade | XXXX - XXXX | NA | NA | NA | NA | Avoid fresh directional trades
Book/avoid longs | XXXX - XXXX | NA | NA | NA | NA | Upside supply / expected high zone
Book/avoid shorts | XXXX - XXXX | NA | NA | NA | NA | Downside support / expected low zone
Base invalidation | Below XXXX / Above XXXX | NA | NA | NA | NA | Switch scenario, do not average
```

End with section confidence.

## 3. Probability Model

```text
From current day open of XXXX:

Upside Probability:   XX%
Downside Probability: XX%
Sideways Probability: XX%
Total:                100%
Section Confidence:   XX%
```

Then explain the leading scenario in 3-5 specific lines.

## 4. Factor Scoring Table

Make this section readable for a trader. Do not put source links, long sentences,
or raw data dumps inside the table. Use compact observations and explain only
what the trader should do with the factor.

```text
Factor | Bias | Weight | Trader read | Confidence
Price action / gap | Bullish/Bearish/Mixed | 35% | Long above XXXX; short below XXXX | XX%
VIX / volatility | Bullish/Bearish/Mixed | 20% | Premium risk / stop width implication | XX%
Derivatives / OI | Bullish/Bearish/Mixed | 20% | Resistance/support writers defend | XX%
Global / macro | Bullish/Bearish/Mixed | 15% | Risk-on/off pressure | XX%
FII-DII liquidity | Bullish/Bearish/Mixed | 10% | Floor or sell-pressure risk | XX%
Markov overlay | Calibration only | Non-voting | Raises/lowers confidence only | XX%
```

After the table, add one line:

```text
Desk read: Highest probability is [upside/downside/sideways]; trade only if [master trigger] confirms.
```

End with section confidence.

## 5. Scenario Mapping

```text
Bullish Case (XX%)
Price must sustain above:
VIX behaviour:
Breakout confirmation:
Upside targets:
Confidence:

Bearish Case (XX%)
Price must fail below:
VIX behaviour:
Breakdown confirmation:
Downside targets:
Confidence:

Sideways Case (XX%)
Range to hold:
Option writer defence zone:
Confirming behaviour:
Mean reversion target:
Confidence:
```

End with section confidence.

## 6. Assumptions Made

Split into:

- Missing Data Assumptions.
- Simulated Derivatives Assumptions.
- Macro Assumptions.
- Markov/Quant Assumptions.

End with section confidence.

## 7. Invalidations / Risk Factors

Use a trader-action table. Every row must say exactly what the trader should do.
Do not use abstract consequences without an action.

```text
If this happens | Trader action | View invalidated | Confidence
Spot accepts below XXXX | Exit longs / avoid calls / bearish scenario active | Close above open / bullish case | XX%
Spot accepts above XXXX | Exit shorts / avoid puts / breakout scenario active | Close below open / bearish case | XX%
VIX moves above XXXX | Cut option selling size / tighten SL / avoid fresh shorts | Range-selling comfort | XX%
News or crude shock | Stop new entries until candle closes beyond trigger | Intraday range forecast | XX%
Watch window HH:MM-HH:MM | Trade only confirmed triggers; no revenge entries | Opening read | XX%
```

End with section confidence.

## 8. Trader-Specific Desk Plan

Include all four trader types:

### Option Non-Directional Seller

Use a compact action table. If live premiums are unavailable, do not invent exact
premium targets. Use spot-level SL plus a clearly labelled premium-risk rule.

```text
Item | Plan
Suitable? | Yes/No only after [condition]
Structure | Short strangle / iron condor / avoid
Entry | After HH:MM only if spot stays inside XXXX - XXXX and VIX is not rising
Legs | Sell XXXX PE and XXXX CE / or no trade if strikes unclear
Leg-wise SL | Exit PE if spot accepts below XXXX; exit CE if spot accepts above XXXX; premium SL if available
Overall SL | Full exit if spot breaks XXXX or XXXX, or combined MTM loss hits stated limit
Target / exit | Book at XX-XX% credit decay or at HH:MM; no overnight carry
Confidence | XX%
```

### Option Directional Seller

```text
Item | Plan
Suitable? | Yes/No
Side | Sell PE for long view / sell CE for short view / avoid
Entry | Must match master long/short trigger
Strike | Strike selection rule from nearest OTM level; label simulated if OI unavailable
Spot SL | Must match master SL
Target / exit | Use master T1/T2 for partial/full booking; premium decay target if available
Time stop | Exit if trigger fails within stated window
Confidence | XX%
```

### Option Buyer

```text
Item | Plan
Suitable? | Yes/No
Instrument | Call/put and strike rule; label simulated if premium unavailable
Entry | Must match master long/short trigger
Spot SL | Must match master SL
Premium SL | Only if live/estimated premium is stated; otherwise say spot-SL only
Target / exit | Use master T1/T2; book partial at T1 and trail/exit at T2
Time stop | Exit if no follow-through by HH:MM
Confidence | XX%
```

### Future Intraday Trader

```text
Item | Plan
Suitable? | Yes/No
Long trade | Entry above XXXX, SL XXXX, T1 XXXX, T2 XXXX, RR X.XX / X.XX
Short trade | Entry below XXXX, SL XXXX, T1 XXXX, T2 XXXX, RR X.XX / X.XX
Avoid zone | XXXX - XXXX
Time stop | Exit if price returns to chop zone or no follow-through by HH:MM
Confidence | XX%
```

End with section confidence.

## 9. Trading Desk Interpretation

Classify as one:

- Buy-on-dip day.
- Sell-on-rise day.
- Range-selling day.
- Breakout-trend day.
- Avoid / wait-and-watch day.
- Extreme volatility / expert-only day.

End with one clear bottom-line sentence and section confidence.

## Integrity Footer

LIVE:

```text
LIVE Mode - Data as of [date and time]. Today's final intraday/closing data was not available at analysis time.
```

BACKTEST:

```text
Backtest Integrity: This analysis was generated using only data available as of/before market open on [date]. The actual [date] closing price and intraday outcome were not referenced.
```
