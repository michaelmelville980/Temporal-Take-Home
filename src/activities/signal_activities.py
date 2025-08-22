from temporalio import activity
from typing import Dict, Any, List
from services.signal_service import cancel_order, update_address

@activity.defn
async def CancelOrder(order_id: str, payment_id: str):
    await cancel_order(order_id, payment_id)

@activity.defn
async def UpdateAddress(order_id: str, address: Dict[str, Any]):
    await update_address(order_id, address)


        
                       
