from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.errors import ConnectionFailure
from django.http import JsonResponse


class database_conn:

    def __init__(self):
        self.client = None

    def __enter__(self):
        try:
            # client = MongoClient("localhost", 27017)
            # db = self.client["mifeel"]
            maxSevSelDelay = 500
            self.client = MongoClient("mongodb://localhost:27017/mifeel", serverSelectionTimeoutMS=maxSevSelDelay)
            if self.client.server_info():
                return self.client.get_database()
        except PyMongoError as e:
            raise Exception({"msg": "DB Connection Error", "msg_code": 81, "msg_dec": e})
        except Exception as e:
            raise Exception({"msg": "Parent Error at DB Connection", "msg_dec": e})

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
