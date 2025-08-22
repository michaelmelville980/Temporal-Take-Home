print("🚀 CLI invoked successfully!") 
import argparse
import asyncio
import os
from temporalio.client import Client
from workflows.order_workflow import OrderWorkflow
from typing import Dict, Any, List


async def connect_client():
    host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    return await Client.connect(host)

async def start_order(order_id: str, payment_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):
    client = await connect_client()
    handle = await client.start_workflow(
        OrderWorkflow.run,
        args=[order_id, payment_id, items, address_json],
        id=f"order-{order_id}",
        task_queue="order-tq",
    )
    print(f"Started OrderWorkflow {handle.id}")

async def cancel_order(order_id: str):
    client = await connect_client()
    handle = client.get_workflow_handle(f"order-{order_id}")
    await handle.signal(OrderWorkflow.CancelOrder)
    print(f"Sent CancelOrder signal to workflow {order_id}")

async def update_address(order_id: str, address: dict):
    client = await connect_client()
    handle = client.get_workflow_handle(f"order-{order_id}")
    await handle.signal(OrderWorkflow.UpdateAddress, address)
    print(f"Sent UpdateAddress signal to workflow {order_id}")

async def status(order_id: str):
    client = await connect_client()
    handle = client.get_workflow_handle(f"order-{order_id}")
    status = await handle.query(OrderWorkflow.get_status) 
    print(f"Workflow {order_id} status: {status}")


def main():
    parser = argparse.ArgumentParser(prog="orders")
    sub = parser.add_subparsers(dest="command", required=True)

    # Start workflow
    s = sub.add_parser("start", help="Start a new order workflow")
    s.add_argument("order_id")
    s.add_argument("payment_id")
    s.add_argument("--items", required=True, help="JSON string for items")
    s.add_argument("--address", required=True, help="JSON string for address")

    # Cancel workflow
    c = sub.add_parser("cancel", help="Send CancelOrder signal to a workflow")
    c.add_argument("order_id")

    # Update address
    ua = sub.add_parser("update-address", help="Send UpdateAddress signal to a workflow")
    ua.add_argument("order_id")
    ua.add_argument("--address", required=True, help="JSON string for new address")

    # Status
    st = sub.add_parser("status", help="Query workflow status")
    st.add_argument("order_id")

    args = parser.parse_args()

    if args.command == "start":
        import json
        items = json.loads(args.items)
        address = json.loads(args.address)
        asyncio.run(start_order(args.order_id, args.payment_id, items, address))
    elif args.command == "cancel":
        asyncio.run(cancel_order(args.order_id))
    elif args.command == "update-address":
        import json
        address = json.loads(args.address)
        asyncio.run(update_address(args.order_id, address))
    elif args.command == "status":
        asyncio.run(status(args.order_id))

if __name__ == "__main__":
    main()
