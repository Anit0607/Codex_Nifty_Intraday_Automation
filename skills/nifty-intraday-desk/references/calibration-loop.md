# Calibration and Auto-Healing Loop

## Purpose

Improve forecast discipline over time by measuring what worked, what failed, and whether confidence was justified. The target is better calibration and process quality, not perfect accuracy.

## Evening Scorecard Fields

Create `learning/scorecards/YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "market_open": true,
  "morning_overall_confidence": 70,
  "actual_close_vs_open": "above_open",
  "predicted_close_vs_open": "above_open",
  "direction_hit": true,
  "expected_range_low": 0.0,
  "expected_range_high": 0.0,
  "vix_risk_envelope_low": 0.0,
  "vix_risk_envelope_high": 0.0,
  "actual_low": 0.0,
  "actual_high": 0.0,
  "range_contained": true,
  "expected_high_zone_low": 0.0,
  "expected_high_zone_high": 0.0,
  "expected_low_zone_low": 0.0,
  "expected_low_zone_high": 0.0,
  "high_zone_error": 0.0,
  "low_zone_error": 0.0,
  "range_precision_hit": true,
  "legacy_actionable_range_low": 0.0,
  "legacy_actionable_range_high": 0.0,
  "legacy_actionable_low_error": 0.0,
  "legacy_actionable_high_error": 0.0,
  "legacy_actionable_range_hit": false,
  "execution_trigger_score": 0.0,
  "leading_scenario": "bullish",
  "scenario_hit": true,
  "key_level_score": 0.0,
  "trader_plan_scores": {
    "option_non_directional_seller": 0.0,
    "option_directional_seller": 0.0,
    "option_buyer": 0.0,
    "future_intraday_trader": 0.0
  },
  "failure_tags": [],
  "notes": ""
}
```

## Section Scores

Score each section from 0 to 100:

- Header data integrity.
- Market summary.
- Trader key levels: whether the visible long/short triggers, target zones, chop zone, and invalidation were useful.
- VIX risk envelope containment.
- Primary expected day range.
- Expected high/low zone precision.
- Opening execution map trigger quality.
- Close vs open direction.
- Probability model.
- Factor scoring.
- Scenario mapping.
- Trader-specific guidance.
- Risk invalidations.

## Bounded Updates

Allowed automatic changes:

- Update rolling hit rates.
- Update average confidence error.
- Treat close-vs-open direction as binary only. `predicted_close_vs_open` and `actual_close_vs_open` must be `above_open` or `below_open`; legacy `near_open` forecasts should be tagged `non_binary_direction_forecast` and must not be counted as a clean direction hit.
- Update high/low range precision hit rate.
- Add range miss tags when actual high/low misses the expected high/low zone by more than 50 points.
- For older morning reports that did not contain explicit high/low zones, score the legacy Expected Day Range edges as legacy high/low forecasts so prior misses are not incorrectly treated as success.
- Score old `Actionable Desk Range` fields only as legacy diagnostics. If the actual high/low misses either edge by more than 50 points, add `legacy_actionable_range_miss`. New reports should use Opening Execution Map instead.
- Add failure tags.
- Add source reliability notes.
- Adjust confidence offsets by no more than 3 percentage points per day.
- Keep any individual factor confidence offset between -10 and +10 points.

Disallowed automatic changes:

- Removing no-hindsight rules.
- Removing risk warnings.
- Increasing leverage assumptions.
- Rewriting CPR math.
- Replacing the probability model wholesale.
- Modifying delivery credentials.

## Promotion Rule

A repeated pattern can become a proposed skill change only after at least five comparable observations. The evening agent should write a proposal under:

```text
learning/proposals/YYYY-MM-DD-proposal.md
```

The proposal should include evidence, affected rule, expected improvement, and rollback plan.
