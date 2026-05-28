---
name: nifty-intraday-desk
description: Generate Nifty 50 intraday desk reports, LIVE or BACKTEST, with CPR, VIX, global cues, FII/DII, derivatives logic, Markov regime overlay, confidence scoring, trader-specific guidance, PDF/Gmail/Telegram delivery, post-market audit, and bounded calibration. Use when asked for Nifty intraday analysis, daily 9:20 reports, 5 PM tally/review, or auto-healing market-analysis workflows.
---

# Nifty Intraday Desk

Use this skill to produce a disciplined Nifty 50 intraday report and to operate the daily morning/evening review loop. Treat every output as probabilistic decision support, not a guarantee or financial advice.

## Required References

Load only the file needed for the task:

- For morning or backtest analysis, read `references/intraday-framework.md` and `references/report-template.md`.
- For delivery by PDF, Gmail, or Telegram, read `references/automation-ops.md`.
- For 5 PM tally and auto-healing, read `references/calibration-loop.md`.

## Mode Selection

Infer or ask for:

- `LIVE`: user says today, current session, morning report, or 9:20 report. Use latest available data and web search.
- `BACKTEST`: user gives a past date. Use only data that would have been known before that date's open.

Never use actual intraday or closing outcomes in BACKTEST mode.

## Morning Report Workflow

1. Confirm the analysis date and mode.
2. Verify NSE trading day and expiry/holiday context. If market is closed, produce a short closed-market notice and skip trading analysis.
3. Fetch or verify all required data using targeted web search:
   - Previous trading day Nifty 50 OHLC.
   - Current day open.
   - India VIX previous close.
   - Global cues, GIFT Nifty, Brent, USD/INR, US 10-year yield if relevant.
   - FII/DII cash flows.
   - India/global news and event context.
4. If data is missing, proceed with clearly labelled assumptions. Never stop only because a source is unavailable.
5. Calculate CPR and pivot levels mathematically from previous day OHLC.
6. Add derivatives logic. Label live option-chain values as confirmed and inferred option zones as simulated.
7. Add Markov regime overlay when enough historical data is available. Use it as a confidence layer, not as the sole decision-maker.
8. Produce the strict report format from `references/report-template.md`.
9. Save automation outputs under the workspace:
   - `reports/YYYY-MM-DD/morning-report.md`
   - `reports/YYYY-MM-DD/morning-report.pdf`
   - `reports/YYYY-MM-DD/source-notes.md`
10. Deliver through `scripts/deliver_report.py` when Gmail or Telegram delivery is requested.

## Evening Tally Workflow

At or after 5 PM IST:

1. Verify whether NSE was open. If it was a holiday, do not run a tally.
2. Load the morning report for the same date.
3. Fetch actual market data available after close:
   - Open, high, low, close.
   - Actual day range.
   - India VIX close or latest available value.
   - Final FII/DII if available, otherwise mark pending.
4. Compare section-wise:
   - Header reference prices.
   - Expected range vs actual range.
   - Close vs open direction.
   - Key levels respected or broken.
   - Bullish, bearish, and sideways scenario triggers.
   - Trader-specific guidance usefulness.
   - Confidence calibration.
5. Save:
   - `reports/YYYY-MM-DD/evening-tally.md`
   - `learning/scorecards/YYYY-MM-DD.json`
6. Run bounded calibration updates using `scripts/update_calibration.py`.

## Auto-Healing Rules

Auto-healing means improving calibration, not chasing perfection.

Allowed automatic updates:

- Rolling accuracy and confidence calibration statistics.
- Source reliability notes.
- Small confidence offsets by factor.
- Repeated failure-pattern flags.
- Suggested weight adjustments within limits defined in `references/calibration-loop.md`.

Do not automatically rewrite core skill logic, remove risk warnings, or make leverage/position sizing more aggressive. For material logic changes, create a dated proposal and preserve rollback.

## Delivery Scripts

Use scripts from this skill folder:

```powershell
python "$env:USERPROFILE\.codex\skills\nifty-intraday-desk\scripts\deliver_report.py" --help
python "$env:USERPROFILE\.codex\skills\nifty-intraday-desk\scripts\update_calibration.py" --help
```

Credentials must be local environment variables or a local `.env` file. Never ask the user to paste broker passwords, Gmail passwords, or API secrets into a chat transcript.

## Data Source Preference

Prefer free/public sources first because Indian broker access tokens are usually short-lived. Broker APIs may be added later for reliability, but only if authentication can be automated safely and legally without storing raw login credentials.

