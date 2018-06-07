from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from datetime import datetime
from pymongo import MongoClient
import json
from rest_framework.views import APIView
from bson.json_util import dumps
# Create your views here.


def default_page(request):
    return  HttpResponse("<h1>hello welcome </h1>");
    # return render(request, "welcome.html", {"Welcome": str(u_name)})


def db_con(db_name,collection_name):
    try:
        client = MongoClient("localhost", 27017)
        collection = client[db_name][collection_name]
        print("collection -",collection)
        return collection
    except Exception as e:
        print("DB Connection fail with -", e)


class MiUserList(APIView):

    # for user login get method
    def get(self, request, user_id,user_pswrd):
        if request.method == 'GET':
            try:
                print("get",user_id)

                collection =db_con("mifeel","mif_user_reg")
                data = collection.find({"_id":int(user_id),"pswrd":str(user_pswrd)})
                dic = {"detail": json.loads(dumps(data))}
                return Response(dic)
            except Exception as e:
                print("Exceltion at GET")
                # return Response(json.loads(dumps(data)));
                # return HttpResponse("<h4> "+str(dic)+" </h4>")



    def post(self,request):
        if request.method == 'POST':
            print("post")


