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
  "expected_range_low_error": 0.0,
  "expected_range_high_error": 0.0,
  "expected_day_range_precision_hit": true,
  "vix_risk_envelope_low": 0.0,
  "vix_risk_envelope_high": 0.0,
  "actual_low": 0.0,
  "actual_high": 0.0,
  "range_contained": true,
  "expected_high_zone_low": 0.0,
  "expected_high_zone_high": 0.0,
  "expected_low_zone_low": 0.0,
  "expected_low_zone_high": 0.0,
  "expected_high_zone_width": 0.0,
  "expected_low_zone_width": 0.0,
  "high_zone_error": 0.0,
  "low_zone_error": 0.0,
  "range_precision_hit": true,
  "long_target1_rr": 0.0,
  "long_target2_rr": 0.0,
  "short_target1_rr": 0.0,
  "short_target2_rr": 0.0,
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
  "bounded_auto_healing": {
    "processed_in_scorecard": true,
    "updates": []
  },
  "notes": ""
}
```

## Section Scores

Score each section from 0 to 100:

- Header data integrity.
- Market summary.
- Trader key levels: whether the visible long/short triggers, target zones, chop zone, and invalidation were useful.
- VIX risk envelope containment.
- Primary expected day range containment and edge precision.
- Expected high/low zone precision.
- High/low zone width discipline.
- Opening execution map trigger quality.
- Trigger risk-reward quality.
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
- Track VIX risk-envelope containment separately from primary expected-range tolerance and high/low zone precision.
- Track Expected Day Range edge precision separately from containment; mark a miss when actual high/low is more than 50 points from the corresponding range edge.
- Track high/low zone width. Add `expected_high_zone_too_wide` or `expected_low_zone_too_wide` if width is above 60 points.
- Track long/short trigger risk-reward. Add `target1_rr_below_preferred` when a fired trigger's first target has RR below 1.5.
- Treat close-vs-open direction as binary only. `predicted_close_vs_open` and `actual_close_vs_open` must be `above_open` or `below_open`; legacy `near_open` forecasts should be tagged `non_binary_direction_forecast` and must not be counted as a clean direction hit.
- Update high/low range precision hit rate.
- Add range miss tags when actual high/low misses the expected high/low zone by more than 50 points.
- For older morning reports that did not contain explicit high/low zones, score the legacy Expected Day Range edges as legacy high/low forecasts so prior misses are not incorrectly treated as success.
- Score old `Actionable Desk Range` fields only as legacy diagnostics. If the actual high/low misses either edge by more than 50 points, add `legacy_actionable_range_miss`. New reports should use Opening Execution Map instead.
- Add failure tags.
- Add source reliability notes.
- Adjust confidence offsets by no more than 3 percentage points per day.
- Keep any individual factor confidence offset between -10 and +10 points.
- If the scorecard contains `bounded_auto_healing.updates`, the calibration script should apply allowed `confidence_offset` updates and `pattern_flag` counts directly, subject to the same bounds.
- For gap-down sessions where the low forms near the open, VIX cools, and the bearish breakdown trigger never fires, add the pattern tag `gap_down_low_at_open_vix_cool_reversal`.

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
