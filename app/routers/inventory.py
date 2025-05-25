from fastapi import APIRouter, HTTPException
from app.database import db
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()
products_collection = db["products"]
logs_collection = db["inventory_logs"]

# 1. Get inventory status with low stock alerts
@router.get("/")
async def get_inventory():
    products = await products_collection.find().to_list(100)
    result = []
    for product in products:
        product["_id"] = str(product["_id"])
        product["low_stock"] = product["stock"] < 10  # You can adjust this threshold
        result.append(product)
    return result

# 2. Update inventory and log changes
@router.put("/{product_id}")
async def update_inventory(product_id: str, quantity: int):
    try:
        obj_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await products_collection.find_one({"_id": obj_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    change = quantity - product["stock"]

    await products_collection.update_one(
        {"_id": obj_id},
        {"$set": {"stock": quantity}}
    )

    # Log inventory change
    await logs_collection.insert_one({
        "product_id": product_id,
        "quantity_changed": change,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Inventory updated", "new_stock": quantity}

# 3. View inventory change logs
@router.get("/logs/{product_id}")
async def get_inventory_logs(product_id: str):
    logs = await logs_collection.find({"product_id": product_id}).to_list(100)
    for log in logs:
        log["_id"] = str(log["_id"])
    return logs
