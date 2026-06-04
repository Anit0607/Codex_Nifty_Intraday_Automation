"""Cloud runner for scheduled Nifty reports.

This script is designed for GitHub Actions. It calls the OpenAI Responses API
with web search enabled, writes the generated Markdown report, optionally writes
an evening scorecard, runs bounded calibration, and sends the PDF to Telegram
through deliver_report.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "nifty-intraday-desk"
REFERENCES_DIR = SKILL_DIR / "references"
DELIVER_SCRIPT = SKILL_DIR / "scripts" / "deliver_report.py"
CALIBRATION_SCRIPT = SKILL_DIR / "scripts" / "update_calibration.py"
IST = ZoneInfo("Asia/Kolkata")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def today_ist() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d")


def extract_response_text(response_json: dict) -> str:
    chunks: list[str] = []
    for item in response_json.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                chunks.append(content.get("text", ""))
    if chunks:
        return "\n".join(chunks).strip()
    if "output_text" in response_json:
        return str(response_json["output_text"]).strip()
    raise RuntimeError("OpenAI response did not contain output text.")


def call_openai(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for cloud automation.")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.5").strip() or "gpt-5.5"
    effort = os.environ.get("OPENAI_REASONING_EFFORT", "high").strip() or "high"
    poll_timeout_seconds = int(os.environ.get("OPENAI_BACKGROUND_TIMEOUT_SECONDS", "2400"))

    payload = {
        "model": model,
        "reasoning": {"effort": effort},
        "background": True,
        "store": True,
        "tools": [
            {
                "type": "web_search",
                "user_location": {
                    "type": "approximate",
                    "country": "IN",
                    "city": "Kolkata",
                    "region": "West Bengal",
                    "timezone": "Asia/Kolkata",
                },
            }
        ],
        "tool_choice": "auto",
        "include": ["web_search_call.action.sources"],
        "input": prompt,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response_json = create_background_response(payload, headers)
    response_id = response_json.get("id")
    if not response_id:
        raise RuntimeError(f"OpenAI response did not include an id: {response_json}")

    print(f"OpenAI background response started: {response_id} | model={model} | effort={effort}", flush=True)
    completed = poll_background_response(response_id, headers, poll_timeout_seconds)
    return extract_response_text(completed)


def create_background_response(payload: dict, headers: dict[str, str]) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            response = requests.post(
                "https://api.openai.com/v1/responses",
                headers=headers,
                json=payload,
                timeout=(30, 120),
            )
        except requests.RequestException as exc:
            last_error = exc
            wait = attempt * 20
            print(f"OpenAI create attempt {attempt} failed: {exc}. Retrying in {wait}s.", flush=True)
            time.sleep(wait)
            continue

        if response.status_code in {429, 500, 502, 503, 504} and attempt < 3:
            wait = attempt * 30
            print(
                f"OpenAI create attempt {attempt} returned {response.status_code}. Retrying in {wait}s.",
                flush=True,
            )
            time.sleep(wait)
            continue

        if not response.ok:
            raise RuntimeError(f"OpenAI API failed: {response.status_code} {response.text[:2000]}")
        return response.json()

    raise RuntimeError(f"OpenAI create failed after retries: {last_error}")


def poll_background_response(response_id: str, headers: dict[str, str], timeout_seconds: int) -> dict:
    deadline = time.monotonic() + timeout_seconds
    poll_count = 0
    while time.monotonic() < deadline:
        poll_count += 1
        try:
            response = requests.get(
                f"https://api.openai.com/v1/responses/{response_id}",
                headers=headers,
                timeout=(30, 120),
            )
        except requests.RequestException as exc:
            print(f"OpenAI poll attempt {poll_count} failed: {exc}. Retrying.", flush=True)
            time.sleep(15)
            continue

        if response.status_code in {429, 500, 502, 503, 504}:
            print(f"OpenAI poll attempt {poll_count} returned {response.status_code}. Retrying.", flush=True)
            time.sleep(20)
            continue
        if not response.ok:
            raise RuntimeError(f"OpenAI retrieve failed: {response.status_code} {response.text[:2000]}")

        response_json = response.json()
        status = response_json.get("status")
        print(f"OpenAI response status: {status}", flush=True)
        if status == "completed":
            return response_json
        if status in {"failed", "cancelled", "incomplete"}:
            error = response_json.get("error") or response_json.get("incomplete_details") or response_json
            raise RuntimeError(f"OpenAI response ended with status={status}: {error}")

        time.sleep(20)

    raise TimeoutError(f"OpenAI background response timed out after {timeout_seconds}s: {response_id}")


def build_common_context() -> str:
    sections = [
        "# Skill",
        read_text(SKILL_DIR / "SKILL.md"),
        "# Intraday Framework",
        read_text(REFERENCES_DIR / "intraday-framework.md"),
        "# Report Template",
        read_text(REFERENCES_DIR / "report-template.md"),
        "# Automation Ops",
        read_text(REFERENCES_DIR / "automation-ops.md"),
    ]
    calibration_path = ROOT / "learning" / "calibration.json"
    if calibration_path.exists():
        sections.extend(
            [
                "# Current Calibration State",
                read_text(calibration_path),
                (
                    "Use the calibration state as a bounded adjustment layer. "
                    "Apply factor_confidence_offsets, pattern_counts, failure_tag_counts, "
                    "and rolling hit/error rates to confidence and scenario weighting. "
                    "Do not override fresh market evidence or rewrite core rules."
                ),
            ]
        )
    return "\n\n".join(sections)


def morning_prompt(date: str) -> str:
    return f"""
