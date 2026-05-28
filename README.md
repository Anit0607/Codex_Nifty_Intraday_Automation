# Codex Nifty Intraday Automation

This workspace is configured for the `nifty-intraday-desk` Codex skill.

Use `config/.env.example` as the template for local delivery secrets. Create `config/.env` when ready; do not commit real Gmail or Telegram credentials.

GitHub is intended to be the source of truth for the skill, report history, scorecards, and calibration files. The installed local Codex skill lives under `~/.codex/skills/nifty-intraday-desk`; the repository copy lives under `skills/nifty-intraday-desk`.

Cloud automation is provided through GitHub Actions:

- `Nifty 9:20 AM Intraday Report` runs at `03:50 UTC` / `09:20 IST`, Monday-Friday.
- `Nifty 5 PM Post-Market Tally` runs at `11:30 UTC` / `17:00 IST`, Monday-Friday.

Add these repository secrets before enabling live use:

- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

These must be **repository Actions secrets**, not variables and not environment-only secrets unless the workflow is also configured with that environment.

Do not create one combined multiline secret with all values. GitHub Actions does not parse secret contents into separate environment variables.

Optional repository variables:

- `OPENAI_MODEL`, default `gpt-5`
- `OPENAI_REASONING_EFFORT`, default `high`

Daily outputs are expected under:

- `reports/YYYY-MM-DD/morning-report.md`
- `reports/YYYY-MM-DD/morning-report.pdf`
- `reports/YYYY-MM-DD/evening-tally.md`
- `learning/scorecards/YYYY-MM-DD.json`
- `learning/calibration.json`
