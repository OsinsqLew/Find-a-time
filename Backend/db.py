import mysql.connector
import random
import string
import hashlib
from datetime import datetime, timedelta, date

def generate_salt(length: int = 4):
    characters = string.ascii_letters + string.digits  # Litery i cyfry
    return ''.join(random.choice(characters) for _ in range(length))


class Readable_DB():
    def __init__(self, host, port, username, password, db_name):
        self.my_db = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=db_name,
            ssl_ca='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/slave/ca.crt',
            ssl_cert='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/slave/slave-mysql.crt',
            ssl_key='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/slave/slave-mysql.key',
            autocommit=True
            )
    def is_password_correct(self, name, password) -> bool:
        """Checks if hash of given password is equal to the hash in the database."""
        query = (
            f"SELECT salt, hash_pass FROM Users WHERE username = %s;"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (name,))
            result = cursor.fetchall()
            salt, password_hash = result[0] if result else ("", "")
            password = password + salt
            given_hash = hashlib.md5(password.encode('utf-8')).hexdigest().strip()

            return password_hash == given_hash
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def check_if_user_exists(self, name) -> bool:
        """Checks if user exists in the database."""
        query = (
            f"SELECT * FROM Users WHERE username = %s;"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query,(name,))
            user = cursor.fetchall()
            return bool(user)
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()


    def user_friendgroups(self, username: str) -> dict[int: str]:
        """Gets ids and names of all the user's friendgroups."""
        query = ( 
            f"WITH grupy AS (SELECT fgroup_id FROM FriendGroup_User WHERE username = '{username}') SELECT * FROM FriendGroup WHERE fgroup_id IN (SELECT fgroup_id FROM grupy);"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query)
            user_fg = {name: id for id, name in cursor}
        except Exception as e:
            print(e)
            user_fg = {}
        finally:
            cursor.close()
            return user_fg


    def get_freespots(self, fg_id, start_date, end_date=None):
        """Gets all free spots of the users in the friendgroup between the given dates."""
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        if end_date is None:
            end_date_datetime = start_date_datetime + timedelta(days=14)
            end_date = end_date_datetime.strftime('%Y-%m-%d')
        query = (
            f"WITH fg_users AS (SELECT username FROM FriendGroup_User WHERE fgroup_id = {fg_id}) SELECT username, `date`, start_time, end_time FROM Availability WHERE username IN (SELECT username FROM fg_users) AND `date` BETWEEN '{start_date}' AND '{end_date}';"
        )
        available_spots = {}
        i = start_date_datetime
        while i <= end_date_datetime:
            available_spots[str(i)[:10]] = {}
            i += timedelta(days=1)
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for spot in result:
                username, day, start, end = spot
                day_str = str(day)[:10]
                if username not in available_spots[day_str]:
                    available_spots[day_str][username] = []
                available_spots[day_str][username].append((str(start), str(end)))
            return available_spots
        except Exception as e:
            print(e)
            available_spots = {}
        finally:
            cursor.close()
            return available_spots
        
    def sql_injection(self, username: str):
        cursor = self.my_db.cursor()
        tmp = []
        query = f"SELECT * FROM users WHERE username = '{username}';"
        for result in cursor.execute(query, multi=True):
            if result.with_rows:
                for row in result.fetchall():
                    tmp.append(row)
        cursor.close()
        return tmp

class Writable_DB():
    def __init__(self, host, port, username, password, db_name):
        self.my_db = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=db_name,
            ssl_ca='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/master/ca.crt',
            ssl_cert='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/master/master-mysql.crt',
            ssl_key='C:/Users/natalcia/Desktop/PWr/Bazy Danych/projekt/Find-a-time/Backend/docker/certs/master/master-mysql.key',
            autocommit=True
            )
    def add_user(self, username, password, salt):
        """Adds a new user to the database."""
        query = (
            f"INSERT INTO users (username, hash_pass, salt) VALUES ('{username}', '{password}', '{salt}')"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query)
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()

    def add_friendgroup(self, fg_name, username):
        """Adds a new friend group to the database."""
        query1 = (
            f"INSERT INTO FriendGroup (name) VALUES (%s)"
        )
        query2 = (
            f"INSERT INTO FriendGroup_User (fgroup_id, username) VALUES (LAST_INSERT_ID(), '{username}')"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query1, (fg_name,))
            cursor.execute(query2)
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()

    def add_friendgroup_user(self, fg_id, username):
        """Adds a new user to the friend group."""
        query = (
            f"INSERT INTO FriendGroup_User (fgroup_id, username) VALUES ({fg_id}, %s)"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (username,))
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()

    def remove_friendgroup():
        pass
    
    def remove_a_friend():
        pass

    
    def add_freespot(self, username: str, day: str, start: str, end: str):
        """Adds a new free spot to the database."""
        query = (
            f"INSERT INTO Availability (username, `date`, start_time, end_time) VALUES ('{username}', '{day}', '{start}', '{end}');"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query)
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()

    def remove_a_spot(self, spot_id):
        """Removes a free spot from the database."""
        query = (
            "DELETE FROM Availability ",
            f"WHERE id = {spot_id}"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query)
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()



if __name__ == "__main__":
    db_write = Writable_DB("localhost", 3314, "root", "root", "projekt2")
    db_read = Readable_DB("localhost", 3315, "root", "root", "projekt2")
    result = db_read.sql_injection("test'; SELECT * FROM FriendGroup WHERE '1'='1")
    print(result)
    # db = Writable_DB("localhost", 3314, "root", "root", "projekt2")
    # result = db.add_friendgroup("grupa", "natalka")
