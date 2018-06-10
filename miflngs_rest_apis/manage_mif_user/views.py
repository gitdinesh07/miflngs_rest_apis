from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from datetime import datetime
from pymongo.errors import ConnectionFailure
from pymongo.errors import DuplicateKeyError
from pymongo.errors import InvalidId
from pymongo.errors import InvalidStringData
from pymongo import MongoClient
import json
from rest_framework.views import APIView
from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import sys


def default_page(request):
    return  HttpResponse("<h1>hello welcome </h1>");
    # return render(request, "welcome.html", {"Welcome": str(u_name)})

def if_error(err_msg,err_code):
    return  JsonResponse({"msg": str(err_msg), "msgcode": int(err_code)})

client = object
def db_con():
    try:
        global client
        client = MongoClient("localhost", 27017)
        db = client["mifeel"]
        return db
    except ConnectionFailure as e:
        return JsonResponse({"msg": "DB Connectino Fail", "msgcode": 81})
    except Exception as e:
        return JsonResponse({"msg": "DB Connectino Error", "msgcode": 100})
    finally:
        client.close()


class MiUserList(APIView):
    # for user login get method
    def get(self, request, user_id,user_pswrd):
        if request.method == 'GET':

            try:
                if user_id is None or user_pswrd == "":
                    return JsonResponse({"msg": "User Name or Password can't be Null", "msgcode": 7})

                elif user_id != None or user_pswrd != '':

                    collection =db_con()["mif_user_reg"]
                    data = collection.find({"_id":str(user_id), "u_pswrd" :str(user_pswrd)})
                    dic = {"user_dt": json.loads(dumps(data))}
                    return JsonResponse(dic)
                    #return Response(dic)

            except ValueError as e:
                print("error --", e)
                return JsonResponse({"msg": "Value Error", "msgcode": 86})
            except InvalidId as e:
                return JsonResponse({"msg": "Invalid ID", "msgcode": 88, "MsgDec": str(e)})
            except InvalidStringData:
                return JsonResponse({"msg": "Invalid Data", "msgcode": 91})
            except Exception as e:
                return JsonResponse({"msg": "Parent Exception at GET", "msgcode": 50})

            finally:
                global client
                client=None
                # return Response(json.loads(dumps(data)));
                # return HttpResponse("<h4> "+str(dic)+" </h4>")

    @csrf_exempt
    def post(self,request):
        if request.method == 'POST':
            try:
                data = request.body.decode('utf-8')
                collection = db_con()["mif_user_reg"]
                ins_msg=collection.insert_one(json.loads(data)).acknowledged
                global client
                client=None
                if ins_msg == True:
                    return JsonResponse({"msg":"Sucess","msgcode":1})

            except ValueError as e:
                print("error --",e)
                return JsonResponse({"msg":"Value Error","msgcode":86})
            except DuplicateKeyError as e:
                return JsonResponse({"msg":"User Name Exist","msgcode":83})
            except InvalidId as e:
                return JsonResponse({"msg": "Invalid ID", "msgcode": 88,"MsgDec":str(e)})
            except InvalidStringData :
                return JsonResponse({"msg": "Invalid Data", "msgcode": 91})
            except Exception as e:
                return JsonResponse({"msg": "Parent Exception", "msgcode": 90, "MsgDec": str(e)})
            finally:
                client=None

    @csrf_exempt
    def put(self,request):
        if request.method == 'PUT':
            try:
                data = request.body.decode('utf-8')
                data = json.loads(data)
                print("_id is -", data["_id"])
                collection = db_con()["mif_user_reg"]
                ins_msg = collection.update_one({'_id':data['_id']},{'$set':{'u_pswrd':data['u_pswrd']},"$currentDate":{"lastModified":True}},).acknowledged
                global client
                client = None
                if ins_msg == True:
                    return JsonResponse({"msg": "Sucess", "msgcode": 1})

            except ValueError as e:
                print("error --", e)
                return JsonResponse({"msg": "Value Error", "msgcode": 86})
            except DuplicateKeyError as e:
                return JsonResponse({"msg": "User Name Exist", "msgcode": 83})
            except InvalidId as e:
                return JsonResponse({"msg": "Invalid ID", "msgcode": 88})
            except InvalidStringData:
                return JsonResponse({"msg": "Invalid Data", "msgcode": 91})
            except Exception as e:
                return JsonResponse({"msg": "Parent Exception", "msgcode": 90, "MsgDec": str(e)})
            finally:
                client = None


def handler404(request):
    return JsonResponse({"msg": "Not Found", "msgcode": 404})
def handler500(request):
    return JsonResponse({"msg": "Server Error", "msgcode": 500})