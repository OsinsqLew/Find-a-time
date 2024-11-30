from pydantic import BaseModel
from datetime import date, time

class FriendGroup(BaseModel):
    fgroup_id: int
    name: str

class Users(BaseModel):
    user_id: int
    username: str
    hash_pass: str

class FriendGroup_User(BaseModel):
    fgroup_id: int
    user_id: int

class Availability(BaseModel):
    avail_id: int
    user_id: int
    'date': date
    start_time: time
    end_time: time