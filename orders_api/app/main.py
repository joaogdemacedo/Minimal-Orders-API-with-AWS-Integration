from fastapi import FastAPI
from app.routes import orders, auth
import logging

logging.basicConfig(
    level=logging.INFO,  # Show INFO, WARNING, ERROR, etc.
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI(
    title="Orders API",
    version="1.0",
    description="A backend API to manage orders with JWT auth",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Orders API! Try /docs for the Swagger UI."}

# Include routes
app.include_router(auth.router)
app.include_router(orders.router)