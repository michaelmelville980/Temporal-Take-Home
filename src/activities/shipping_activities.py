from temporalio import activity
from typing import Dict, Any
from services.shipping_service import package_prepared, carrier_dispatched, order_shipped
from services.event_service import persist_event_log


@activity.defn
async def PreparePackage(order_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "PreparePackage_start", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}")

    # Run service
    await package_prepared(order_id)

    # Log success
    event = await persist_event_log(order_id, "PreparePackage_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event


@activity.defn
async def DispatchCarrier(order_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "DispatchCarrier_start", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}")

    # Run service
    await carrier_dispatched(order_id)

    # Log success
    event = await persist_event_log(order_id, "DispatchCarrier_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event


@activity.defn
async def ShipOrder(order_id: str) -> Dict[str, Any]:
    attempt = activity.info().attempt

    # Log start
    event = await persist_event_log(order_id, "ShipOrder_start", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (start): {event}")

    # Run service
    await order_shipped(order_id)

    # Log success
    event = await persist_event_log(order_id, "ShipOrder_success", {"attempt": attempt})
    activity.logger.info(f"[Attempt {attempt}] Event logged (success): {event}")

    return event
