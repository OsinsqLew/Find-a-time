import mysql.connector
from mysql.connector import Error

def get_master_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3310,
            user='mirror_user',
            password='mirror_root',
            database='projekt'
        )

        if connection.is_connected():
            print('Connection to master database - ok.')
        return connection

    except Error as e:
        print(f'Failed to obtain connection to master database: {e}.')
        return None

def get_slave_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3311,
            user='mirror_user',
            password='mirror_root',
            database='projekt'
        )

        if connection.is_connected():
            print('Connection to slave database - ok.')
        return connection

    except Error as e:
        print(f'Failed to obtain connection to slave database: {e}.')
        return None