You are running the Nifty 9:20 AM intraday desk automation in GitHub Actions.

Analysis date: {date}
Mode: LIVE if {date} is today's IST date; otherwise BACKTEST.
Time boundary: act as of 09:20 IST on the analysis date.

Use web search for all required market data. If this is a past date, do not use
the actual close, high, low, or intraday path of the analysis date while forming
the morning view. You may use the analysis-date open/reference price only.

First verify whether NSE is open. If the market is closed, produce a concise
market-closed notice in Markdown with the reason and do not produce trading
plans. If open, produce the full Nifty 50 report exactly following the skill
template. Include clickable source links in a Sources section at the end.

Critical range requirement:
- Do not present the VIX statistical envelope as the tradable Expected Day Range.
- In the header, include VIX Risk Envelope, Expected Day Range, Expected High Zone, Expected Low Zone, Range Precision Confidence, and Opening Execution Map.
- Expected Day Range is the primary practical forecast range derived from Expected Low Zone and Expected High Zone, not the VIX envelope.
- Expected High Zone and Expected Low Zone are the primary high/low forecast and should target practical precision, normally within about +/-50 points of actual if the model is good.
- Keep Expected High Zone and Expected Low Zone tight: target 30-50 points wide; avoid more than 60 points unless explicitly lowering confidence for exceptional uncertainty.
- Do not show Tail Expansion Zones in the morning report. Keep tail levels internal and express them only as invalidation/risk levels if needed.
- Do not include "Actionable Desk Range" in new morning reports. Use Opening Execution Map instead: No-Trade/Chop Zone, Long Trigger with SL/targets, Short Trigger with SL/targets, and Execution Confidence.
- If uncertainty is high, widen the high/low zones honestly and lower confidence; do not hide uncertainty inside the VIX envelope.

Critical direction requirement:
- Close vs Open Direction must be binary only: Close above open or Close below open.
- Do not use near open, flat, neutral, conditional range, or similar wording in that field.
- If evidence is mixed, still choose above or below and lower Direction Confidence.
- Do not choose Close below open only because the market opened gap-down. If the bearish case needs a lower breakdown trigger, expected low is near the open, and VIX-cooling recovery risk is meaningful, consider Close above open with modest confidence.

Critical Section 2 requirement:
- Calculate CPR, Pivot, R1/R2, S1/S2, previous high/low/close, option zones, and range zones internally.
- Do not show a full key-level calculation table in the morning report.
- Section 2 must be "Trader Key Levels" with no more than six rows.
- The long and short rows must show Entry/Zone, SL, T1, T2, RR to T1/T2, and Action in the same row.
- Do not display raw rows named Pivot, CPR Zone, R1, R2, S1, S2, Previous Day High, Previous Day Low, or Previous Day Close unless the level is embedded as the chosen trigger/target.

