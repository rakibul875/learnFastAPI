from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated
import json


class userClass(BaseModel):
    id: Annotated[str, Field(...,description="User ID", example="123") ]
    name: Annotated[str, Field(...,description="User Name", example="Jon Doe") ]
    email: Annotated[str, Field(...,description="User Email", example="johndoe@example.com") ]
    role:Annotated[str, Field(...,description="User Role",example="user")]
    age: Annotated[int,Field(...,description="User Age",example=30)]
    status:Annotated[str,Field(...,description="User Status",example="active")]



app= FastAPI()

def load_users():
    with open("user.json",'r')as f:
            data=json.load(f)
    return{"users": data}

def save_users(users):
    with open('user.json','w')as f:
        json.dump(users,f)


@app.get("/")
def view():
    return {"message": "Hello, World!"}
@app.get("/items")
def view_items():
    return {"items": ["item1", "item2", "item3"]}

@app.get("/api/v1/users")
def view_users():
    return load_users()
@app.get("/api/v1/users/{user_id}")
def view_users(user_id: str):
    user=load_users()
    users_dict = user["users"]
    
    if user_id not in users_dict:
        raise HTTPException(status_code =404, detail="User not found")

    return users_dict[user_id]

@app.get("/api/v1/sort")
def sort_users(sorted_by:str,age:str):
    user= load_users()
    users_dict=user['users']
    sorted_users=list(users_dict.values())
    def valid_sort_keys(key):
        return key[sorted_by]
    if age == 'asc':
        
        sorted_users.sort(key=valid_sort_keys)
    else:
        sorted_users.sort(key=valid_sort_keys, reverse=True)
    return {"sorted_users": sorted_users}


@app.post("/api/v1/users")
def create_user(user: userClass):
    users=load_users()
    users[user.id]=user.model_dump(exclude=['id'])
    save_users(users)