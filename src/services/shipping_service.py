import asyncio
from typing import Dict, Any, List
from .error_helper import flaky_call
from db.crud import create_event, prepare_package, dispatch_carrier, ship_order
from db.database import SessionLocal

async def package_prepared(order_id: str) -> str:
    await flaky_call()
    def db_call():
        db = SessionLocal()
        try:
            prepare_package(db, order_id)
        finally:
            db.close()
    await asyncio.to_thread(db_call)  
    return "Package ready"

async def carrier_dispatched(order_id: str) -> str:
    await flaky_call()
    def db_call():
        db = SessionLocal()
        try:
            dispatch_carrier(db, order_id)
        finally:
            db.close()
    await asyncio.to_thread(db_call)
    return "Dispatched"


async def order_shipped(order_id: str) -> str:
    await flaky_call()
    def db_call():
        db = SessionLocal()
        try:
            ship_order(db, order_id)
        finally:
            db.close()
    await asyncio.to_thread(db_call)
    return "Shipped"