import boto3
from models.order import Order
from typing import Optional, List

# Connect to DynamoDB using the AWS credentials configured via `aws configure`
dynamodb = boto3.resource("dynamodb")

# Reference the 'Orders' orders_table by name
orders_table = dynamodb.Table("Orders")

def save_order(order: Order) -> None:
    orders_table.put_item(Item=order.model_dump())

def get_order(order_id: str) -> Optional[Order]:
    response = orders_table.get_item(Key={"id": order_id})
    item = response.get("Item")
    return Order(**item) if item else None

def list_orders() -> List[Order]:
    response = orders_table.scan()
    items = response.get("Items", [])
    return [Order(**item) for item in items]

def cancel_order(order_id: str) -> bool:
    # Get existing order
    existing = get_order(order_id)
    if not existing:
        return False
    existing.status = "cancelled"
    save_order(existing)
    return True