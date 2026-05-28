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
    "notes": [],
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


def update_offsets(calibration: dict[str, Any], scorecard: dict[str, Any], outcome_score: float | None) -> None:
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
        "vix_misread": "vix_volatility",
        "option_chain_misread": "derivatives_logic",
        "global_cue_misread": "global_macro",
        "fii_dii_misread": "institutional_flow",
        "markov_misread": "markov_overlay",
    }
    offsets = calibration.setdefault("factor_confidence_offsets", {})
    for tag, factor in mapping.items():
        if tag in tags:
            offsets[factor] = int(clamp(int(offsets.get(factor, 0)) + step, -10, 10))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Nifty desk calibration from a scorecard.")
    parser.add_argument("--scorecard", required=True, help="Path to learning/scorecards/YYYY-MM-DD.json")
    parser.add_argument("--calibration", default="learning/calibration.json", help="Calibration JSON path.")
    args = parser.parse_args()

    scorecard_path = Path(args.scorecard)
    calibration_path = Path(args.calibration)
    scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
    calibration = load_json(calibration_path, DEFAULT_CALIBRATION)

    count = int(calibration.get("sample_count") or 0)
    direction_score = bool_score(scorecard.get("direction_hit"))
    range_score = bool_score(scorecard.get("range_contained"))
    scenario_score = bool_score(scorecard.get("scenario_hit"))
    key_level_score = scorecard.get("key_level_score")
    trader_scores = scorecard.get("trader_plan_scores") or {}

    outcome_score = mean(
        [
            v
            for v in [
                direction_score,
                range_score,
                scenario_score,
                float(key_level_score) if isinstance(key_level_score, (int, float)) else None,
                mean([float(v) for v in trader_scores.values() if isinstance(v, (int, float))]),
            ]
            if v is not None
        ]
    )

    confidence = scorecard.get("morning_overall_confidence")
    confidence_value = float(confidence) if isinstance(confidence, (int, float)) else None

    calibration["direction_hit_rate"] = rolling_average(calibration.get("direction_hit_rate"), count, direction_score)
    calibration["range_containment_rate"] = rolling_average(
        calibration.get("range_containment_rate"), count, range_score
    )
    calibration["scenario_hit_rate"] = rolling_average(calibration.get("scenario_hit_rate"), count, scenario_score)
    calibration["average_confidence"] = rolling_average(calibration.get("average_confidence"), count, confidence_value)
    calibration["average_outcome_score"] = rolling_average(
        calibration.get("average_outcome_score"), count, outcome_score
    )
    if confidence_value is not None and outcome_score is not None:
        calibration["confidence_error"] = rolling_average(
            calibration.get("confidence_error"), count, confidence_value - outcome_score
        )

    failure_counts = calibration.setdefault("failure_tag_counts", {})
    for tag in scorecard.get("failure_tags") or []:
        failure_counts[tag] = int(failure_counts.get(tag, 0)) + 1

    update_offsets(calibration, scorecard, outcome_score)
    calibration["sample_count"] = count + 1
    calibration["updated_at"] = datetime.now(timezone.utc).isoformat()

    notes = calibration.setdefault("notes", [])
    note = scorecard.get("notes")
    if note:
        notes.append({"date": scorecard.get("date"), "note": str(note)[:500]})
        calibration["notes"] = notes[-30:]

    calibration_path.parent.mkdir(parents=True, exist_ok=True)
    calibration_path.write_text(json.dumps(calibration, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Calibration updated: {calibration_path}")
    print(f"Samples: {calibration['sample_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

