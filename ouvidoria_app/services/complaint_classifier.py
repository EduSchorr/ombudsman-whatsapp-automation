from __future__ import annotations

import unicodedata
from ouvidoria_app.models import Classification, Complaint

RULES = {
    "Entrega": ("entrega", "atraso", "transportadora", "não recebi", "pedido não chegou"),
    "Atendimento": ("atendimento", "loja", "colaborador", "tratamento", "retorno"),
    "Financeiro": ("estorno", "reembolso", "cobrança", "pagamento", "cartão"),
    "Produto": ("produto", "avaria", "validade", "embalagem", "troca"),
}

def normalize(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in text if not unicodedata.combining(ch)).lower()

def classify(complaint: Complaint) -> Classification:
    text = normalize(f"{complaint.subject}\n{complaint.body}")
    scores = {}
    for category, terms in RULES.items():
        scores[category] = sum(normalize(term) in text for term in terms)
    category, score = max(scores.items(), key=lambda item: item[1])
    if score == 0:
        return Classification("Outros", 0.35, "No explicit rule matched the message.")
    confidence = min(0.95, 0.50 + score * 0.12)
    return Classification(category, confidence, f"{score} matching rule(s).")
