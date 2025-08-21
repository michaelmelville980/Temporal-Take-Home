from temporalio import activity
from typing import Dict, Any, List
from services.shipping_service import package_prepared, carrier_dispatched, order_shipped

@activity.defn
async def PreparePackage(order_id: str) -> str:
    return await package_prepared(order_id)

@activity.defn
async def DispatchCarrier(order_id: str) -> str:
    return await carrier_dispatched(order_id)

@activity.defn
async def ShipOrder(order_id: str) -> str:
    return await order_shipped(order_id)


    
        
                       
