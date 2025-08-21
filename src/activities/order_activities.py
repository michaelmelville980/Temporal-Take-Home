from temporalio import activity
from typing import Dict, Any, List
from services.order_service import order_received, order_validated, payment_charged

@activity.defn
async def ReceiveOrder(order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]) -> Dict[str, Any]:
    return await order_received(order_id, items, address_json)

@activity.defn
async def ValidateOrder(order_id: str) -> bool:
    return await order_validated(order_id)

@activity.defn
async def ChargePayment(order_id: str, payment_id: str) -> Dict[str, Any]:
    return await payment_charged(order_id, payment_id)


    
        
                       
