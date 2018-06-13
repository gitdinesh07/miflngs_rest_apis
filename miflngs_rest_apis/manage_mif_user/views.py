from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from pymongo.errors import InvalidId
from pymongo.errors import InvalidStringData
import json
from rest_framework.views import APIView
from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from miflngs_rest_apis import model as db_connection


client = object


class MiUserList(APIView):
    # for user login get method
    def get(self, request, user_id, user_pswrd):
        try:
            if request.method == 'GET' and user_id != '' or user_pswrd != '':
                try:
                        collection = db_connection.db_con()["mif_user_reg"]
                        data = collection.find({"$and": [{"_id": str(user_id)}, {"password": str(user_pswrd)}]})
                        dic = {'user_dt': json.loads(dumps(data))}
                        if dic.get('user_dt'):
                            return JsonResponse(dic)
                        elif bool(dic.get('user_dt')) is False :
                            return JsonResponse({"msg": "User Does Not Exist", "msg_code": 11})
                except ValueError as e:
                    print("error --", e)
                    return JsonResponse({"msg": "Value Error", "msg_code": 86})
                except InvalidId as e:
                    return JsonResponse({"msg": "Invalid ID", "msg_code": 88, "msg_dec": str(e)})
                except InvalidStringData:
                    return JsonResponse({"msg": "Invalid Data", "msg_code": 91})
                except Exception as e:
                    return JsonResponse({"msg": "Parent Exception at GET", "msg_code": 0, 'msg_dec': str(e)})
                finally:
                    global client
                    client = None

            elif user_id is None or user_pswrd == "":
                return JsonResponse({"msg": "User Name or Password can't be Null", "msg_code": 7})
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    @csrf_exempt
    def post(self, request):
        try:
            if request.method == 'POST':
                try:
                    data = request.header.decode('utf-8')
                    collection = db_connection.db_con()["mif_user_reg"]
                    ins_msg = collection.insert_one(json.loads(data)).acknowledged
                    global client
                    client = None
                    if ins_msg:
                        return JsonResponse({"msg": "Success", "msg_code": 1})
                except ValueError:
                    return JsonResponse({"msg": "Value Error", "msg_code": 86})
                except DuplicateKeyError:
                    return JsonResponse({"msg": "User Name Already Exist", "msg_code": 83})
                except InvalidId as e:
                    return JsonResponse({"msg": "Invalid ID", "msg_code": 88, "msg_dec": str(e)})
                except InvalidStringData:
                    return JsonResponse({"msg": "Invalid Data", "msg_code": 91})
                except Exception as e:
                    return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})
                finally:
                    client = None
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

