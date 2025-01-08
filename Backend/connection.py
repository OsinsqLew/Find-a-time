import mysql.connector
from mysql.connector import Error

def get_master_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3314,
            user='mirror_user',
            password='mirror_password',
            database='projekt2',
            ssl_ca='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/master/ca.crt',
            ssl_cert='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/master/master-mysql.crt',
            ssl_key='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/master/master-mysql.key'
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
            port=3315,
            user='mirror_user',
            password='mirror_password',
            database='projekt2',
            ssl_ca='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/slave/ca.crt',
            ssl_cert='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/slave/slave-mysql.crt',
            ssl_key='C:/Users/lenovo/Documents/Semestr_V/Bazy Danych/friends_app/Find-a-time/find-time/certs/slave/slave-mysql.key'
        )

        if connection.is_connected():
            print('Connection to slave database - ok.')
        return connection

    except Error as e:
        print(f'Failed to obtain connection to slave database: {e}.')
        return None
    