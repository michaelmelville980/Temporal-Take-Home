from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, List
from activities.order_activities import ReceiveOrder, ValidateOrder, ChargePayment
from activities.signal_activities import CancelOrder, UpdateAddress
from workflows.shipping_workflow import ShippingWorkflow

@workflow.defn
class OrderWorkflow:

    def __init__ (self):
        self.newAddress = None
        self.cancelOrder = False

    @workflow.signal
    def UpdateAddress(self, address: Dict[str, Any]):
        self.newAddress=address

    @workflow.signal
    def CancelOrder(self):
        self.cancelOrder=True

    async def apply_signals(self, order_id: str):
        if self.cancelOrder:
            await workflow.execute_activity(CancelOrder, order_id, schedule_to_close_timeout=timedelta(seconds=300))
            return {"order_id": order_id, "status": "cancelled"}
        if self.newAddress is not None:
            address = self.newAddress
            self.newAddress = None
            await workflow.execute_activity(UpdateAddress, order_id, address, schedule_to_close_timeout=timedelta(seconds=300))
        return None

    @workflow.run
    async def run (self, order_id: str, payment_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):

        # Checks for signals
        appliedSignal = await self.apply_signals(order_id)
        if appliedSignal: 
            return appliedSignal

        # Step 1: ReceiveOrder
        await workflow.execute_activity(ReceiveOrder, order_id, items, schedule_to_close_timeout=timedelta(seconds=300))

        # Checks for signals
        appliedSignal = await self.apply_signals(order_id)
        if appliedSignal: 
            return appliedSignal

        # Step 2: ValidateOrder
        await workflow.execute_activity(ValidateOrder, order_id, schedule_to_close_timeout=timedelta(seconds=300))

        # Checks for signals
        appliedSignal = await self.apply_signals(order_id)
        if appliedSignal: 
            return appliedSignal

        # Step 3: Timer (SimulatedManual Review)
        await workflow.sleep(timedelta(milliseconds=100))

        # Checks for signals
        appliedSignal = await self.apply_signals(order_id)
        if appliedSignal: 
            return appliedSignal

        # Step 4: ChargePayment
        await workflow.execute_activity(ChargePayment, order_id, payment_id, schedule_to_close_timeout=timedelta(seconds=300))

        # Checks for signals
        appliedSignal = await self.apply_signals(order_id)
        if appliedSignal: 
            return appliedSignal

        # Step 5: Child ShippingWorkflow
        await workflow.execute_child_workflow(ShippingWorkflow.run, order_id, task_queue="shipping-tq")

        # Return
        return {"order_id": order_id, "status": "completed"}



   
        

                   
      
