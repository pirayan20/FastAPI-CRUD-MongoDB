from fastapi import APIRouter, HTTPException
from app.data_model import Vote
from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["votes"]
collection = db["votes"]


@router.post("/votes")
async def create_vote(vote: Vote):
    result = collection.insert_one(vote.model_dump())
    return {"id": str(result.inserted_id), "name": vote.name, "count": vote.count}


@router.get("/votes/{id}")
async def get_vote_by_id(id: str):
    vote = collection.find_one({"_id": ObjectId(id)})
    if vote:
        return {"id": str(vote["_id"]), "name": vote["name"], "count": vote["count"]}
    else:
        raise HTTPException(status_code=404, detail="id not found in vote")


@router.put("/votes/{id}")
async def update_vote_by_id(id: str, vote: Vote):
    result = collection.update_one(
        {"_id": ObjectId(id)}, {"$set": vote.model_dump(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return {"id": id, "name": vote.name, "count": vote.count}
    else:
        raise HTTPException(status_code=404, detail="id not found in vote")


@router.delete("/votes/{id}")
async def delete_vote_by_id(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Delete Successfully"}
    else:
        HTTPException(status_code=404, detail="id not found in vote")
