from typing import Dict, Any
from .error_helper import flaky_call
from src.db.crud import create_event, create_order 
from src.db.database import SessionLocal

async def order_received(order_id: str) -> Dict[str, Any]:
    await flaky_call()
    db = SessionLocal()
    try:
        order = create_order(db, order_id)
    finally:
        db.close()
    return {"order_id": order_id}

async def order_validated(order: Dict[str, Any]) -> bool:
    await flaky_call()
    # TODO: Implement DB read/write: fetch order, update validation status
    if not order.get("items"):
        raise ValueError("No items to validate")
    return True

async def payment_charged(order: Dict[str, Any], payment_id: str, db) -> Dict[str, Any]:
    """Charge payment after simulating an error/timeout first.
    You must implement your own idempotency logic in the activity or here.
    """
    await flaky_call()
    # TODO: Implement DB read/write: check payment record, insert/update payment status
    amount = sum(i.get("qty", 1) for i in order.get("items", []))
    return {"status": "charged", "amount": amount}




