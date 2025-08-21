import asyncio
from temporalio.client import Client
from workflows.order_workflow import OrderWorkflow

async def main():

    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        OrderWorkflow.run,
        "order-123",  # order_id
        id="order-123-workflow",
        task_queue="order_tq"
    )
    
    result = await handle.result()
    print("Workflow result:", result)

if __name__ == "__main__":
    asyncio.run(main())
