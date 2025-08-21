from typing import Dict, Any, List
from .error_helper import flaky_call
from db.crud import remove_and_refund_order, change_address
from db.database import SessionLocal
import asyncio

async def cancel_order(order_id: str, payment_id: str):
    await flaky_call()
    def db_call():
        db = SessionLocal()
        try:
            return remove_and_refund_order(db, order_id, payment_id)
        finally:
            db.close()
    await asyncio.to_thread(db_call) # prevents blocking of async event loop


async def update_address(order_id: str, address: Dict[str, Any]):
    await flaky_call()
    def db_call():
        db = SessionLocal()
        try:
            return change_address(db, order_id, address)
        finally:
            db.close()
    await asyncio.to_thread(db_call) # prevents blocking of async event loop

