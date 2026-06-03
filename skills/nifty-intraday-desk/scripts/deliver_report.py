"""Render a Markdown Nifty report to PDF and deliver by Gmail/Telegram.

Secrets are read from environment variables or a local .env file:
GMAIL_USER, GMAIL_APP_PASSWORD, REPORT_EMAIL_TO,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable


TELEGRAM_LIMIT = 3900


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


def markdown_to_text(markdown: str) -> str:
    text = markdown.replace("\r\n", "\n")
    text = re.sub(r"```[\s\S]*?```", lambda m: m.group(0).replace("```", ""), text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`]", "", text)
    return text.strip()


def chunks(text: str, limit: int = TELEGRAM_LIMIT) -> Iterable[str]:
    current: list[str] = []
    size = 0
    for paragraph in text.split("\n\n"):
        block = paragraph.strip()
        if not block:
            continue
        if len(block) > limit:
            for i in range(0, len(block), limit):
                yield block[i : i + limit]
            continue
        if size + len(block) + 2 > limit and current:
            yield "\n\n".join(current)
            current = [block]
            size = len(block)
        else:
            current.append(block)
            size += len(block) + 2
    if current:
        yield "\n\n".join(current)


def render_pdf(markdown_path: Path, pdf_path: Path, title: str) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        raise RuntimeError(
            "reportlab is required for PDF rendering. Install with: "
            "python -m pip install -r scripts/requirements.txt"
        ) from exc

    markdown = markdown_path.read_text(encoding="utf-8")
    lines = markdown.splitlines()
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="DeskTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            spaceAfter=12,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="DeskHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#0F766E"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="DeskBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DeskMono",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            backColor=colors.HexColor("#F3F4F6"),
            borderPadding=4,
        )
    )

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title=title,
    )

    story = [Paragraph(html.escape(title), styles["DeskTitle"])]
    in_code = False
    code_buffer: list[str] = []

    def flush_code() -> None:
        nonlocal code_buffer
        if code_buffer:
            escaped = html.escape("\n".join(code_buffer)).replace("\n", "<br/>")
            story.append(Paragraph(escaped, styles["DeskMono"]))
            story.append(Spacer(1, 5))
            code_buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buffer.append(line)
            continue
        if not stripped:
            story.append(Spacer(1, 4))
            continue
        if stripped == "---":
            story.append(PageBreak())
            continue
        if stripped.startswith("#"):
            clean = re.sub(r"^#{1,6}\s*", "", stripped)
            story.append(Paragraph(html.escape(clean), styles["DeskHeading"]))
            continue
        clean = html.escape(stripped)
        clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", clean)
        story.append(Paragraph(clean, styles["DeskBody"]))

    flush_code()
    doc.build(story)


def send_email(pdf_path: Path, subject: str, body: str) -> None:
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")
    recipients = os.environ.get("REPORT_EMAIL_TO")
    if not gmail_user or not gmail_password or not recipients:
        raise RuntimeError("Missing Gmail settings: GMAIL_USER, GMAIL_APP_PASSWORD, REPORT_EMAIL_TO")

    msg = EmailMessage()
    msg["From"] = gmail_user
    msg["To"] = recipients
    msg["Subject"] = subject
    msg.set_content(body)
    msg.add_attachment(
        pdf_path.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=pdf_path.name,
    )
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.send_message(msg)


def telegram_request(method: str, data: dict[str, str], files: dict[str, object] | None = None) -> None:
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "requests is required for Telegram delivery. Install with: "
            "python -m pip install -r scripts/requirements.txt"
        ) from exc

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    response = requests.post(url, data=data, files=files, timeout=60)
    if not response.ok:
        raise RuntimeError(f"Telegram {method} failed: {response.status_code} {response.text}")


def send_telegram(pdf_path: Path, summary_text: str, mode: str) -> None:
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        raise RuntimeError("Missing TELEGRAM_CHAT_ID")

    if mode in {"document-only", "document-and-summary"}:
        with pdf_path.open("rb") as handle:
            telegram_request(
                "sendDocument",
                data={"chat_id": chat_id},
                files={"document": handle},
            )

    if mode in {"messages-only", "document-and-summary"}:
        for idx, part in enumerate(chunks(summary_text), start=1):
            prefix = f"Part {idx}\n\n" if idx > 1 else ""
            telegram_request("sendMessage", data={"chat_id": chat_id, "text": prefix + part})


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and deliver a Nifty desk report.")
    parser.add_argument("--markdown", required=True, help="Path to Markdown report.")
    parser.add_argument("--title", required=True, help="Report title.")
    parser.add_argument("--out-dir", default=None, help="Directory for generated PDF.")
    parser.add_argument("--env", default=None, help="Optional .env file.")
    parser.add_argument("--email", action="store_true", help="Send Gmail email with PDF attachment.")
    parser.add_argument("--telegram", action="store_true", help="Send to Telegram.")
    parser.add_argument(
        "--telegram-mode",
        choices=["document-only", "document-and-summary", "messages-only"],
        default="document-only",
    )
    parser.add_argument("--dry-run", action="store_true", help="Render only; do not send.")
    args = parser.parse_args()

    load_env(args.env)
    markdown_path = Path(args.markdown)
    if not markdown_path.exists():
        raise FileNotFoundError(markdown_path)

    out_dir = Path(args.out_dir) if args.out_dir else markdown_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", args.title).strip("-")
    pdf_path = out_dir / f"{safe_name}.pdf"

    render_pdf(markdown_path, pdf_path, args.title)
    summary = markdown_to_text(markdown_path.read_text(encoding="utf-8"))

    if args.dry_run:
        print(f"PDF rendered: {pdf_path}")
        print("Dry run: delivery skipped.")
        return 0

    if args.email:
        send_email(pdf_path, args.title, "Attached is the Nifty 50 intraday desk report.")
        print("Email sent.")

    if args.telegram:
        send_telegram(pdf_path, summary, args.telegram_mode)
        print("Telegram delivery complete.")

    if not args.email and not args.telegram:
        print(f"PDF rendered: {pdf_path}")
        print("No delivery channel selected.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
