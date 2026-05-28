"""Cloud runner for scheduled Nifty reports.

This script is designed for GitHub Actions. It calls the OpenAI Responses API
with web search enabled, writes the generated Markdown report, optionally writes
an evening scorecard, runs bounded calibration, and sends the PDF/report summary
to Telegram through deliver_report.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
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
    model = os.environ.get("OPENAI_MODEL", "gpt-5").strip() or "gpt-5"
    effort = os.environ.get("OPENAI_REASONING_EFFORT", "high").strip() or "high"

    payload = {
        "model": model,
        "reasoning": {"effort": effort},
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
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=600,
    )
    if not response.ok:
        raise RuntimeError(f"OpenAI API failed: {response.status_code} {response.text[:2000]}")
    return extract_response_text(response.json())


def build_common_context() -> str:
    return "\n\n".join(
        [
            "# Skill",
            read_text(SKILL_DIR / "SKILL.md"),
            "# Intraday Framework",
            read_text(REFERENCES_DIR / "intraday-framework.md"),
            "# Report Template",
            read_text(REFERENCES_DIR / "report-template.md"),
            "# Automation Ops",
            read_text(REFERENCES_DIR / "automation-ops.md"),
        ]
    )


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

Important output requirement:
Return only Markdown for the file. Do not wrap the report in code fences.

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
