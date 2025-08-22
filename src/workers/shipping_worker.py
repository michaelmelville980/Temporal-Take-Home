import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.order_workflow import OrderWorkflow
from activities.shipping_activities import PreparePackage, DispatchCarrier

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="shipping-tq",
        workflows=[OrderWorkflow],
        activities=[PreparePackage, DispatchCarrier]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
