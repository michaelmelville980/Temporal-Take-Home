from temporalio import activity
from typing import Dict, Any, List
from services.order_service import order_received, order_validated, payment_charged
from services.event_service import persist_event_log 

@activity.defn
async def ReceiveOrder(order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "ReceiveOrder_start", {"attempt": attempt}) 
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}") 

    # Run service
    await order_received(order_id, items, address_json)

    # Log success
    event = await persist_event_log(order_id, "ReceiveOrder_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event

@activity.defn
async def ValidateOrder(order_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "ValidateOrder_start", {"attempt": attempt}) 
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}") 

    # Run service
    await order_validated(order_id)

    # Log success
    event = await persist_event_log(order_id, "ValidateOrder_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event

@activity.defn
async def ChargePayment(order_id: str, payment_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "ChargePayment_start", {"attempt": attempt}) 
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}") 

    # Run service
    await payment_charged(order_id, payment_id)

    # Log success
    event = await persist_event_log(order_id, "ChargePayment_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event

                       
