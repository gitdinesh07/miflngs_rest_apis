from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from miflngs_rest_apis import models as db_connection
from .service import user_service

collection = db_connection.db_con()["mif_user_reg"]


class MiUserList(APIView):

    obj = user_service()

    # for user login get method

    def get(self, request, user_id, user_pswrd):
        if request.method == 'GET':
            get_response = self.obj.user_login_auth(user_id, user_pswrd)
            return JsonResponse((get_response))

    # Get user profile details
    def get_user_dt(self, request, get_id):
        if request.method == 'GET' and get_id != '':
            get_response = self.obj.get_user_details(get_id)
            return JsonResponse(get_response)

    # Update user profile
    @csrf_exempt
    def put_user_dt(self, request, get_id):
        if request.method == 'PUT' and get_id != '':
            data = request.body.decode('utf-8')
            get_response = self.obj.upt_user_prf(get_id, data)
            return JsonResponse(get_response)

    # Create new user
    @csrf_exempt
    def post_cre_user(self, request):
        try:
            if request.method == 'POST':
                data = request.body.decode('utf-8')
                get_response = self.obj.create_nw_user(data)
                return JsonResponse(get_response)
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    # user password reset
    @csrf_exempt
    def put_reset_psw(self, request):
        try:
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                get_response = self.obj.res_usr_psw(data)
                return JsonResponse(get_response)
        except Exception as e:
            return JsonResponse({"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)})

    # Forget password module
    @csrf_exempt
    def put_forget(self, request):
        try:
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                get_response = self.obj.frgt_user_psw(data)
                return JsonResponse(get_response)
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    def ver_user(self,request, get_id):
        if request.method == 'GET':
            print("verify user get_id -", get_id)
            get_response = self.obj.verify_user(get_id)
            return JsonResponse(get_response)

    def usr_logs(self, request):
        try:
            if request.method == 'POST':
                data = request.body.decode('utf-8')
                get_response = self.obj.create_usr_logs(data)
                return JsonResponse(get_response)
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})


def handler404(request):
    return JsonResponse({"msg": "Not Found", "msg_code": 404})


def handler500(request):
    return JsonResponse({"msg": "Server Error", "msg_code": 500})