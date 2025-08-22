from temporalio import activity
from typing import Dict, Any
from services.signal_service import cancel_order, update_address
from services.event_service import persist_event_log


@activity.defn
async def CancelOrder(order_id: str, payment_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "CancelOrder_start", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}")

    # Run service
    await cancel_order(order_id, payment_id)

    # Log success
    event = await persist_event_log(order_id, "CancelOrder_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event


@activity.defn
async def UpdateAddress(order_id: str, address: Dict[str, Any]) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "UpdateAddress_start", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}")

    # Run service
    await update_address(order_id, address)

    # Log success
    event = await persist_event_log(order_id, "UpdateAddress_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event
