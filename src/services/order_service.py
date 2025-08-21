from typing import Dict, Any, List
from .error_helper import flaky_call
from db.crud import create_event, create_order, validate_order, charge_payment
from db.database import SessionLocal

async def order_received(order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]) -> Dict[str, Any]:
    await flaky_call()
    db = SessionLocal()
    try:
        order = create_order(db, order_id, items, address_json)
    finally:
        db.close()
    return {"order_id": order.id, "items": order.items, "address": order.address_json}  

async def order_validated(order_id: str) -> bool:
    await flaky_call()
    db = SessionLocal()
    try:
        order = validate_order(db, order_id)
        if not order.items or len(order.items) == 0:
            raise ValueError("No items to validate")
    finally:
        db.close()
    return True

async def payment_charged(order_id: str, payment_id: str) -> Dict[str, Any]:
    await flaky_call()
    db = SessionLocal()
    try:
        payment = charge_payment(db, order_id, payment_id)
    finally:
        db.close()
    return {"status": "charged", "amount": payment.amount}






