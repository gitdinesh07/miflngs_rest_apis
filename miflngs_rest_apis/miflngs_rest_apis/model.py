from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from django.http import JsonResponse

def db_con():
    try:
        global client
        client = MongoClient("localhost", 27017)
        db = client["mifeel"]
        return db
    except ConnectionFailure as e:
        return JsonResponse({"msg": "DB Connectino Fail", "msg_code": 81})
    except Exception as e:
        return JsonResponse({"msg": "DB Connectino Error", "msg_code": 100})
    finally:
        client.close()

