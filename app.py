from ouvidoria_app.services.complaint_classifier import classify
from ouvidoria_app.services.parser import parse_message
from ouvidoria_app.services.whatsapp_service import build_follow_up_link

def prepare_follow_up(message: dict) -> dict:
    complaint = parse_message(message)
    classification = classify(complaint)
    whatsapp = None
    if complaint.phone:
        try:
            whatsapp = build_follow_up_link(complaint.phone, complaint.customer_name, complaint.protocol)
        except ValueError:
            pass
    return {
        "complaint": complaint.__dict__,
        "classification": classification.__dict__,
        "whatsapp_url": whatsapp,
    }

if __name__ == "__main__":
    demo = {
        "id": "DEMO-001",
        "from": "Cliente Demo <cliente@example.com>",
        "subject": "Pedido não chegou",
        "body": "Olá, meu pedido está atrasado. Telefone (54) 99999-9999.",
    }
    print(prepare_follow_up(demo))
