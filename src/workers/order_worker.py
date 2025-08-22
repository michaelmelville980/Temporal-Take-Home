import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.order_workflow import OrderWorkflow
from activities.order_activities import ReceiveOrder, ValidateOrder, ChargePayment
from activities.signal_activities import CancelOrder, UpdateAddress

async def main():

    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="order-tq",
        workflows=[OrderWorkflow],
        activities=[ReceiveOrder, ValidateOrder, ChargePayment, CancelOrder, UpdateAddress],
        max_concurrent_activities=50,
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())