from models.order import Order
from typing import Dict, List, Optional

# Simulated DynamoDB table using a Python dictionary
_order_store: Dict[str, Order] = {}

def save_order(order: Order) -> None:
    _order_store[order.id] = order

def get_order(order_id: str) -> Optional[Order]:
    return _order_store.get(order_id)

def list_orders() -> List[Order]:
    return list(_order_store.values())

def cancel_order(order_id: str) -> bool:
    if order_id in _order_store:
        _order_store[order_id].status = "cancelled"
        return True
    return False