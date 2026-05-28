# Codex Automations

These are the recurring jobs configured in the Codex app. They are documented here so the GitHub repo remains the source of truth even if the local app configuration has to be recreated.

## Nifty 9:20 AM Intraday Report

- Schedule: Monday to Friday, 09:20 IST
- Status at setup: paused until `config/.env` is configured
- Workspace: `C:\Users\ANIT BOSE\Documents\Codex_Nifty Intraday Automation`

Prompt:

```text
Use $nifty-intraday-desk to generate the LIVE Nifty 50 intraday desk report for today. Verify NSE holiday status first using current sources. If the market is closed, create reports/YYYY-MM-DD/market-closed.md with the reason, render it to PDF, send the market-closed notice by Gmail and Telegram if config/.env exists, and stop. If the market is open, gather all required data using targeted web search and public/free sources, including previous trading day Nifty OHLC, today's open, India VIX previous close, global cues, GIFT Nifty, Brent, USD/INR, FII/DII flows, news/events, expiry and holiday context. Use no hindsight. Produce the full strict report with header reference prices, expected day range plus confidence, close-vs-open direction plus confidence, section confidence percentages, overall confidence, Markov regime overlay when enough data is available, and trader-specific plans for option non-directional seller, option directional seller, option buyer, and future intraday trader. Save reports/YYYY-MM-DD/morning-report.md, render a PDF using the local .venv Python and the skill delivery script, and deliver by Gmail and Telegram using config/.env when available. Clearly label assumptions and simulated derivatives data.
```

## Nifty 5 PM Post-Market Tally

- Schedule: Monday to Friday, 17:00 IST
- Status at setup: paused until `config/.env` is configured
- Workspace: `C:\Users\ANIT BOSE\Documents\Codex_Nifty Intraday Automation`

Prompt:

```text
Use $nifty-intraday-desk to run the 5 PM post-market tally for today. Verify NSE was open; if it was a holiday, skip and do not run a market tally. Load reports/YYYY-MM-DD/morning-report.md. Fetch actual post-market Nifty 50 OHLC, actual day range, close vs open direction, India VIX close or latest value, and final institutional/macro context where available. Compare the morning report section-wise against actual market data: header prices, expected range, close-vs-open direction, key levels, probability model, factor scoring, scenario mapping, trader-specific guidance, invalidations, and confidence calibration. Save reports/YYYY-MM-DD/evening-tally.md and learning/scorecards/YYYY-MM-DD.json. Run the bounded calibration updater using the local .venv Python and the skill script. Only update learning/calibration.json and proposal files; do not rewrite core skill logic automatically unless a dated proposal with evidence and rollback is created.
```

