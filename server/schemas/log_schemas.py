from pydantic import BaseModel

class AuthCreate(BaseModel):
    user_id: str
    email: str
    full_name: str

class UserAction(BaseModel):
    user_id: str
    action_type: str