from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from bson import ObjectId
from app.models.sale import Sale, SaleCreate
from app.database import db

router = APIRouter()
collection = db["sales"]
products_collection = db["products"]

# Record a sale
@router.post("/", response_model=Sale)
async def create_sale(sale: SaleCreate):
    # Validate product exists
    product = await products_collection.find_one({"_id": ObjectId(sale.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    result = await collection.insert_one(sale.dict())
    new_sale = await collection.find_one({"_id": result.inserted_id})
    new_sale["_id"] = str(new_sale["_id"])
    return Sale(**new_sale)

# Get sales (filterable)
@router.get("/", response_model=list[Sale])
async def get_sales(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    product_id: str = Query(None)
):
    query = {}
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    if product_id:
        query["product_id"] = product_id

    sales = await collection.find(query).to_list(100)
    for sale in sales:
        sale["_id"] = str(sale["_id"])
    return [Sale(**s) for s in sales]

# Get revenue summary
@router.get("/summary")
async def get_revenue_summary():
    now = datetime.utcnow()

    async def revenue_in_range(start, end):
        pipeline = [
            {"$match": {"date": {"$gte": start, "$lte": end}}},
            {"$group": {"_id": None, "revenue": {"$sum": "$total_price"}}}
        ]
        result = await collection.aggregate(pipeline).to_list(1)
        return result[0]["revenue"] if result else 0

    return {
        "daily": await revenue_in_range(now - timedelta(days=1), now),
        "weekly": await revenue_in_range(now - timedelta(weeks=1), now),
        "monthly": await revenue_in_range(now - timedelta(days=30), now),
        "yearly": await revenue_in_range(now - timedelta(days=365), now),
    }
