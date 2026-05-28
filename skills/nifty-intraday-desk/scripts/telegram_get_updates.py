"""Print Telegram chat IDs visible to a bot.

Usage:
1. Put TELEGRAM_BOT_TOKEN in config/.env.
2. Send one message to the bot, or add it to a channel/group and post once.
3. Run this script with --env config/.env.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests


def load_env(path: str | None) -> None:
    if not path:
        return
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Telegram chat IDs visible to the bot.")
    parser.add_argument("--env", default="config/.env", help="Path to local .env file.")
    args = parser.parse_args()
    load_env(args.env)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Missing TELEGRAM_BOT_TOKEN in environment or .env file.", file=sys.stderr)
        return 1

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url, timeout=30)
    if not response.ok:
        print(f"Telegram getUpdates failed: {response.status_code} {response.text}", file=sys.stderr)
        return 1

    updates = response.json().get("result", [])
    if not updates:
        print("No updates found. Send a message to the bot/channel, then run again.")
        return 0

    seen: set[int] = set()
    for update in updates:
        message = update.get("message") or update.get("channel_post") or update.get("edited_message")
        if not message:
            continue
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        if chat_id in seen:
            continue
        seen.add(chat_id)
        title = chat.get("title") or "private chat"
        username = chat.get("username") or ""
        chat_type = chat.get("type") or ""
        print(f"TELEGRAM_CHAT_ID={chat_id} | type={chat_type} | title={title} | username={username}")

    if not seen:
        print("Updates were found, but no chat objects were readable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

