from __future__ import annotations

import re
from email.utils import parseaddr

from ouvidoria_app.models import Complaint

PHONE_RE = re.compile(r"(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?(?:9\d{4}|\d{4})[-\s]?\d{4}")

def normalize_text(value: str) -> str:
    value = (value or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in value.split("\n")]
    return "\n".join(line for line in lines if line)

def parse_message(message: dict) -> Complaint:
    sender_name, sender_email = parseaddr(str(message.get("from") or ""))
    subject = str(message.get("subject") or "").strip()
    body = normalize_text(str(message.get("body") or ""))
    phone_match = PHONE_RE.search(body)
    protocol = str(message.get("protocol") or message.get("id") or "").strip()

    return Complaint(
        protocol=protocol,
        customer_name=sender_name or "Cliente",
        channel=str(message.get("channel") or "E-mail"),
        subject=subject,
        body=body,
        phone=phone_match.group(0) if phone_match else "",
        email=sender_email,
    )