Critical execution consistency requirement:
- Treat the header's Opening Execution Map as the master trade plan.
- Section 2, Scenario Mapping, Invalidations, Trader-Specific Desk Plan, and Trading Desk Interpretation must reuse the exact same long trigger, long SL, long T1/T2, short trigger, short SL, and short T1/T2.
- Do not create different exit targets in trader-specific sections. If mentioning a level beyond T2, label it as an extension beyond T2, not the primary exit target.
- Calculate and display RR to T1 and T2 for long and short triggers. If T1 RR is below 1.25, mark that setup weak/scalp-only or avoid it. If T1 RR is below 1.5, say partial booking must be fast.

Critical readability requirement:
- Factor Scoring Table must be compact and action-oriented: Factor, Bias, Weight, Trader read, Confidence.
- Do not put source links or long paragraphs inside factor or invalidation tables. Put links only in the Sources section.
- Invalidations must use "If this happens / Trader action / View invalidated / Confidence" language.
- Every invalidation row must tell the trader what to do: exit longs, exit shorts, avoid calls/puts, avoid option selling, reduce risk, or wait.

Critical trader-specific requirement:
- For Option Non-Directional Seller, state structure, entry, legs/strike rule, leg-wise SL, overall SL, target/exit, and time stop.
- For Option Directional Seller, state side, strike rule, entry trigger, spot SL, target/exit, and time stop.
- For Option Buyer, state call/put, strike rule, entry trigger, spot SL, premium SL only if premium is available/estimated, target/exit, and time stop.
- For Future Intraday Trader, use the exact master long/short trigger, SL, T1, T2, and RR.
- If an actionable entry/exit cannot be stated clearly for a trader type, mark that trader type "Avoid" rather than filling the section with vague guidance.

Important output requirement:
Return only Markdown for the file. Do not wrap the report in code fences.
After the header's Overall Report Confidence line, go directly to ## 1. Market Summary.
Do not include a Data boundary note, Reference note, or extra data-boundary paragraph.

{build_common_context()}
""".strip()


def evening_prompt(date: str, morning_report: str) -> str:
    calibration_context = read_text(REFERENCES_DIR / "calibration-loop.md")
    return f"""
You are running the Nifty 5 PM post-market tally automation in GitHub Actions.

Tally date: {date}
Time boundary: post-market after 17:00 IST.

First verify whether NSE was open. If the market was closed, produce a short
skip notice and a scorecard with market_open=false. If open, use web search to
fetch actual post-market Nifty 50 OHLC, India VIX, and final institutional/macro
context where available. Compare the morning report section-wise against
actuals. Run the bounded auto-healing logic: create a scorecard JSON and
recommend/process only bounded calibration changes. Do not rewrite core skill
logic.

Morning report to audit:

<MORNING_REPORT>
{morning_report}
</MORNING_REPORT>

Output exactly two blocks:

<EVENING_TALLY_MARKDOWN>
...Markdown tally report...
</EVENING_TALLY_MARKDOWN>

<SCORECARD_JSON>
{{...valid JSON matching the scorecard schema...}}
</SCORECARD_JSON>

Scorecard requirements:
- predicted_close_vs_open and actual_close_vs_open must be normalized to above_open or below_open only. Do not use near_open.
- Include expected_high_zone_low, expected_high_zone_high, expected_low_zone_low, expected_low_zone_high.
- Include high_zone_error and low_zone_error if calculable.
- Include expected_range_high_error, expected_range_low_error, and expected_day_range_precision_hit. Score Expected Day Range edge precision separately from containment.
- Include expected_high_zone_width and expected_low_zone_width. Add expected_high_zone_too_wide / expected_low_zone_too_wide when zone width is above 60 points.
- Include long_target1_rr, long_target2_rr, short_target1_rr, short_target2_rr when trigger, SL, and targets are available. Add target1_rr_below_preferred if fired target-1 RR is below 1.5.
- Check whether trader-specific exit targets match the master Opening Execution Map. If later sections use conflicting primary targets/stops, add execution_target_inconsistency and lower the trader guidance score.
- If the morning report has only a legacy Expected Day Range and no high/low zones, treat the high edge and low edge as legacy high/low zone forecasts and score them against the +/-50 point tolerance.
- If the morning report contains a legacy Actionable Desk Range, score it separately as legacy_actionable_range_hit using the same +/-50 edge tolerance, add legacy_actionable_range_miss when it fails, and do not let it override the primary Expected Day Range score.
- Set range_precision_hit=false if actual high or low misses the expected zone by more than 50 points.
- Do not treat range_contained=true as sufficient success when range_precision_hit=false.
- Add failure tags expected_high_miss, expected_low_miss, and range_precision_miss when applicable.

