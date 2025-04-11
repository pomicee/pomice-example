from .dbconnect import Database

def close_database():
    db = Database()
    db.close()
    print("Database connection closed.")
