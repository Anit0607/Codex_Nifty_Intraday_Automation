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

Actionable Desk Range: XXXX - XXXX
Actionable Range Confidence: XX%

Expected High Zone: XXXX - XXXX
Expected Low Zone: XXXX - XXXX
Tail Expansion Zones: Upside XXXX - XXXX / Downside XXXX - XXXX
Range Precision Confidence: XX%

Close vs Open Direction:
Expected Bias: Close above open / Close below open / Near open
Direction Confidence: XX%

Overall Report Confidence: XX%
```

## 1. Market Summary

Maximum five lines. Include opening character, CPR position, VIX tone, probable behaviour, main directional risk, and whether the day favours trend/range/conditional breakout.

End with:

```text
Section Confidence: XX%
```

## 2. Key Levels

Use a table:

```text
Level Type | Level | Interpretation | Confidence
Strong Resistance | |
Immediate Resistance | |
Strong Support | |
Immediate Support | |
Pivot | |
CPR Zone (TC to BC) | |
Previous Day High | |
Previous Day Low | |
Previous Day Close | |
Breakout Level | |
Breakdown Level | |
VIX Risk Envelope | |
Primary Expected Day Range | |
Expected High Zone | |
Expected Low Zone | |
Tail Expansion Zones | |
R1 | |
R2 | |
S1 | |
S2 | |
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

```text
Factor | Observation | Bias | Weight | Impact | Confidence
Price Action & Gap Context | | | 35% | |
India VIX / Volatility | | | 20% | |
Derivatives Logic | | | 20% | |
Global & Macro Cues | | | 15% | |
Institutional Flow / Liquidity | | | 10% | |
Markov Regime Overlay | | Calibration layer | Non-voting or bounded | |
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

Use a table:

```text
Risk Factor | Trigger | Consequence | Primary View Invalidated | Confidence
Price invalidation | | | |
Geopolitical/news risk | | | |
FII selling shock | | | |
VIX spike | | | |
Watch window | | | |
```

End with section confidence.

## 8. Trader-Specific Desk Plan

Include all four trader types:

### Option Non-Directional Seller

- Suitable / avoid:
- Preferred structure:
- Strike or range logic:
- Entry condition:
- Stop/invalidation:
- Time window:
- Confidence:

### Option Directional Seller

- Suitable / avoid:
- Preferred side:
- Strike logic:
- Entry condition:
- Stop/invalidation:
- Time window:
- Confidence:

### Option Buyer

- Suitable / avoid:
- Calls or puts:
- Entry condition:
- Stop/invalidation:
- Target logic:
- Time window:
- Confidence:

### Future Intraday Trader

- Suitable / avoid:
- Entry zone:
- Stop:
- Targets:
- Timing:
- Confidence:

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
