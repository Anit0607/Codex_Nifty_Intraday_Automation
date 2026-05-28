# Nifty 50 Intraday Framework

## Integrity

- Use LIVE for today's session and BACKTEST for past dates.
- In BACKTEST, use only information available before the market open of the analysis date.
- Never predict an exact close. Use probabilities, levels, and scenarios.
- Every probability set must total exactly 100%.
- Use assumptions when data is missing; label them explicitly.

## Data Collection

Fetch or verify:

- Previous trading day Nifty 50 OHLC.
- Current day open.
- India VIX previous close. If full OHLC is unavailable, use only close. Do not estimate VIX O/H/L.
- US market previous close: Dow, S&P 500, Nasdaq.
- Asian markets current morning: Nikkei, Hang Seng, Kospi.
- GIFT Nifty or SGX-equivalent indication.
- Brent crude, USD/INR, and US 10-year yield if relevant.
- Previous trading day FII/DII cash flows.
- Indian and global macro/news events.
- NSE holiday and weekly/monthly expiry context.

## CPR and Pivot

Use previous trading day OHLC:

```text
Pivot = (High + Low + Close) / 3
BC    = (High + Low) / 2
TC    = (2 * Pivot) - BC
CPR Width = abs(TC - BC)
R1 = (2 * Pivot) - Low
R2 = Pivot + (High - Low)
S1 = (2 * Pivot) - High
S2 = Pivot - (High - Low)
```

CPR width:

- `< 30`: very narrow, trending day likely.
- `30-60`: moderate, trend or range depends on open.
- `> 60`: wide, sideways or mean-reversion likely.

Open vs CPR:

- Open well above TC by more than 50 points: strong bullish opening.
- Open just above TC by 10-50 points: cautious bullish.
- Open inside CPR: balanced/sideways.
- Open just below BC: cautious bearish.
- Open well below BC by more than 50 points: strong bearish opening.

Narrow CPR expiry guardrail:

- If CPR width is below 30, the day is expiry-sensitive, and the open is inside CPR, keep the headline close-vs-open bias neutral until price accepts outside CPR or breaks a defined trigger.
- Do not let prior-day FII/DII buying alone create a constructive headline bias in this setup.
- Keep direction confidence at or below 60% unless price action, VIX, derivatives, and macro cues align.

## Gap Classification

- More than +1%: strong gap up.
- +0.3% to +1%: moderate gap up.
- Within +/-0.3%: flat open.
- -0.3% to -1%: moderate gap down.
- Less than -1%: strong gap down.

## India VIX Regime

- `< 12`: very low, range-bound/complacent.
- `12-16`: normal, balanced.
- `16-20`: elevated, directional expansion possible.
- `20-25`: high, volatile.
- `> 25`: extreme, expert-only.

Expected intraday range:

```text
Approx daily range = (VIX / 100) * Nifty level * (1 / sqrt(252)) * 1.5
Expected range = open +/- approx_daily_range
```

Always separate:

- VIX Statistical Range: the wide volatility envelope from the formula.
- Actionable Desk Range: tighter trigger-based intraday operating range derived from CPR, S/R, round strikes, and opening acceptance.

Do not treat the VIX statistical range as a trade target.

## Derivatives Logic

If live option-chain data is unavailable, simulate and label it:

- Call writing zones: previous day high, R1/R2, round numbers above open.
- Put writing zones: previous day low, S1/S2, round numbers below open.
- Max pain: round number closest to open unless confirmed by source.
- PCR greater than 1.0: put-heavy, bullish signal.
- PCR less than 0.8: call-heavy, bearish signal.
- PCR 0.8-1.0: neutral.

For this user's intraday reports, default trader guidance to SL/invalidation-based execution rather than hedge-first structures. Do not imply that SL removes all risk: fast expiry moves, liquidity gaps, and slippage can still cause losses. Avoid suggesting overnight carry unless explicitly requested.

Expiry context:

- Expiry day: gamma acceleration and forced delta hedging can create violent swings.
- Pre-holiday plus expiry: forced squaring risk.
- First day of new series: fresh writing, OI builds gradually.
- Post 3-day weekend: information compression at open, gap-fill risk.

## Global and Institutional Classification

Classify as:

- Risk-on.
- Risk-off.
- Neutral.
- Mixed but constructive.
- Mixed but fragile.

Evaluate:

- FII as structural buyer/seller using daily flow and recent trend.
- DII as liquidity floor or not.
- Brent above USD 100 as India macro risk.
- USD/INR above 85 as mild risk, above 94 as severe FII pressure signal.
- Election, RBI, Fed, earnings, geopolitical context when relevant.

## Probability Model

Weighted framework:

```text
Price Action & Gap Context: 35%
India VIX / Volatility: 20%
Derivatives / Option Logic: 20%
Global & Macro Cues: 15%
Institutional Flow / Liquidity: 10%
```

Convert evidence into:

- Upside probability: close higher than current day open.
- Downside probability: close lower than current day open.
- Sideways probability: close within about +/-0.4% to 0.5% of current day open.

Use Markov regime overlay as a calibration layer:

- Bull persistence supports upside.
- Bear persistence supports downside.
- Sideways persistence supports range.
- Mixed transition matrix lowers confidence.

## Confidence Scores

Give each section a confidence percentage and an overall confidence score.

Confidence should reflect:

- Data completeness.
- Source reliability.
- Agreement among CPR/gap/VIX/options/globals/FII-DII/Markov.
- Whether option-chain data is confirmed or simulated.
- Whether the day has event, expiry, or gap shock risk.

Do not overstate close-vs-open confidence. It is normally lower than key-level confidence.
