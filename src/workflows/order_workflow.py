from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, List
from activities.order_activities import ReceiveOrder, ValidateOrder, ChargePayment
from workflows.shipping_workflow import ShippingWorkflow

@workflow.defn
class OrderWorkflow:
    
    @workflow.run
    async def run (self, order_id: str, payment_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):

        # Step 1: ReceiveOrder
        await workflow.execute_activity(ReceiveOrder, order_id, items, schedule_to_close_timeout=timedelta(seconds=300))

        # Step 2: ValidateOrder
        await workflow.execute_activity(ValidateOrder, order_id, schedule_to_close_timeout=timedelta(seconds=300))

        # Step 3: Timer (SimulatedManual Review)
        await workflow.sleep(timedelta(milliseconds=100))

        # Step 4: ChargePayment
        await workflow.execute_activity(ChargePayment, order_id, payment_id, schedule_to_close_timeout=timedelta(seconds=300))

        # Step 5: ShippingWorkflow
        await workflow.execute_child_workflow(ShippingWorkflow.run, order_id, task_queue="shipping-tq")



   
        

                   
      
