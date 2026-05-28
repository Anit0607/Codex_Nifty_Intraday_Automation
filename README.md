# Codex Nifty Intraday Automation

This workspace is configured for the `nifty-intraday-desk` Codex skill.

Use `config/.env.example` as the template for local delivery secrets. Create `config/.env` when ready; do not commit real Gmail or Telegram credentials.

GitHub is intended to be the source of truth for the skill, report history, scorecards, and calibration files. The installed local Codex skill lives under `~/.codex/skills/nifty-intraday-desk`; the repository copy lives under `skills/nifty-intraday-desk`.

Daily outputs are expected under:

- `reports/YYYY-MM-DD/morning-report.md`
- `reports/YYYY-MM-DD/morning-report.pdf`
- `reports/YYYY-MM-DD/evening-tally.md`
- `learning/scorecards/YYYY-MM-DD.json`
- `learning/calibration.json`
