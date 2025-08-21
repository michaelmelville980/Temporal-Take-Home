import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.order_workflow import OrderWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="shipping-tq",
        workflows=[OrderWorkflow],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())