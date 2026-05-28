# Nifty 50 Post-Market Tally

Analysis Date: 2026-05-26  
Tally Time: 2026-05-26 17:00 IST  
Morning Report Reviewed: `reports/2026-05-26/morning-report.md`  

## 1. Actual Market Snapshot

| Field | Morning Reference / Forecast | Actual Result | Tally |
|---|---:|---:|---|
| Open | 24,004.10 | 24,004.10 | Correct |
| High | Not used in morning view | 24,089.80 | Post-market actual |
| Low | Not used in morning view | 23,885.45 | Post-market actual |
| Close | Not used in morning view | 23,913.70 | Post-market actual |
| Close vs Open | Near open to mildly positive if 24,000 holds | Close below open by 90.40 pts (-0.38%) | Directional lean missed |
| VIX Statistical Range | 23,625 - 24,383 | Actual 23,885 - 24,090 | Contained but too wide |
| Actionable Desk Range | 23,950 - 24,135 | Downside broke; upside held | Lower range failure correctly activated bearish triggers |
| India VIX | Prior close 16.70 | Closed 16.13 | VIX cooling confirmed |
| FII/DII | 25 May supportive | 26 May FII -2,408 Cr, DII +1,361 Cr | FII pressure returned |

Tally Confidence: 88%

## 2. Morning Thesis vs Actual

| Morning View | Actual Market Behaviour | Score |
|---|---|---:|
| Leading case: Sideways 40% | Close was -0.38% from open, within the sideways bucket, but path broke actionable lower range | 76/100 |
| Upside probability: 36% | High reached 24,089.80 but failed to sustain above 24,100 | 58/100 |
| Downside probability: 24% | Breakdown trigger below 23,922 activated and price moved toward S2 zone | 82/100 |
| Range-selling with conditional upside breakout | Range worked early, but downside break became the better tactical trade | 70/100 |

Section Score: 72/100

## 3. Key Levels Tally

| Level / Zone | Morning Logic | Actual Test | Result |
|---|---|---|---|
| 24,085 - 24,100 breakout | Bullish confirmation | High 24,089.80, no sustained acceptance above 24,100 | Strong filter |
| 24,054 - 24,083 resistance | Immediate resistance | Price stretched into this zone and failed above it | Good hit |
| 23,950 - 23,920 breakdown | Bearish turn | Broken; close finished below this band | Strong hit |
| Previous day low 23,922.85 | Breakdown support reference | Broken intraday and close below it | Strong hit |
| S2 / strong support 23,871 - 23,885 | Downside target/defence zone | Low 23,885.45, almost exact tag | Excellent hit |
| Mean reversion 24,003 - 24,032 | Sideways target | Not held into close | Miss after breakdown |

Section Score: 87/100

## 4. Probability Calibration

Morning probabilities:

- Upside: 36%
- Downside: 24%
- Sideways: 40%

Actual classification:

- Close finished below open by about 0.38%, which still fits the report's sideways bucket of roughly +/-0.4% to 0.5%.
- Intraday structure, however, was not comfortably sideways because the actionable lower range broke and the bearish case activated.
- The morning model underweighted the downside case and over-weighted the constructive lean from prior-day institutional buying.

Calibration result:

- Leading bucket hit: Yes, but with weak quality.
- Direction hit: No.
- Bearish scenario mapping worked better than the headline probability.
- Overall confidence of 68% was slightly high for a day with monthly expiry and narrow CPR.

Section Score: 68/100

## 5. Trader-Specific Review

### Option Non-Directional Seller

Morning plan allowed range selling only if 23,950 - 24,085 held. Since the lower range broke, disciplined sellers should have exited or avoided fresh neutral positions. The structure protected against the worst mistake: staying short premium after breakdown.

Score: 68/100  
Learning: Non-directional plans should visually mark "range broken = no neutral sell" more prominently.

### Option Directional Seller

