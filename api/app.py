from typing import List, Optional
from datetime import datetime
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from big_python_library import main as my_library

app = FastAPI()

neural_net = my_library.SimpleNet()

# Pydantic model for Order


class Order(BaseModel):
    id: str
    customer_name: str
    order_items: List[str]
    total_amount: float
    status: str
    created_at: datetime


# In-memory storage for orders
orders_db = {}

# Create Order


@app.post("/orders/", response_model=Order)
async def create_order(customer_name: str, order_items: List[str], total_amount: float):
    order = Order(
        id=str(uuid.uuid4()),
        customer_name=customer_name,
        order_items=order_items,
        total_amount=total_amount,
        status="pending",
        created_at=datetime.now()
    )
    orders_db[order.id] = order
    return order

# Get all orders


@app.get("/orders/", response_model=List[Order])
async def get_orders():
    return list(orders_db.values())

# Get specific order


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

# Update order


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, status: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    order = orders_db[order_id]
    order.status = status
    return order

# Delete order


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders_db[order_id]
    return {"message": "Order deleted successfully"}
