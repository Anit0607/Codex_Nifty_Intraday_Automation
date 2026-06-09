# Automation Operations

## Recommended Data Source Policy

Start with public/free sources and web verification. Do not depend on broker login credentials for the first production version.

Reason: most Indian broker access tokens, including common retail broker APIs, are session-bound or expire daily. A daily token dependency can break the 9:20 report exactly when reliability matters.

Optional later upgrade:

- Add a broker or paid market data API only if it supports stable refresh-token flow or server-side app credentials.
- Store credentials in local environment variables only.
- Never store raw trading passwords, TOTP seeds, or PINs in this skill.

## Local Environment Variables

Use a local `.env` file or process environment:

```text
# AI providers. Configure at least one. Default order uses Anthropic first.
AI_PROVIDER_ORDER=anthropic,openai
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-opus-4-8
ANTHROPIC_EFFORT=high

# Optional OpenAI fallback
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.5
OPENAI_REASONING_EFFORT=high

TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=-1001234567890

# Optional Gmail fallback
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
REPORT_EMAIL_TO=recipient@example.com
```

Use a Gmail app password, not the normal Gmail password.

## AI Provider Failover

The cloud agent supports:

- Anthropic Claude API using `claude-opus-4-8` with adaptive thinking and
  high effort.
- OpenAI Responses API as an alternate provider.

`AI_PROVIDER_ORDER` controls priority. The default is `anthropic,openai`.
When the first provider fails because of quota, authentication, rate limits,
network errors, or another provider-level error, the agent attempts the next
configured provider.

For GitHub Actions, create separate repository secrets:

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY` (optional fallback)
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Enable Anthropic web search in the Claude Console organization. Without web
search, Claude cannot reliably fetch current market data for LIVE reports.
Never store provider keys in the repository.

## Delivery

Telegram is the primary channel. Gmail is optional. Telegram delivery should send
only the PDF document, with no separate text summary and no document caption.

Convert Markdown to PDF and deliver:

```powershell
python "$env:USERPROFILE\.codex\skills\nifty-intraday-desk\scripts\deliver_report.py" `
  --markdown "reports\YYYY-MM-DD\morning-report.md" `
  --title "Nifty 50 Intraday Desk Report - YYYY-MM-DD" `
  --out-dir "reports\YYYY-MM-DD" `
  --telegram `
  --telegram-mode document-only `
  --env "config\.env"
```

Do not use `document-and-summary` or `messages-only` for the scheduled morning
or evening reports unless the user explicitly asks to restore text messages.

## Holiday Handling

The 9:20 agent must check whether NSE is open. If closed:

- Send a closed-market notice by Telegram when configured; Gmail is optional.
- Do not create a trading report.
- Record the reason in `reports/YYYY-MM-DD/market-closed.md`.

The 5 PM agent is scheduled on weekdays but must self-skip on holidays. This is operationally safer than trying to rewrite the calendar schedule for every special NSE holiday.

## Suggested Automation Prompts

Morning prompt:

```text
Use $nifty-intraday-desk to generate the LIVE Nifty 50 intraday report for today. Verify NSE holiday status first. If the market is closed, send a market-closed notice by Telegram when config/.env contains Telegram credentials and stop. If open, produce the full strict report with section confidence scores, overall confidence, expected day range, close-vs-open direction, and trader-specific desk plans. Save Markdown/PDF under reports/YYYY-MM-DD and deliver by Telegram using config/.env when available. Use Gmail only if explicitly configured and requested.
```

Evening prompt:

```text
Use $nifty-intraday-desk to run the 5 PM post-market tally for today. Verify NSE was open; if closed, skip. Load the morning report, fetch actual post-market OHLC/VIX data, compare section-wise, score forecast quality and confidence calibration, save reports/YYYY-MM-DD/evening-tally.md and learning/scorecards/YYYY-MM-DD.json, then run bounded calibration update. Render the tally PDF and deliver by Telegram when config/.env contains Telegram credentials. Do not rewrite core skill logic without creating a dated proposal.
```
