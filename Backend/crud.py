#from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connection import get_master_connection

#app = FastAPI()

def insert_friend_group(group_name, user_name):
    connection = get_master_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO FriendGroup (name) VALUES (%s)", (group_name))

        #cursor.execute("INSERT INTO Users (name) VALUES (%s)", (user_name))
        #user_id = cursor.lastrowid

        #cursor.execute("INSERT INTO FriendGroup_User (fgroup_id, user_id) VALUES (%s, %s)", (fgroup_id, user_id))

        connection.commit()
        return{"status": "success", "message": "Data inserted successfully"}
    
    except Exception as e:
        connection.rollback()
        return{"status": "error", "message": str(e)}
    
    finally:
        cursor.close()
        connection.close()


        