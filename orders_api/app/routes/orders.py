# orders_api/app/routes/orders.py
from fastapi import APIRouter, Query
from services.order_service import OrderService
from models.order import Order, OrderCreate, PaginatedOrders
from typing import Optional
from fastapi import Depends
from auth.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["Orders"])

# Create a new order
@router.post("/create", response_model=Order)
def create_order(order_data: OrderCreate, user_id: str = Depends(get_current_user)):
    print(f"POST /orders by user: {user_id} | data: {order_data}")
    return OrderService.create_order(order_data)

# Get a list of all orders
@router.get("/", response_model=PaginatedOrders)
def list_orders(
    limit: int = Query(10, ge=1, le=100),  # limit must be 1 ≤ limit ≤ 100
    start_key: Optional[str] = None,
    user_id: str = Depends(get_current_user)
):
    logger.info(f"GET /orders by user: {user_id} | limit={limit} | start_key={start_key}")
    return OrderService.list_orders(limit=limit, start_key=start_key)

# Get a specific order by ID
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str, user_id: str = Depends(get_current_user)):
    logger.info(f"GET /orders/{order_id} by user: {user_id}")
    return OrderService.get_order(order_id)

# Cancel (delete) an order by ID
@router.delete("/{order_id}")
def cancel_order(order_id: str, user_id: str = Depends(get_current_user)):
    logger.info(f"DELETE /orders/{order_id} by user: {user_id}")
    OrderService.cancel_order(order_id)
    return {"message": "Order cancelled"}