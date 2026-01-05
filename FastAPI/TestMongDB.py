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

class UpdateDetails(BaseModel):
    id:int
 

@app.post("/update_mongodb")
async def update_data_Mongo_helper(upd:UpdateDetails):
    result=await coll.update_one(
        {"id":upd.id},
        {"$set":{"name":"Name Updated","age":99}}
    )

    if result.modified_count==0:
        return {"message":"nothing to modify"}
    
    if result.matched_count ==0:
        return {"message":"no id found"}
    


    return {
        "message": "Data updated successfully",
        
    }

class UpdateNamePlace(BaseModel):
    id:int
    name:str
    age:int
    place:str
    zipcode:str
 

@app.post("/update_parameter_mongodb")
async def update_data_Mongo_helper(updm:UpdateNamePlace):
    result=await coll.update_one(
        {"id":updm.id},
        {"$set":{"name":updm.name,"age":updm.age,"place":updm.place,"zipcode":updm.zipcode}}
    )

    if result.modified_count==0:
        return {"message":"nothing to modify"}
    
    if result.matched_count ==0:
        return {"message":"no id found"}
    


    return {
        "message": "Data updated successfully",
        
    }

class DeleteDetails(BaseModel):
    id:int
 

@app.post("/delete_mongodb")
async def update_data_Mongo_helper(dele:DeleteDetails):
    result=await coll.delete_one({"id":dele.id})

    if result.deleted_count==0:
        return {"message":"nothing to delete"}
    
    return {
        "message": "Data deleted successfully",
        
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
async def diplay_mongo_data2():
    items=[]
    cursor=coll.find({})
    async for document in cursor:
        items.append(mongo_helper2(document))
    return items

@app.get("/debug_env")
def debug_env():
    uri = os.getenv("MONGO_URI") or ""
    return {
        "has_mongo_uri": bool(uri),
        "starts_with_mongodb": uri.startswith("mongodb"),
        "contains_srv": "mongodb+srv://" in uri,
        "length": len(uri),
        "first_20": uri[:20],   # safe prefix only
        "last_10": uri[-10:]    # safe suffix only
    }