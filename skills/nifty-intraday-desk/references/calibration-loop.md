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
  "actual_low": 0.0,
  "actual_high": 0.0,
  "range_contained": true,
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
- Key levels.
- Expected range.
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