# user password reset
    @csrf_exempt
    def put(self, request):
        try:
            if request.method == 'PUT':
                try:

                    data = request.body.decode('utf-8')
                    data = json.loads(data)
                    ins_msg = 0
                    if data['_id'] == "" or str(data['password']) == "" or str(data['new_password']) == "":
                        return JsonResponse({"msg": "Fail Password Reset - Fields Can not be Empty", "msg_code": 13})
                    elif data['_id'] != '' and str(data['password']) != "" and str(data['new_password']) != "":
                        collection = db_connection.db_con()["mif_user_reg"]
                        user_id = {}
                        try:
                            user_id = collection.find({"_id": str(data["_id"]), "password": str(data['password'])}, {'_id': 1}).__getitem__(0)
                            # check user exist or not user_id == False if it empty.
                            if bool(user_id) is False:
                                return JsonResponse({"msg": "User Does Not Exist", "msg_code": 11})
                            elif user_id['_id'] != '' or user_id['_id'] is not None:
                                ins_msg = collection.update_one({'_id': data['_id']}, {'$set': {'password': data['new_password']},"$currentDate":{"lastModified":True}}).modified_count
                        except Exception as e:
                            print("Exception - ", e)
                            if bool(user_id) is False :
                                return JsonResponse({"msg": "Incorrect User ID & Password ", "msg_code": 11, "msg_dec": str(e)})
                    global client
                    client = None

                    if ins_msg == 1:
                        return JsonResponse({"msg": "Success", "msg_code": 1})
                    elif ins_msg == 0:
                        return JsonResponse({"msg": "Fail", "msg_code": 0})

                except ValueError as e:
                    print("error --", e)
                    return JsonResponse({"msg": "Value Error", "msg_code": 86})
                except DuplicateKeyError:
                    return JsonResponse({"msg": "User Name Already Exist", "msg_code": 83})
                except InvalidId as e:
                    return JsonResponse({"msg": "Invalid ID", "msg_code": 88})
                except Exception as e:
                    return JsonResponse({"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)})
                finally:
                    client = None
        except Exception as e:
            return JsonResponse({"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)})

    # Forget password module
    @csrf_exempt
    def put_forget(self,request):
        try:
            if request.method == 'PUT':
                try:
                    data = request.body.decode('utf-8')
                    data = json.loads(data)
                    collection = db_connection.db_con()["mif_user_reg"]
                    user_id = {}
                    ins_msg = 0
                    try:
                        # Get _id from database
                        user_id = json.loads(MiUserList().put_chk_usr(request,str(data['verify_id'])).getvalue())
                        # check user exist in DB or not user_id == False if it empty.
                        print("user id ",(user_id))
                        if '_id' in user_id  :
                            ins_msg = collection.update_one(user_id, {'$set': {'password': data['password']},
                                                                      "$currentDate": {
                                                                          "lastModified": True}}).modified_count

                        elif '_id' not in user_id  and 'msg_code' in user_id :
                            return JsonResponse(user_id)
                    except Exception as e:
                        print("Exception - ", e)
                        if bool(user_id) is False:
                            return JsonResponse({"msg": "User Does Not Exist", "msg_code": 11, "msg_dec": str(e)})
                    global client
                    client = None
                    if ins_msg == 1:
                        return JsonResponse({"msg": "Success", "msg_code": 1})
                    elif ins_msg == 0:
                        return JsonResponse({"msg": "Password Not Change", "msg_code": 0})
                except ValueError as e:
                    print("error --", e)
                    return JsonResponse({"msg": "Value Error", "msg_code": 86})
                except DuplicateKeyError as e:
                    return JsonResponse({"msg": "User Name Exist", "msg_code": 83})
                except InvalidId as e:
                    return JsonResponse({"msg": "Invalid ID", "msg_code": 88})
                except InvalidStringData:
                    return JsonResponse({"msg": "Invalid Data", "msg_code": 91})
                except Exception as e:
                    return JsonResponse({"msg": str(e), "msg_code": 0})
                finally:
                    client = None
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    # Check user exist or not for Forget password module
    @csrf_exempt
    def put_chk_usr(self, request,get_id):
        try:
            #if request.method == 'GET':
                print("Get_data -",get_id)
                collection = db_connection.db_con()["mif_user_reg"]
                user_id = {}
                if get_id == "":
                    return JsonResponse(
                        {"msg": "Fail Password Forget - Fields Can not be Empty", "msg_code": 13})
                elif get_id != '':
                    try:
                        # Get _id from database
                        user_id = collection.find(
                            {'$or': [{"_id": str(get_id)}, {"email": str(get_id)}]},
                            {'mob_ivr': 1}).__getitem__(0)
                        # check user exist in DB or not user_id == False if it empty.
                        if bool(user_id) is False:
                            return JsonResponse({"msg": "User Does Not Exist", "msg_code": 11})
                        elif user_id['mob_ivr'] != '' or user_id['mob_ivr'] is None:
                            return JsonResponse(user_id)
                    except Exception as e:
                        print("Exception - ", e)
                        if bool(user_id) is False:
                            return JsonResponse(
                                {"msg": "User Does Not Exist", "msg_code": 11, "msg_dec": str(e)})
        except AssertionError as e:
            print(e)

def handler404(request):
    return JsonResponse({"msg": "Not Found", "msg_code": 404})


def handler500(request):
    return JsonResponse({"msg": "Server Error", "msg_code": 500})