Evening tally format requirement:
- Include a trader audit table with: Item, Predicted, Actual, Deviation / Result, Verdict, Auto-heal action.
- The table must cover VIX Risk Envelope, Expected Day Range edge precision, Expected High Zone, Expected Low Zone, visible tail-zone usefulness if any were printed, long trigger RR/targets, short trigger RR/targets, and close-vs-open direction.
- Do not award a high overall score only because broad containment passed; penalize wide zones, poor target RR, redundant visible ranges, and Expected Day Range edge misses.

{build_common_context()}

# Calibration Loop
{calibration_context}
""".strip()


def parse_tagged_block(text: str, tag: str) -> str:
    pattern = rf"<{tag}>\s*(.*?)\s*</{tag}>"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Missing <{tag}> block in model output.")
    return match.group(1).strip()


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def run_command(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def deliver(markdown_path: Path, title: str, out_dir: Path) -> None:
    if not os.environ.get("TELEGRAM_BOT_TOKEN") or not os.environ.get("TELEGRAM_CHAT_ID"):
        print("Telegram secrets missing; delivery skipped.")
        return
    run_command(
        [
            sys.executable,
            str(DELIVER_SCRIPT),
            "--markdown",
            str(markdown_path),
            "--title",
            title,
            "--out-dir",
            str(out_dir),
            "--telegram",
            "--telegram-mode",
            "document-only",
        ]
    )


def run_morning(date: str) -> None:
    report_dir = ROOT / "reports" / date
    markdown_path = report_dir / "morning-report.md"
    text = call_openai(morning_prompt(date))
    write_file(markdown_path, text)
    deliver(markdown_path, f"Nifty 50 Intraday Desk Report - {date}", report_dir)


def run_evening(date: str) -> None:
    report_dir = ROOT / "reports" / date
    morning_path = report_dir / "morning-report.md"
    if not morning_path.exists():
        notice = (
            f"# Nifty 50 Post-Market Tally - {date}\n\n"
            "Morning report was not found in the repository checkout, so the 5 PM tally could not run.\n"
        )
        tally_path = report_dir / "evening-tally.md"
        write_file(tally_path, notice)
        deliver(tally_path, f"Nifty 50 Post-Market Tally - {date}", report_dir)
        return

    output = call_openai(evening_prompt(date, read_text(morning_path)))
    tally = parse_tagged_block(output, "EVENING_TALLY_MARKDOWN")
    scorecard_text = parse_tagged_block(output, "SCORECARD_JSON")
    scorecard = json.loads(scorecard_text)

    tally_path = report_dir / "evening-tally.md"
    scorecard_path = ROOT / "learning" / "scorecards" / f"{date}.json"
    write_file(tally_path, tally)
    write_file(scorecard_path, json.dumps(scorecard, indent=2, sort_keys=True))
    run_command(
        [
            sys.executable,
            str(CALIBRATION_SCRIPT),
            "--scorecard",
            str(scorecard_path),
            "--calibration",
            str(ROOT / "learning" / "calibration.json"),
        ]
    )
    deliver(tally_path, f"Nifty 50 Post-Market Tally - {date}", report_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Nifty cloud report automation.")
    parser.add_argument("--mode", choices=["morning", "evening"], required=True)
    parser.add_argument("--date", default="today", help="YYYY-MM-DD or today in Asia/Kolkata.")
    args = parser.parse_args()

    date = today_ist() if args.date == "today" else args.date
    if args.mode == "morning":
        run_morning(date)
    else:
        run_evening(date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
