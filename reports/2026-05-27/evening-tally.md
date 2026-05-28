# Nifty 50 Post-Market Tally

Analysis Date: 2026-05-27  
Tally Time: 2026-05-27 17:00 IST  
Morning Report Reviewed: `reports/2026-05-27/morning-report.md`  

## 1. Actual Market Snapshot

| Field | Morning Reference / Forecast | Actual Result | Tally |
|---|---:|---:|---|
| Open | 23,880.35 | 23,880.35 | Correct |
| High | Not used in morning view | 23,983.20 | Post-market actual |
| Low | Not used in morning view | 23,858.25 | Post-market actual |
| Close | Not used in morning view | 23,907.15 | Post-market actual |
| Close vs Open | Near open, mild downside risk | Close above open by 26.80 pts | Near-open call hit; downside lean did not play out |
| Actual Day Range | Expected broad range: 23,516 - 24,244 | 124.95 pts | Contained, but forecast range too wide |
| India VIX | Prior close 16.13 | Closed near 14.98 | VIX cooling view confirmed |

Tally Confidence: 86%

## 2. Morning Thesis vs Actual

| Morning View | Actual Market Behaviour | Score |
|---|---|---:|
| Leading case: Sideways 44% | Nifty closed only 26.80 pts above open and 6.55 pts below previous close | 88/100 |
| Downside probability: 31% | Breakdown below 23,800 did not happen | 62/100 |
| Upside probability: 25% | No breakout above 24,050; upside capped below 24,000 | 72/100 |
| Range-selling day with conditional breakdown risk | Range-selling worked; conditional breakdown did not trigger | 82/100 |

Section Score: 78/100

## 3. Key Levels Tally

| Level / Zone | Morning Logic | Actual Test | Result |
|---|---|---|---|
| 23,800 breakdown | Bearish trigger | Low 23,858.25, no break | Correct invalidation |
| 23,836 - 23,885 support | Immediate support cluster | Low formed inside this zone | Strong hit |
| 23,938 - 24,000 resistance | Immediate resistance / CPR supply | High 23,983.20, rejected below 24,000 | Strong hit |
| 24,040 - 24,050 breakout | Bullish confirmation | Not reached | Correct filter |
| 23,913 - 23,963 mean reversion | Sideways target | Close 23,907.15, near target band | Good hit |

Section Score: 86/100

## 4. Probability Calibration

Morning probabilities:

- Upside: 25%
- Downside: 31%
- Sideways: 44%

Actual classification:

- Close finished above open, but by only 0.11%.
- Close remained within the morning sideways definition of roughly +/-0.4% to 0.5% from open.
- Therefore, the correct outcome bucket is **Sideways / near-open**, not a clean directional upside day.

Calibration result:

- Leading scenario hit: Yes.
- Directional nuance: Mild miss, because the report leaned slightly downside while actual closed slightly above open.
- Confidence was conservative: 66% overall vs stronger realized fit.

Section Score: 82/100

## 5. Trader-Specific Review

### Option Non-Directional Seller

Morning view said range-selling was suitable only after 30-45 minutes if 23,800 - 24,050 held. That was the best trader category for the day because both sides stayed contained and VIX cooled.

Score: 75/100  
Learning: Future reports should give a cleaner SL-based intraday structure instead of hedge-first language.

### Option Directional Seller

Morning view preferred call-side selling after rejection near CPR/24,000. That broadly worked because 24,000 was not reclaimed, but conviction should have stayed moderate because the index did not trend down.

Score: 62/100  
Learning: Directional sellers needed quicker profit booking; trend follow-through was absent.

### Option Buyer

Morning view warned against blind buying and required 23,800 breakdown or 24,050 breakout. Neither happened, so the avoid/conditional stance was correct.

Score: 52/100  
Learning: Buyer section should explicitly say "no trade if trigger does not fire."

### Future Intraday Trader

Morning view said avoid the middle zone and trade only outside 23,835/23,800 or 24,050. Since no clean trigger occurred, the correct behaviour was mostly no-trade or scalp-only.

Score: 70/100  
Learning: Future reports should mark "no-trade zone" more visually and prominently.

Trader Plan Section Score: 65/100

## 6. Risk / Invalidation Review

| Risk Item | Morning Trigger | Actual | Result |
|---|---|---|---|
| Bullish invalidation | Sustain above 24,050 | Not triggered | Correct |
| Bearish acceleration | Sustain below 23,800 | Not triggered | Correct |
| VIX spike risk | VIX above 17.2 | VIX cooled to 14.98 | Risk did not materialize |
| Watch window | 9:20 - 10:15 acceptance/rejection | Market stayed contained | Useful |
| Holiday/expiry caution | Avoid aggressive late trades | Valid due next-day holiday/expiry context | Useful |

Section Score: 80/100

## 7. What Worked

- The sideways/range-selling thesis was correct.
- 23,800 as breakdown trigger worked well because price never accepted below it.
- 24,000/24,050 as upside filter worked well because upside failed below that zone.
- VIX cooling reduced trend risk and supported option premium decay.
- The warning against blind option buying was appropriate.

## 8. What Did Not Work

- Expected day range was statistically correct but too wide for actionable intraday use.
- Direction bias was slightly too bearish; actual close was near open but above it.
- Markov overlay was only a proxy and should not be counted as a strong input.
- Trader-specific language used hedge-first wording, which does not match the preferred intraday SL-based style.
- Visual density of the report needs improvement for faster trader reading.

## 9. Auto-Healing / Calibration Update

Allowed update:

- Record one successful sideways scenario.
- Record range estimate as "contained but too wide."
- Reduce future practical/actionable range confidence when VIX formula produces very broad bands but opening structure is tight.
- Add preference: intraday trader guidance should default to SL/invalidation, not hedge-first plans.

Not allowed:

- Do not rewrite the core model from one data point.
- Do not increase confidence aggressively after one good hit.
- Do not remove risk warnings from naked option selling or buying.

Calibration Action: Update learning scorecard and calibration file only. No core probability-weight change from a single sample.

## 10. Final Tally

| Category | Score |
|---|---:|
| Header / data integrity | 92 |
| Market summary | 82 |
| Key levels | 86 |
| Expected range | 65 |
| Close vs open bias | 70 |
| Probability model | 82 |
| Scenario mapping | 84 |
| Trader-specific guidance | 65 |
| Risk invalidations | 80 |
| Overall Tally Score | 78 |

Bottom line: The 9:20 AM report was directionally cautious but structurally useful; its best call was the sideways/range-selling thesis, while the biggest improvement area is making the actionable range and trader execution plan cleaner and more SL-based.

