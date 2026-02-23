import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="muhammad-hamza-khalid",
        password="hamza000",
        database="password_security"
    )