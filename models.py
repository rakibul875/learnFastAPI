from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

class userClass(BaseModel):
  
    name: Annotated[str, Field(..., description="User Name", example="Jon Doe")]
    email: Annotated[EmailStr, Field(..., description="User Email", example="johndoe@example.com")]
    role: Annotated[str, Field(..., description="User Role", example="user")]
    age: Annotated[int, Field(..., description="User Age", example=30)]
    status: Annotated[str, Field(..., description="User Status", example="active")]

class userClassUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, example="Jon Doe")]
    email: Annotated[Optional[EmailStr], Field(default=None, example="johndoe@example.com")]
    role: Annotated[Optional[str], Field(default=None, example="user")]
    age: Annotated[Optional[int], Field(default=None, example=30)]
    status: Annotated[Optional[str], Field(default=None, example="active")]