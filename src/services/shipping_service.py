from typing import Dict, Any, List
from .error_helper import flaky_call
from src.db.crud import create_event, prepare_package, dispatch_carrier, ship_order
from src.db.database import SessionLocal




async def package_prepared(order_id: str) -> str:
    await flaky_call()
    db = SessionLocal()
    try:
        package = prepare_package(db, order_id)
    finally:
        db.close()
    return "Package ready"






async def carrier_dispatched(order_id: str) -> str:
    await flaky_call()
    db = SessionLocal()
    try:
        package = dispatch_carrier(db, order_id)
    finally:
        db.close()
    return "Dispatched"






async def order_shipped(order_id: str) -> str:
    await flaky_call()
    db = SessionLocal()
    try:
        package = ship_order(db, order_id)
    finally:
        db.close()
    return "Shipped"