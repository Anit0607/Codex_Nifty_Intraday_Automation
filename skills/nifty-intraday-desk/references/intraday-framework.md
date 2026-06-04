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

Trader-facing level display:

- Always calculate Pivot, CPR, R1, R2, S1, S2, previous high, previous low, previous close, expected high/low zones, tail zones, and option-writing zones in the backend.
- Do not show the full calculation table in the trader-facing morning report.
- Section 2 should expose only the decision levels that affect execution: long trigger, short trigger, upside supply/target, downside support/target, chop/no-trade zone, and base-view invalidation.
- If a calculated level such as R1, S1, CPR upper/lower, or previous day high/low is the chosen trigger or target, show the price level but do not label the row as a formula dump.

Narrow CPR expiry guardrail:

- If CPR width is below 30, the day is expiry-sensitive, and the open is inside CPR, keep close-vs-open confidence low until price accepts outside CPR or breaks a defined trigger.
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

VIX risk envelope:

```text
Approx daily range = (VIX / 100) * Nifty level * (1 / sqrt(252)) * 1.5
VIX risk envelope = open +/- approx_daily_range
```

Always separate:

- VIX Risk Envelope: the wide volatility envelope from the formula. It is for risk awareness, not the primary tradable high/low forecast.
- Primary Expected Day Range: the practical forecast range built from Expected Low Zone to Expected High Zone. This is the range the evening tally must judge against the +/-50 point tolerance.
- Expected High Zone: most likely day-high area, usually a 40-80 point band built from CPR, R1/R2, previous high, option resistance, and round numbers.
- Expected Low Zone: most likely day-low area, usually a 40-80 point band built from CPR, S1/S2, previous low, option support, and round numbers.
- Tail Expansion Zones: upside/downside extension targets if the primary range fails. Calculate them in the backend for invalidation/risk awareness, but do not show them in the morning report header.
- Opening Execution Map: trigger-based trading plan with no-trade/chop zone, long trigger, short trigger, stop-loss logic, and targets.

Do not label the VIX risk envelope as "Expected Day Range." The report header's Expected Day Range must be the primary forecast range, not the wide VIX envelope.
Do not use the phrase "Actionable Desk Range" in new reports. It was too easy to confuse with a second day high/low forecast. Execution guidance must be expressed as triggers and invalidations, not as another range to predict the full day's extremes.

Range precision rule:

- The evening tally must score expected high and expected low separately.
- A high/low zone is acceptable only if the actual high/low is inside the zone or within 50 points of the nearest zone edge.
- If either side misses by more than 50 points, mark `range_precision_hit=false` even if the broad VIX range contained the day.
- Range containment is not a model success by itself; it only means the risk envelope was wide enough.
- Expected Day Range edge precision must also be scored separately from containment. A contained day is not enough if the actual high or low is more than 50 points away from the corresponding Expected Day Range edge.
- Expected High Zone and Expected Low Zone should normally be 30-50 points wide. Width above 60 points is a visible-quality failure unless marked as exceptional uncertainty with lower confidence. Width above 80 points is not acceptable for a trader-facing precision zone.
- Legacy Actionable Desk Range precision must be audited separately when it appears in older reports. Treat its lower edge as a low forecast and upper edge as a high forecast; if either edge misses actual low/high by more than 50 points, tag `legacy_actionable_range_miss`. Do not promote it back into the report unless repeated evidence supports it.

Execution risk-reward rule:

- For long/short triggers, calculate risk from trigger to SL and reward from trigger to target 1 and target 2.
- Target 1 RR should preferably be at least 1.5. If it is below 1.25, mark the setup as weak/scalp-only or adjust the trigger/target.
- Target 2 RR should preferably be at least 2.0.
- The evening tally must report whether each trigger fired, which targets were reached, and the actual target-1/target-2 RR.

Range construction guardrails:

- On gap-up opens inside or below wide CPR after heavy FII selling, do not project expected high to the VIX upper envelope. Cap expected high near CPR upper/R1/previous high until price accepts above it.
- On failed gap-up risk days, expected low must include S1/prior low and a tail zone toward S2 if support breaks.
- If VIX is elevated and the prior day was a large selloff, widen the low-side tail before widening the upside target unless global and institutional evidence are strongly risk-on.

Gap-down reversal guardrail:

- Do not treat a gap-down open below prior low/S1 as enough evidence for a `Close below open` call by itself.
- If the bearish thesis depends on a lower breakdown trigger that has not fired, keep bearish close-direction confidence at or below 52 unless VIX is rising and the opening support shelf is failing.
- If the expected low zone is close to the opening price, the short trigger is below the open, and the long-trigger targets offer more distance than the short-trigger targets, explicitly consider a gap-down exhaustion / short-covering recovery.
- In that setup, `Close above open` is allowed even when the broader classification remains sell-on-rise, but confidence must stay modest unless VIX is already cooling.
- Tag misses from this setup as `gap_down_low_at_open_vix_cool_reversal` and `vix_cooling_underweighted` when the day low forms near the open and VIX closes materially lower.

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

Binary close-vs-open rule:

- The header must always make one black-and-white close direction call: `Close above open` or `Close below open`.
- Never write `near open`, `flat`, `conditional range`, `neutral`, or similar language in the Close vs Open Direction field.
- If the leading market-behaviour scenario is sideways, still choose the binary direction from the stronger weighted evidence between upside and downside.
- If evidence is almost balanced, choose the side with the larger Upside/Downside probability and reduce Direction Confidence. If upside and downside are exactly tied, use price action/gap plus VIX as the tie-breaker.
- Sideways probability may remain in the probability model as a range-behaviour classification, but it is not an allowed close direction.

Use Markov regime overlay as a calibration layer:

- Bull persistence supports upside.
- Bear persistence supports downside.
- Sideways persistence supports range.
- Mixed transition matrix lowers confidence.

Downside weighting guardrail:

- If the prior day was a large red candle, FIIs were heavy sellers, VIX is above 16 or rising, and the current open is a gap-up inside/wide CPR, do not let sideways probability dominate by default.
- In that setup, bearish probability should be at least equal to sideways unless price reclaims and holds CPR upper/R1 with VIX cooling.

## Confidence Scores

Give each section a confidence percentage and an overall confidence score.

Confidence should reflect:

- Data completeness.
- Source reliability.
- Agreement among CPR/gap/VIX/options/globals/FII-DII/Markov.
- Whether option-chain data is confirmed or simulated.
- Whether the day has event, expiry, or gap shock risk.

Do not overstate close-vs-open confidence. It is normally lower than key-level confidence.
