from dataclasses import dataclass

@dataclass(frozen=True)
class Complaint:
    protocol: str
    customer_name: str
    channel: str
    subject: str
    body: str
    phone: str = ""
    email: str = ""

@dataclass(frozen=True)
class Classification:
    category: str
    confidence: float
    reason: str
