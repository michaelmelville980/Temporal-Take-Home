from teporalio import activity
from typing import Dict, Any, List
from . import order_received, order_validated, payment_charged

@activity.defn
async def ReceiveOrder(order_id: str, items: List[Dict[str, Any]]):
    order_received(order_id, items)

@activity.defn
async def ValidateOrder(order_id: str):
    order_validated(order_id)

@activity.defn
async def ChargePayment(order_id: str, payment_id: str):
    payment_charged(order_id, payment_id)


    
        
                       
