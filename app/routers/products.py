from fastapi import APIRouter, HTTPException
from app.models.product import Product, ProductCreate
from app.database import db
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Path
router = APIRouter()

collection = db["products"]

# Add a new product
@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    result = await collection.insert_one(product.dict())
    created_product = await collection.find_one({"_id": result.inserted_id})
    return Product(**created_product)

# Get all products
@router.get("/", response_model=list[Product])
async def get_products():
    products = await collection.find().to_list(100)
    return [Product(**prod) for prod in products]



@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        obj_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await collection.find_one({"_id": obj_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert ObjectId to str so Pydantic can handle it
    product["_id"] = str(product["_id"])
    return Product(**product)



# Update a product
@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    result = await collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": product.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or not modified")
    updated = await collection.find_one({"_id": ObjectId(product_id)})
    return Product(**updated)

# Delete a product
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    result = await collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
