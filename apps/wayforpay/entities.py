from dataclasses import dataclass


@dataclass
class Transaction:
    order_reference: str
    email: str
    phone: str
    payment_system: str
    card_pan: str
    card_type: str
    amount: str
    currency: str
    transaction_status: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_reference=data.get("orderReference", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            payment_system=data.get("paymentSystem", ""),
            card_pan=data.get("cardPan", ""),
            card_type=data.get("cardType", ""),
            amount=str(data.get("amount", "0.00")),
            currency=data.get("currency", ""),
            transaction_status=data.get("transactionStatus", ""),
        )
