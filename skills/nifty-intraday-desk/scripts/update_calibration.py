"""Update bounded calibration stats from an evening scorecard JSON file."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CALIBRATION: dict[str, Any] = {
    "version": 1,
    "updated_at": None,
    "sample_count": 0,
    "direction_hit_rate": None,
    "range_containment_rate": None,
    "vix_risk_envelope_containment_rate": None,
    "primary_expected_range_tolerance_hit_rate": None,
    "range_precision_hit_rate": None,
    "average_high_zone_error": None,
    "average_low_zone_error": None,
    "legacy_actionable_range_hit_rate": None,
    "average_legacy_actionable_high_error": None,
    "average_legacy_actionable_low_error": None,
    "average_execution_trigger_score": None,
    "scenario_hit_rate": None,
    "average_confidence": None,
    "average_outcome_score": None,
    "confidence_error": None,
    "factor_confidence_offsets": {
        "price_action_gap": 0,
        "vix_volatility": 0,
        "derivatives_logic": 0,
        "global_macro": 0,
        "institutional_flow": 0,
        "markov_overlay": 0,
    },
    "failure_tag_counts": {},
    "pattern_counts": {},
    "notes": [],
    "metric_counts": {},
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(json.dumps(default))


def bool_score(value: Any) -> float | None:
    if value is True:
        return 100.0
    if value is False:
        return 0.0
    return None


def zone_error(actual: Any, low: Any, high: Any) -> float | None:
    if not all(isinstance(v, (int, float)) and math.isfinite(float(v)) for v in [actual, low, high]):
        return None
    actual_f = float(actual)
    low_f = min(float(low), float(high))
    high_f = max(float(low), float(high))
    if low_f <= actual_f <= high_f:
        return 0.0
    return min(abs(actual_f - low_f), abs(actual_f - high_f))


def mean(values: list[float]) -> float | None:
    clean = [v for v in values if isinstance(v, (int, float)) and math.isfinite(float(v))]
    if not clean:
        return None
    return sum(float(v) for v in clean) / len(clean)


def rolling_average(previous: float | None, count: int, new_value: float | None) -> float | None:
    if new_value is None:
        return previous
    if previous is None or count <= 0:
        return float(new_value)
    return ((previous * count) + float(new_value)) / (count + 1)


def rolling_metric(calibration: dict[str, Any], key: str, new_value: float | None) -> None:
    if new_value is None:
        return
    counts = calibration.setdefault("metric_counts", {})
    count = int(counts.get(key, 0))
    previous = calibration.get(key)
    calibration[key] = rolling_average(previous, count, float(new_value))
    counts[key] = count + 1


def numeric(value: Any) -> float | None:
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    return None


def normalized_direction(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    clean = value.strip().lower().replace("-", "_").replace(" ", "_")
    if not clean:
        return None
    if "near" in clean or "flat" in clean or "neutral" in clean or "conditional" in clean:
        return None
    if "above" in clean or "higher" in clean or "positive" in clean or "up" in clean:
        return "above_open"
    if "below" in clean or "lower" in clean or "negative" in clean or "down" in clean:
        return "below_open"
    return None


def actual_direction(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    clean = value.strip().lower().replace("-", "_").replace(" ", "_")
    if "above" in clean or "higher" in clean or "positive" in clean or "up" in clean:
        return "above_open"
    if "below" in clean or "lower" in clean or "negative" in clean or "down" in clean:
        return "below_open"
    return None


def normalize_binary_direction(scorecard: dict[str, Any]) -> float | None:
    predicted_raw = scorecard.get("predicted_close_vs_open")
    actual_raw = scorecard.get("actual_close_vs_open")
    predicted = normalized_direction(predicted_raw)
    actual = actual_direction(actual_raw)

    if actual is not None:
        scorecard["actual_close_vs_open"] = actual

    if predicted is None:
        tags = scorecard.setdefault("failure_tags", [])
        if "non_binary_direction_forecast" not in tags:
            tags.append("non_binary_direction_forecast")
        scorecard["direction_hit"] = False
        scorecard.setdefault("direction_precision_basis", "legacy_non_binary_forecast")
        return 0.0

    scorecard["predicted_close_vs_open"] = predicted
    if actual is None:
        return bool_score(scorecard.get("direction_hit"))

    hit = predicted == actual
    scorecard["direction_hit"] = hit
    return bool_score(hit)


def normalize_range_precision_fields(scorecard: dict[str, Any]) -> None:
    """Backfill precision fields for legacy scorecards that had only range edges."""
    high_low = numeric(scorecard.get("expected_high_zone_low"))
    high_high = numeric(scorecard.get("expected_high_zone_high"))
    low_low = numeric(scorecard.get("expected_low_zone_low"))
    low_high = numeric(scorecard.get("expected_low_zone_high"))
    if high_low is not None and high_high is not None and low_low is not None and low_high is not None:
        return

    legacy_low = numeric(scorecard.get("expected_range_low"))
    legacy_high = numeric(scorecard.get("expected_range_high"))
    if legacy_low is None or legacy_high is None:
        return

    scorecard.setdefault("expected_high_zone_low", legacy_high)
    scorecard.setdefault("expected_high_zone_high", legacy_high)
    scorecard.setdefault("expected_low_zone_low", legacy_low)
    scorecard.setdefault("expected_low_zone_high", legacy_low)
    scorecard.setdefault("range_precision_basis", "legacy_expected_range_edges")


def factor_key(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    clean = value.strip().lower()
    mapping = {
        "price action & gap context": "price_action_gap",
        "price action and gap context": "price_action_gap",
        "price_action_gap": "price_action_gap",
        "india vix / volatility": "vix_volatility",
        "india vix volatility": "vix_volatility",
        "vix_volatility": "vix_volatility",
        "derivatives logic": "derivatives_logic",
        "derivatives / option logic": "derivatives_logic",
        "derivatives_logic": "derivatives_logic",
        "global & macro cues": "global_macro",
        "global macro": "global_macro",
        "global_macro": "global_macro",
        "institutional flow / liquidity": "institutional_flow",
        "institutional flow": "institutional_flow",
        "institutional_flow": "institutional_flow",
        "markov regime overlay": "markov_overlay",
        "markov_overlay": "markov_overlay",
    }
    return mapping.get(clean)


def bounded_updates(scorecard: dict[str, Any]) -> list[dict[str, Any]]:
    healing = scorecard.get("bounded_auto_healing")
    if not isinstance(healing, dict):
        return []
    updates = healing.get("updates")
    if not isinstance(updates, list):
        return []
    return [update for update in updates if isinstance(update, dict)]


def apply_bounded_auto_healing(calibration: dict[str, Any], scorecard: dict[str, Any]) -> bool:
    applied_confidence_offset = False
    offsets = calibration.setdefault("factor_confidence_offsets", {})
    pattern_counts = calibration.setdefault("pattern_counts", {})

    for update in bounded_updates(scorecard):
        update_type = update.get("type")
        if update_type == "confidence_offset":
            key = factor_key(update.get("factor"))
            delta = numeric(update.get("delta_points"))
            if key is None or delta is None:
                continue
            if update.get("within_daily_limit") is False or update.get("within_factor_limit") is False:
                continue
            offsets[key] = round(clamp(float(offsets.get(key, 0)) + delta, -10, 10), 2)
            applied_confidence_offset = True
        elif update_type == "pattern_flag":
            name = update.get("name")
            if isinstance(name, str) and name.strip():
                pattern_counts[name] = int(pattern_counts.get(name, 0)) + 1

    return applied_confidence_offset


def has_legacy_actionable_range(scorecard: dict[str, Any]) -> bool:
    if scorecard.get("legacy_actionable_range_present") is False:
        return False
    low = numeric(scorecard.get("legacy_actionable_range_low"))
    high = numeric(scorecard.get("legacy_actionable_range_high"))
    if low is None or high is None:
        return False
    return not (low == 0 and high == 0)


def remove_failure_tag(scorecard: dict[str, Any], tag: str) -> None:
    tags = scorecard.get("failure_tags")
    if isinstance(tags, list):
        scorecard["failure_tags"] = [item for item in tags if item != tag]


def update_offsets(calibration: dict[str, Any], scorecard: dict[str, Any], outcome_score: float | None) -> None:
    if apply_bounded_auto_healing(calibration, scorecard):
        return

    confidence = scorecard.get("morning_overall_confidence")
    if not isinstance(confidence, (int, float)) or outcome_score is None:
        return

    error = float(confidence) - outcome_score
    step = 0
    if error > 12:
        step = -1
    elif error < -12:
        step = 1

    tags = set(scorecard.get("failure_tags") or [])
    mapping = {
        "gap_misread": "price_action_gap",
        "gap_up_failed": "price_action_gap",
        "non_binary_direction_forecast": "price_action_gap",
        "direction_miss": "price_action_gap",
        "leading_bearish_scenario_miss": "price_action_gap",
        "sell_on_rise_classification_miss": "price_action_gap",
        "vix_misread": "vix_volatility",
        "vix_expansion_underweighted": "vix_volatility",
        "vix_cooling_underweighted": "vix_volatility",
        "range_precision_miss": "vix_volatility",
        "legacy_actionable_range_miss": "price_action_gap",
        "option_chain_misread": "derivatives_logic",
        "global_cue_misread": "global_macro",
        "fii_dii_misread": "institutional_flow",
        "fii_pressure_materialized": "institutional_flow",
        "markov_misread": "markov_overlay",
    }
    offsets = calibration.setdefault("factor_confidence_offsets", {})
    for tag, factor in mapping.items():
        if tag in tags:
            offsets[factor] = round(clamp(float(offsets.get(factor, 0)) + step, -10, 10), 2)


def apply_scorecard(calibration: dict[str, Any], scorecard_path: Path) -> dict[str, Any]:
    scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
    normalize_range_precision_fields(scorecard)
    count = int(calibration.get("sample_count") or 0)
    direction_score = normalize_binary_direction(scorecard)
    range_score = bool_score(scorecard.get("range_contained"))
    vix_envelope_score = bool_score(scorecard.get("vix_risk_envelope_contained"))
    primary_range_tolerance_score = bool_score(scorecard.get("expected_range_edge_tolerance_hit"))
    high_error = zone_error(
        scorecard.get("actual_high"),
        scorecard.get("expected_high_zone_low"),
        scorecard.get("expected_high_zone_high"),
    )
    low_error = zone_error(
        scorecard.get("actual_low"),
        scorecard.get("expected_low_zone_low"),
        scorecard.get("expected_low_zone_high"),
    )
    if high_error is not None:
        scorecard["high_zone_error"] = high_error
    if low_error is not None:
        scorecard["low_zone_error"] = low_error

    range_precision = scorecard.get("range_precision_hit")
    if not isinstance(range_precision, bool) and high_error is not None and low_error is not None:
        range_precision = high_error <= 50.0 and low_error <= 50.0
        scorecard["range_precision_hit"] = bool(range_precision)

    if range_precision is False:
        tags = scorecard.setdefault("failure_tags", [])
        if "range_precision_miss" not in tags:
            tags.append("range_precision_miss")
        if high_error is not None and high_error > 50 and "expected_high_miss" not in tags:
            tags.append("expected_high_miss")
        if low_error is not None and low_error > 50 and "expected_low_miss" not in tags:
            tags.append("expected_low_miss")

    legacy_actionable_high_error = None
    legacy_actionable_low_error = None
    legacy_actionable_hit = None
    if has_legacy_actionable_range(scorecard):
        legacy_actionable_high_error = zone_error(
            scorecard.get("actual_high"),
            scorecard.get("legacy_actionable_range_high"),
            scorecard.get("legacy_actionable_range_high"),
        )
        legacy_actionable_low_error = zone_error(
            scorecard.get("actual_low"),
            scorecard.get("legacy_actionable_range_low"),
            scorecard.get("legacy_actionable_range_low"),
        )
        legacy_actionable_hit = scorecard.get("legacy_actionable_range_hit")
        if legacy_actionable_high_error is not None:
            scorecard["legacy_actionable_high_error"] = legacy_actionable_high_error
        if legacy_actionable_low_error is not None:
            scorecard["legacy_actionable_low_error"] = legacy_actionable_low_error
        if (
            not isinstance(legacy_actionable_hit, bool)
            and legacy_actionable_high_error is not None
            and legacy_actionable_low_error is not None
        ):
            legacy_actionable_hit = legacy_actionable_high_error <= 50.0 and legacy_actionable_low_error <= 50.0
            scorecard["legacy_actionable_range_hit"] = bool(legacy_actionable_hit)
        if legacy_actionable_hit is False:
            tags = scorecard.setdefault("failure_tags", [])
            if "legacy_actionable_range_miss" not in tags:
                tags.append("legacy_actionable_range_miss")
    else:
        scorecard["legacy_actionable_range_present"] = False
        for key in [
            "legacy_actionable_high_error",
            "legacy_actionable_low_error",
            "legacy_actionable_range_hit",
        ]:
            scorecard.pop(key, None)
        remove_failure_tag(scorecard, "legacy_actionable_range_miss")

    range_precision_score = bool_score(range_precision)
    legacy_actionable_score = bool_score(legacy_actionable_hit)
    scenario_score = bool_score(scorecard.get("scenario_hit"))
    key_level_score = scorecard.get("key_level_score")
    execution_trigger_score = scorecard.get("execution_trigger_score")
    trader_scores = scorecard.get("trader_plan_scores") or {}

    outcome_score = mean(
        [
            v
            for v in [
                direction_score,
                range_precision_score if range_precision_score is not None else range_score,
                scenario_score,
                float(key_level_score) if isinstance(key_level_score, (int, float)) else None,
                mean([float(v) for v in trader_scores.values() if isinstance(v, (int, float))]),
            ]
            if v is not None
        ]
    )

    confidence = scorecard.get("morning_overall_confidence")
    confidence_value = float(confidence) if isinstance(confidence, (int, float)) else None

    rolling_metric(calibration, "direction_hit_rate", direction_score)
    rolling_metric(calibration, "range_containment_rate", range_score)
    rolling_metric(calibration, "vix_risk_envelope_containment_rate", vix_envelope_score)
    rolling_metric(calibration, "primary_expected_range_tolerance_hit_rate", primary_range_tolerance_score)
    rolling_metric(calibration, "range_precision_hit_rate", range_precision_score)
    rolling_metric(calibration, "average_high_zone_error", high_error)
    rolling_metric(calibration, "average_low_zone_error", low_error)
    rolling_metric(calibration, "legacy_actionable_range_hit_rate", legacy_actionable_score)
    rolling_metric(calibration, "average_legacy_actionable_high_error", legacy_actionable_high_error)
    rolling_metric(calibration, "average_legacy_actionable_low_error", legacy_actionable_low_error)
    rolling_metric(
        calibration,
        "average_execution_trigger_score",
        float(execution_trigger_score) if isinstance(execution_trigger_score, (int, float)) else None,
    )
    rolling_metric(calibration, "scenario_hit_rate", scenario_score)
    rolling_metric(calibration, "average_confidence", confidence_value)
    rolling_metric(calibration, "average_outcome_score", outcome_score)
    if confidence_value is not None and outcome_score is not None:
        rolling_metric(calibration, "confidence_error", confidence_value - outcome_score)

    failure_counts = calibration.setdefault("failure_tag_counts", {})
    for tag in scorecard.get("failure_tags") or []:
        failure_counts[tag] = int(failure_counts.get(tag, 0)) + 1

    update_offsets(calibration, scorecard, outcome_score)
    calibration["sample_count"] = count + 1

    notes = calibration.setdefault("notes", [])
    note = scorecard.get("notes")
    if note:
        notes.append({"date": scorecard.get("date"), "note": str(note)[:500]})
        calibration["notes"] = notes[-30:]

    scorecard_path.write_text(json.dumps(scorecard, indent=2, sort_keys=True), encoding="utf-8")
    return calibration


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Nifty desk calibration from a scorecard.")
    parser.add_argument("--scorecard", help="Path to learning/scorecards/YYYY-MM-DD.json")
    parser.add_argument("--rebuild-dir", help="Rebuild calibration from all JSON scorecards in this directory.")
    parser.add_argument("--calibration", default="learning/calibration.json", help="Calibration JSON path.")
    args = parser.parse_args()

    calibration_path = Path(args.calibration)
    if args.rebuild_dir:
        calibration = json.loads(json.dumps(DEFAULT_CALIBRATION))
        for path in sorted(Path(args.rebuild_dir).glob("*.json")):
            calibration = apply_scorecard(calibration, path)
    elif args.scorecard:
        calibration = load_json(calibration_path, DEFAULT_CALIBRATION)
        calibration = apply_scorecard(calibration, Path(args.scorecard))
    else:
        parser.error("Either --scorecard or --rebuild-dir is required.")

    calibration["updated_at"] = datetime.now(timezone.utc).isoformat()

    calibration_path.parent.mkdir(parents=True, exist_ok=True)
    calibration_path.write_text(json.dumps(calibration, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Calibration updated: {calibration_path}")
    print(f"Samples: {calibration['sample_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
