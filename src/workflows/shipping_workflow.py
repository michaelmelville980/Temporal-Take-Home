from temporalio import workflow
from datetime import timedelta
from activities.shipping_activities import PreparePackage, DispatchCarrier
from typing import Dict, Any, List
import asyncio 

@workflow.defn
class ShippingWorkflow:
    @workflow.run
    async def run(self, order_id: str, parent_id: str):
        parent = workflow.get_external_workflow_handle(parent_id)
        
        # Step 1: PreparePackage
        try:
            await workflow.execute_activity(
                PreparePackage,
                args=[order_id],
                schedule_to_close_timeout=timedelta(seconds=300),
            )
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await parent.signal("dispatch_failed", "PreparePackage failed")
            raise

        # Step 2: DispatchCarrier
        try:
            await workflow.execute_activity(
                DispatchCarrier,
                args=[order_id],
                schedule_to_close_timeout=timedelta(seconds=300),
            )
            return "done"
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await parent.signal("dispatch_failed", "DispatchCarrier failed")
            raise
        
   
