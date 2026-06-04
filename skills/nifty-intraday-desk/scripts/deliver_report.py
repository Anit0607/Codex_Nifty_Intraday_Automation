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
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
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
    styles.add(
        ParagraphStyle(
            name="DeskTableHeader",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="DeskTableCell",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.2,
            textColor=colors.HexColor("#111827"),
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

    def clean_inline(text: str) -> str:
        clean = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
        clean = html.escape(clean.strip())
        clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", clean)
        clean = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', clean)
        return clean

    def split_table_row(line: str) -> list[str]:
        stripped = line.strip()
        if "|" not in stripped:
            return []
        if stripped.startswith("|"):
            stripped = stripped[1:]
        if stripped.endswith("|"):
            stripped = stripped[:-1]
        return [cell.strip() for cell in stripped.split("|")]

    def is_separator_row(line: str) -> bool:
        cells = split_table_row(line)
        return len(cells) >= 2 and all(re.fullmatch(r":?-{2,}:?", cell.strip()) for cell in cells)

    def is_table_start(index: int) -> bool:
        return index + 1 < len(lines) and "|" in lines[index] and is_separator_row(lines[index + 1])

    def column_widths(headers: list[str]) -> list[float]:
        count = max(1, len(headers))
        lowered = [header.lower() for header in headers]
        if count == 2:
            weights = [0.28, 0.72]
        elif count == 3:
            weights = [0.25, 0.25, 0.50]
        elif count == 4:
            weights = [0.25, 0.28, 0.28, 0.19]
        elif count == 5:
            weights = [0.22, 0.16, 0.13, 0.34, 0.15]
        elif count == 6 and any("factor" in header for header in lowered):
            weights = [0.18, 0.13, 0.10, 0.34, 0.15, 0.10]
        elif count == 7 and any("rr" in header for header in lowered):
            weights = [0.13, 0.16, 0.11, 0.11, 0.11, 0.15, 0.23]
        else:
            weights = [1 / count] * count
        total = sum(weights)
        return [doc.width * weight / total for weight in weights]

    def add_table(table_lines: list[str]) -> None:
        rows = [split_table_row(row) for row in table_lines if not is_separator_row(row)]
        rows = [row for row in rows if row]
        if not rows:
            return
        max_cols = max(len(row) for row in rows)
        normalized = [row + [""] * (max_cols - len(row)) for row in rows]
        data = []
        for row_index, row in enumerate(normalized):
            style = styles["DeskTableHeader"] if row_index == 0 else styles["DeskTableCell"]
            data.append([Paragraph(clean_inline(cell), style) for cell in row])
        table = Table(data, colWidths=column_widths(normalized[0]), repeatRows=1, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0F2F1")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 6))

    def flush_code() -> None:
        nonlocal code_buffer
        if code_buffer:
            escaped = html.escape("\n".join(code_buffer)).replace("\n", "<br/>")
            story.append(Paragraph(escaped, styles["DeskMono"]))
            story.append(Spacer(1, 5))
            code_buffer = []

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            idx += 1
            continue
        if in_code:
            code_buffer.append(line)
            idx += 1
            continue
        if is_table_start(idx):
            table_lines = [lines[idx], lines[idx + 1]]
            idx += 2
            while idx < len(lines) and "|" in lines[idx].strip() and lines[idx].strip():
                table_lines.append(lines[idx])
                idx += 1
            add_table(table_lines)
            continue
        if not stripped:
            story.append(Spacer(1, 4))
            idx += 1
            continue
        if stripped == "---":
            story.append(PageBreak())
            idx += 1
            continue
        if stripped.startswith("#"):
            clean = re.sub(r"^#{1,6}\s*", "", stripped)
            story.append(Paragraph(html.escape(clean), styles["DeskHeading"]))
            idx += 1
            continue
        story.append(Paragraph(clean_inline(stripped), styles["DeskBody"]))
        idx += 1

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
