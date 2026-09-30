from __future__ import annotations

from urllib.parse import quote

def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if len(digits) in {10, 11}:
        digits = "55" + digits
    if not digits.startswith("55") or len(digits) < 12:
        raise ValueError("Invalid Brazilian phone number.")
    return digits

def build_follow_up_link(phone: str, customer_name: str, protocol: str) -> str:
    digits = normalize_phone(phone)
    text = (
        f"Olá, {customer_name}. Estamos entrando em contato sobre o protocolo "
        f"{protocol}. Podemos continuar seu atendimento por aqui?"
    )
    return f"https://wa.me/{digits}?text={quote(text)}"
