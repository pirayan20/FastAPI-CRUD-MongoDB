from fastapi import APIRouter, HTTPException
from app.data_model import Product
from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["products"]
collection = db["products"]


@router.get("/products")
async def get_all_products():
    products = list(collection.find())
    return [
        {"id": str(product["_id"]), "name": product["name"], "price": product["price"]}
        for product in products
    ]


@router.post("/products")
async def create_product(product: Product):
    result = collection.insert_one(product.model_dump())
    return {"id": str(result.inserted_id), "name": product.name, "price": product.price}


@router.get("/products/{id}")
async def get_product_by_id(id: str):
    product = collection.find_one({"_id": ObjectId(id)})
    if product:
        return {
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
        }
    else:
        raise HTTPException(status_code=404, detail="id not found in product")


@router.put("/products/{id}")
async def update_product_by_id(id: str, product: Product):
    result = collection.update_one(
        {"_id": ObjectId(id)}, {"$set": product.model_dump(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return {"id": id, "name": product.name, "price": product.price}
    else:
        raise HTTPException(status_code=404, detail="id not found in product")


@router.delete("/products/{id}")
async def delete_product_by_id(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Delete Successfully"}
    else:
        raise HTTPException(status_code=404, detail="id not found in product")
