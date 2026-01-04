from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client=AsyncIOMotorClient(MONGO_URI)
db=client["Mongodbtest"]
coll=db["Mongodata"]

app=FastAPI()

class StudentData(BaseModel):
    id:int
    name:str
    age:int
    place:str

@app.post("/insert_mongodb")
async def insert_data_Mongo_helper(data:StudentData):
    result=await coll.insert_one(data.dict())
    return {
        "message": "Data inserted successfully",
        "mongo_id": str(result.inserted_id)
    }

def mongo_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/display_mongodb")
async def diplay_mongo_data():
    items=[]
    cursor=coll.find({})
    async for document in cursor:
        items.append(mongo_helper(document))
    return items

def mongo_helper2(doc):
    result = {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "age": doc.get("age")
    }
    if "place" in doc:
        result["place"] = doc["place"]

    if "zipcode" in doc:
        result["zipcode"] = doc["zipcode"]

    if "city" in doc:
        result["city"] = doc["city"]
    return result



@app.get("/display_mongodb_helper2")
async def diplay_mongo_data():
    items=[]
    cursor=coll.find({})
    async for document in cursor:
        items.append(mongo_helper2(document))
    return items