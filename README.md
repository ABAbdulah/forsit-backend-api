# 🛒 Forsit E-commerce Admin API

A backend API for managing products, sales analytics, and inventory for an e-commerce admin dashboard.

---

## 🚀 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: MongoDB (Cloud - MongoDB Atlas)
- **API Style**: RESTful
- **ORM/Driver**: Motor (async MongoDB client)

---

## 📦 Features

- ✅ Product Management (CRUD)
- 📊 Sales Tracking & Revenue Summary (daily, weekly, monthly, yearly)
- 📈 Sales Filtering by Date, Product, Category
- 📦 Inventory Management with Low Stock Alerts
- 📝 Inventory Change Logs
- 🧪 Demo Data Seed Script
- 📚 Swagger API Documentation

---

## 🛠 Setup Instructions

1. **Clone the repo** and create a virtual environment:

```bash
git clone https://github.com/ABAbdulah/forsit-backend-api
cd forsit-backend-api

python -m venv venv
# On Windows:
.\venv\Scripts\activate
Now run this command in root folder:  uvicorn app.main:app --reload    
pip install -r requirements.txt
