from fastapi import FastAPI
from app.routers import products, sales, inventory

app = FastAPI(title="Forsit Admin API")

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

@app.get("/")
async def root():
    return {"message": "Forsit E-commerce Admin API is running"}
