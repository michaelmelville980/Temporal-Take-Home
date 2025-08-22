from temporalio import activity
from services.event_service import persist_event_log 

@activity.defn
async def CreateEventLog(order_id: str, event_type: str, payload_json: dict):
    return persist_event_log(order_id=order_id, event_type=event_type, payload_json=payload_json)