Morning plan allowed call selling after failed breakout near R1 and warned PE selling invalid below 23,950. This was useful. The best directional selling idea was CE sell after failure above 24,085/24,100, not PE selling.

Score: 72/100  
Learning: On expiry plus narrow CPR days, directional sellers should prioritize failed-breakout/failure-trap trades over early support-based PE selling.

### Option Buyer

Morning plan said puts only below 23,922. That trigger fired and downside moved toward S2. This was the cleanest conditional buyer setup from the report.

Score: 78/100  
Learning: Buyer section should include "trigger fired / no trigger" binary status in evening review.

### Future Intraday Trader

Morning plan said short below 23,922 with targets 23,871 then 23,800. Actual low was 23,885.45, close to the first target. Good tactical map, though the SL above 23,975 was somewhat wide for intraday execution.

Score: 80/100  
Learning: Future trader SL should be tighter and tied to retest failure after breakdown, not only static level.

Trader Plan Section Score: 75/100

## 6. Risk / Invalidation Review

| Risk Item | Morning Trigger | Actual | Result |
|---|---|---|---|
| Bullish confirmation | 15-min hold above 24,100 | Not confirmed | Correct filter |
| Bearish confirmation | 15-min hold below 23,922 | Activated | Strong hit |
| Expiry gamma | Fast 60-100 point reversal near 24,000 | Direction shifted after early range | Valid warning |
| VIX spike risk | VIX above 17.2 with price below 23,950 | VIX cooled instead | Bear move happened without VIX panic |
| Macro shock | Crude/rupee risk | Profit booking and crude/geopolitical context pressured market | Useful |

Section Score: 78/100

## 7. What Worked

- The 24,100 breakout filter prevented false bullish chasing.
- The 23,922 breakdown trigger worked.
- S2 / strong support zone around 23,871 - 23,885 was almost exactly where the day found its low.
- Option buyer and futures trader conditional short plans worked after trigger.
- VIX statistical range contained the day.

## 8. What Did Not Work

- The headline bias was too constructive because it leaned on prior-day FII/DII buying and the 25 May breakout.
- Sideways was technically the correct bucket by close-vs-open distance, but the intraday path became a conditional bearish day after 23,922 broke.
- Actionable range confidence was too high for a monthly expiry plus very narrow CPR setup.
- Non-directional seller guidance needs stronger "do not continue after range break" emphasis.
- Markov overlay remained a proxy and should carry low confidence until automated historical reconstruction is added.

## 9. Auto-Healing / Calibration Update

Applied automatic updates:

- Add a scorecard for 2026-05-26.
- Update rolling calibration statistics.
- Add failure tags for constructive bias miss, actionable range break, and expiry/narrow-CPR underweighting.
- Keep core probability weights unchanged because one trading day is not enough evidence for model rewrite.

Bounded improvement to future 9:20 analysis:

- For expiry days with very narrow CPR and open inside CPR, the report should keep the close-vs-open bias neutral until price accepts outside CPR or breaks a defined trigger.
- Prior-day FII/DII buying should not be allowed to create a strong constructive lean when the day is expiry-sensitive and macro risks remain elevated.
- Option/futures sections should use binary execution language: "trade only if trigger fires; otherwise no trade."

Not applied:

- No CPR formula change.
- No core probability-weight rewrite.
- No increase in confidence after one mixed-but-useful outcome.

## 10. Final Tally

| Category | Score |
|---|---:|
| Header / data integrity | 94 |
| Market summary | 70 |
| Key levels | 87 |
| Expected statistical range | 66 |
| Actionable range | 62 |
| Close vs open bias | 52 |
| Probability model | 68 |
| Factor scoring | 66 |
| Scenario mapping | 80 |
| Trader-specific guidance | 75 |
| Risk invalidations | 78 |
| Overall Tally Score | 72 |

Bottom line: The 9:20 report had strong levels and useful bearish triggers, but the headline bias was too constructive; future reports should stay neutral on narrow-CPR expiry mornings until price confirms acceptance outside the CPR/range.

