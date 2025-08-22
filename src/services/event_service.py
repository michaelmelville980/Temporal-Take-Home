from temporalio import activity
import asyncio
from db.crud import create_event
from db.database import SessionLocal 
from typing import Dict, Any
from .error_helper import flaky_call

async def persist_event_log(order_id: str, event_type: str, payload_json: dict) -> dict:
    await flaky_call()
    
    def db_call():
        db = SessionLocal()
        try:
            return create_event(db, order_id, event_type, payload_json)
        finally:
            db.close()

    event = await asyncio.to_thread(db_call)

    return {
        "event_id": event.id,
        "order_id": event.order_id,
        "event_type": event.type,
        "payload": event.payload_json,
        "time": event.ts.isoformat() if event.ts else None,  
    }
