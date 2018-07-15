from django.shortcuts import render
from miflngs_rest_apis import models as db_connection
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import JsonResponse
from .service import cate_service
import datetime


class MifCategoryList(APIView):
    obj = cate_service()

    def get(self, request):
        try:
            if request.method == 'GET':
                return JsonResponse(self.obj.get_cate())
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    @csrf_exempt
    def usr_cate_upt(self, request):
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                get_response = self.obj.upt_user_cate_flw(data)
                return JsonResponse(get_response)

    def get_usr_cate_flw_cnt(self, request, user_id):
            if request.method == 'GET':
                get_response = self.obj.get_user_cate_flw(user_id)
                return JsonResponse(get_response)

    def cate_user_cate_flw(self,request,user_id):
        if request.method == 'GET':
                get_response = self.obj.get_cate_by_user(user_id)
                return JsonResponse(get_response)