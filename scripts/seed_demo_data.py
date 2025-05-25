import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "forsitDB"

products = [
    {"name": "iPhone 15", "category": "Electronics", "price": 999.99, "stock": 50},
    {"name": "Samsung TV", "category": "Electronics", "price": 599.99, "stock": 30},
    {"name": "Nike Sneakers", "category": "Fashion", "price": 120.00, "stock": 100},
    {"name": "Kitchen Knife Set", "category": "Home", "price": 49.99, "stock": 75},
    {"name": "Protein Powder", "category": "Health", "price": 29.99, "stock": 60}
]

async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # Drop old data
    await db.products.delete_many({})
    await db.sales.delete_many({})
    await db.inventory_logs.delete_many({})

    # Insert products
    result = await db.products.insert_many(products)
    product_ids = result.inserted_ids

    # Insert sales
    for _ in range(50):  # 50 sales records
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 5)
        total_price = quantity * random.uniform(20, 100)
        days_ago = random.randint(0, 365)

        sale = {
            "product_id": str(product_id),
            "quantity": quantity,
            "total_price": round(total_price, 2),
            "date": datetime.utcnow() - timedelta(days=days_ago)
        }
        await db.sales.insert_one(sale)

    print("Demo data inserted.")

asyncio.run(seed())
