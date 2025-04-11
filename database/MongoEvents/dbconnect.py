from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient("")
        self.db = self.client['']  

    def get_db(self):
        return self.db

    def close(self):
        self.client.close()