# fastapi dev API.py
from fastapi import FastAPI, HTTPException
import Backend.db as db
from pydantic import BaseModel
import hashlib
from datetime import date, time
from typing import Optional

app = FastAPI()


db_write = db.Writable_DB("localhost", 3314, "mirror_user", "mirror_password", "projekt2")
db_read = db.Readable_DB("localhost", 3315, "mirror_user", "mirror_root", "projekt2")
# db_read = db.Readable_DB("localhost", 3314, "mirror_user", "mirror_password", "projekt2")



class User(BaseModel):
    username: str
    password: str

class FriendGroup(BaseModel):
    # model_config = {"extra": "forbid"} # * This will prevent the user from sending extra data
    group_name: str
    username: str

class Member(BaseModel):
    fg_id: int
    username: str

class postFreeSpot(BaseModel):
    username: str
    day: str
    start: str
    end: str

class getFreeSpot(BaseModel):
    fg_id: int
    start_day: str
    end_day: Optional[str] = None

@app.post("/register_user/")
def register_user(user: User):
    salt = db.generate_salt()
    user.password = user.password + salt
    hash = hashlib.md5(user.password.encode('utf-8')).hexdigest().strip()
    try:
        db_write.add_user(user.username, hash, salt)
        return {"message": "User created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating user: " + str(e))
    
@app.post("/login_user/")
def login_user(user: User):
    try:
        logged = db_read.is_password_correct(user.username, user.password)
        if logged:
            return {"logged": True}
        else:
            return {"logged": False}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error logging in user: " + str(e))

@app.get("/user_friendgroups/{username}")
def get_user_friendgroups(username: str):
    try:
        return {"friend_groups": db_read.user_friendgroups(username)}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error getting groups: " + str(e))

@app.post("/add_user_to_group/")
def add_user_to_group(member: Member):
    try:
        if db_read.check_if_user_exists(member.username):
            db_write.add_friendgroup_user(member.fg_id, member.username)
            return {"message": "User added to group successfully!"}
        else:
            return {"message": "User does not exist!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error adding user to group: " + str(e))

@app.post("/create_group/")
def create_group(fg: FriendGroup):
    try:
        db_write.add_friendgroup(fg.group_name, fg.username)
        return {"message": f"Group '{fg.group_name}' created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating group: " + str(e))

@app.post("/add_freespot/")
def add_freespot(freespot: postFreeSpot):
    try:
        db_write.add_freespot(freespot.username, freespot.day, freespot.start, freespot.end)
        return {"message": "Free spot added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error adding free spot: " + str(e))

@app.post("/find_time/")
def get_freespots(fg: getFreeSpot):
    try:
        if fg.end_day:
            return {"freespots": db_read.get_freespots(fg.fg_id, fg.start_day, fg.end_day)}
        else:
            return {"freespots": db_read.get_freespots(fg.fg_id, fg.start_day)}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error getting free spots: " + str(e))
    

@app.get("/sql_injection/{name}")
def search_user(name: str):
    try:
        result = db_read.sql_injection(name)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error getting user info: " + str(e))
    return {"users": result}

