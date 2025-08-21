from temporalio import workflow
from datetime import timedelta
from activities import PreparePackage, DispatchCarrier
from . import ShippingWorkflow
from typing import Dict, Any, List

@workflow.defn
class ShippingWorkflow:
    @workflow.run
    async def run (self, order_id: str):
        
        # Step 1: PreparePackage
        await workflow.execute_activity(PreparePackage, order_id, schedule_to_close_timeout=timedelta(seconds=300))

        # Step 2: DispatchCarrier
        await workflow.execute_activity(DispatchCarrier, order_id, schedule_to_close_timeout=timedelta(seconds=300))

        

   
        

                   
      
