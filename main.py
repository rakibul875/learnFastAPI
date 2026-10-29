from fastapi import FastAPI, HTTPException
from database import users_collection
from models import userClass, userClassUpdate
from bson import ObjectId

app = FastAPI()


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "age": user["age"],
        "status": user["status"]
    }


@app.get("/api/v1/users")
async def view_users():
    users = []
    cursor = users_collection.find({})
    async for document in cursor:
        users.append(user_helper(document))
    return {"users": users}


@app.get("/api/v1/users/{user_id}")
async def view_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user_helper(user)


@app.post("/api/v1/create/users")
async def create_user(user: userClass):
  
    existing_email = await users_collection.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
        
    user_data = user.model_dump()
    
 
    new_user = await users_collection.insert_one(user_data)
    
    return {
        "message": "User created successfully", 
        "id": str(new_user.inserted_id)
    }


@app.put("/api/v1/update/users/{user_id}")
async def update_user(user_id: str, user: userClassUpdate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    existing_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    update_data = user.model_dump(exclude_unset=True)
    
    if "email" in update_data:
        email_check = await users_collection.find_one({
            "email": update_data["email"], 
            "_id": {"$ne": ObjectId(user_id)}
        })
        if email_check:
            raise HTTPException(status_code=400, detail="Email already exists")
            
    if update_data:
        await users_collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
        
    return {"message": "User updated successfully", "id": user_id}


@app.delete("/api/v1/delete/users/{user_id}")
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {"message": "User deleted successfully", "id": user_id}