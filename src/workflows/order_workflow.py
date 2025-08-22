from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, List
from activities.order_activities import ReceiveOrder, ValidateOrder, ChargePayment
from activities.signal_activities import CancelOrder, UpdateAddress
from temporalio.common import RetryPolicy
import asyncio

@workflow.defn
class OrderWorkflow:
    def __init__(self):
        self.status = None
        self.newAddress = None
        self.cancelOrder = False
        self.dispatchFailed = False
        self.dispatchReason = None

    @workflow.query
    def get_status(self):
        return self.status

    @workflow.signal
    def dispatch_failed(self, reason: str):
        self.dispatchFailed = True
        self.dispatchReason = reason

    @workflow.signal
    def UpdateAddress(self, address: Dict[str, Any]):
        self.newAddress = address

    @workflow.signal
    def CancelOrder(self):
        self.cancelOrder = True

    async def apply_signals(self, order_id: str, payment_id: str, address: Dict[str, Any]):
        if self.cancelOrder:
            await workflow.execute_activity(
                CancelOrder,
                args=[order_id, payment_id],
                start_to_close_timeout=timedelta(milliseconds=75),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=1),  
                    backoff_coefficient=1.0,                     
                    maximum_attempts=10,
                ),
            )
            self.status = "cancelled"
            return {"order_id": order_id, "status": "cancelled"}

        if self.newAddress is not None:
            address = self.newAddress
            self.newAddress = None
            await workflow.execute_activity(
                UpdateAddress,
                args=[order_id, address],
                start_to_close_timeout=timedelta(milliseconds=75),
                 retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=1),  
                    backoff_coefficient=1.0,                     
                    maximum_attempts=10,
                ),
            )
        return None

    @workflow.run
    async def run(self, order_id: str, payment_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):
        # Pre-signal check
        applied = await self.apply_signals(order_id, payment_id, address_json)
        if applied:
            return applied

        # 1) Receive order
        await workflow.execute_activity(
            ReceiveOrder,
            args=[order_id, items, address_json],
            start_to_close_timeout=timedelta(milliseconds=135),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(milliseconds=1),  
                backoff_coefficient=2.0,            
                maximum_attempts=10,          
            ),
        )
        self.status = "Order Received"

        applied = await self.apply_signals(order_id, payment_id, address_json)
        if applied:
            return applied

        # 2) Validate order
        await workflow.execute_activity(
            ValidateOrder,
            args=[order_id],
            start_to_close_timeout=timedelta(milliseconds=75),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(milliseconds=1),  
                backoff_coefficient=1.0,                     
                maximum_attempts=10,
            ),
        )
        self.status = "Order Validated"

        applied = await self.apply_signals(order_id, payment_id, address_json)
        if applied:
            return applied

        # 3) Simulated manual review
        await workflow.sleep(timedelta(milliseconds=50))
        self.status = "Manual Review"

        applied = await self.apply_signals(order_id, payment_id, address_json)
        if applied:
            return applied

        # 4) Charge payment
        await workflow.execute_activity(
            ChargePayment,
            args=[order_id, payment_id],
            start_to_close_timeout=timedelta(milliseconds=75),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(milliseconds=1),  
                backoff_coefficient=1.0,                     
                maximum_attempts=10,
            ),
        )
        self.status = "Payment Charged"

        applied = await self.apply_signals(order_id, payment_id, address_json)
        if applied:
            return applied

        # 5) Child ShippingWorkflow
        parent_id = workflow.info().workflow_id

        i = 0
        while True:
            i += 1
            child = await workflow.start_child_workflow(
                "ShippingWorkflow",
                args=[order_id, parent_id],
                id=f"ship-{order_id}-{i}",
                task_queue="shipping-tq",
            )
            await workflow.wait_condition(lambda: self.dispatchFailed or child.done())

            if self.dispatchFailed:
                self.dispatchFailed = False
                try:
                    await child.cancel()
                    await child.result()   
                except Exception:
                    pass
                continue

            try:
                result = await child.result()
                self.status = "Shipping Completed"
                return {"order_id": order_id, "status": "shipped"}
            except Exception as e:
                raise
