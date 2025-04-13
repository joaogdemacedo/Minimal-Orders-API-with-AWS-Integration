from models.order import Order, OrderCreate
from db import dynamo as db
import base64
import json
from exceptions import InvalidStartKeyException, OrderNotFoundException
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @staticmethod
    def create_order(order_data: OrderCreate) -> Order:
        logger.info(f"Creating order for user: {order_data.userId}")
        order = Order(**order_data.model_dump())
        db.save_order(order)
        logger.info(f"Order created with ID: {order.id}")
        return order

    @staticmethod
    def get_order(order_id: str) -> Order | None:
        logger.info(f"Retrieving order ID: {order_id}")
        order = db.get_order(order_id)
        if not order:
            logger.warning(f"Order not found: {order_id}")
            raise OrderNotFoundException()
        logger.info(f"Order found: {order_id}")
        return order

    @staticmethod
    def list_orders(limit: int = 10, start_key: str = None):
        logger.info(f"Listing orders with limit={limit} start_key={start_key}")
        scan_kwargs = {
            "Limit": limit
        }

        # Decode start_key if provided
        if start_key:
            try:
                decoded = base64.b64decode(start_key).decode("utf-8")
                decoded_key = json.loads(decoded)
                scan_kwargs["ExclusiveStartKey"] = decoded_key
                logger.info(f"Decoded start_key: {decoded_key}")
            except Exception as e:
                logger.warning(f"Invalid start_key provided: {start_key} | Error: {e}")
                raise InvalidStartKeyException()

        response = db.orders_table.scan(**scan_kwargs)
        orders = [Order(**item) for item in response.get("Items", [])]
        logger.info(f"Retrieved {len(orders)} orders")

        # Encode LastEvaluatedKey for the client to use as next_key
        last_evaluated_key = response.get("LastEvaluatedKey")
        encoded_key = (
            base64.b64encode(json.dumps(last_evaluated_key).encode("utf-8")).decode("utf-8")
            if last_evaluated_key else None
        )

        return {
            "items": orders,
            "next_key": encoded_key
        }

    @staticmethod
    def cancel_order(order_id: str) -> None:
        logger.info(f"Cancelling order ID: {order_id}")
        success = db.cancel_order(order_id)
        if not success:
            logger.warning(f"Cancel failed: order not found {order_id}")
            raise OrderNotFoundException()
        logger.info(f"Order cancelled: {order_id}")