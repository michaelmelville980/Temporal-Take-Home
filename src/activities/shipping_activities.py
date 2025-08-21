from teporalio import activity
from typing import Dict, Any, List
from . import package_prepared, carrier_dispatched, order_shipped

@activity.defn
async def PreparePackage(order_id: str):
    package_prepared(order_id)

@activity.defn
async def DispatchCarrier(order_id: str):
    carrier_dispatched(order_id)

@activity.defn
async def ShipOrder(order_id: str):
    order_shipped(order_id)


    
        
                       
