import mysql.connector

class Database:
    def __init__(self, host, port, username, password, db_name):
        self.my_db = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=db_name
            )

    # def create_tables(self, file):
    #     self.cursor = self.my_db.cursor()
    #     create_commands = ''.join(file.readlines()).split('\n\n')
    #     for table in create_commands:
    #         try:
    #             self.cursor.execute(table)
    #         except mysql.connector.errors.ProgrammingError:
    #             continue

class Readable_DB(Database):
    def user_friendgroups(self, user_id: int) -> dict[int: str]:
        """Gets ids and names of all the user's friendgroups."""
        query = (
            f"WITH grupy AS ("
            f"    SELECT fgroup_id "
            f"    FROM FriendGroup_User "
            f"    WHERE user_id = {user_id})"
            f"SELECT * FROM FriendGroup "
            f"WHERE fgroup_id IN (SELECT fgroup_id FROM grupy)"
        )

        cursor = self.my_db.cursor()
        cursor.execute(query)
        user_fg = {id: name for id, name in cursor}
        return user_fg

    def people_in_friendgroup(self, friendgroup_id):
        pass

    def get_password_hash(self, name):
        pass

class Writable_DB(Database):
    def add_user():
        pass

    def add_friendgroup():
        pass

    def remove_friendgroup():
        pass

    def add_a_friend():
        pass
    
    def remove_a_friend():
        pass

    def add_free_spot():
        pass

    def remove_a_spot():
        pass



if __name__ == "__main__":
    db = Readable_DB("127.0.0.1", 3306, "user", "user", "test")
    result = db.user_friendgroups(1)
    print(result)