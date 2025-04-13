from pydantic import BaseModel, Field, conint, constr
from typing import Annotated, List, Optional
from uuid import uuid4
from datetime import datetime, timezone

# Define constraints as annotations
PositiveInt = Annotated[int, conint(gt=0)]

# Represents a single item in an order
class OrderItem(BaseModel):
    productId: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$"
    ) # ID of the product being ordered
    quantity: PositiveInt   # Number of units ordered

# Request body schema for creating a new order
class OrderCreate(BaseModel):
    userId: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$"
    )                # ID of the user placing the order
    items: List[OrderItem]      # List of products in the order

# Full Order model used internally and in responses
class Order(OrderCreate):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Unique order ID
    status: str = "created"                                # Order status (default: "created")
    createdAt: str = Field(                                 
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )  # Timestamp in ISO format with timezone (UTC)
    
class PaginatedOrders(BaseModel):
    items: List[Order]
    next_key: Optional[str] = None  # Encoded cursor for the next page