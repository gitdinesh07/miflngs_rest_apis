from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .service import user_service


class MiUserList(APIView, user_service):

    # for user login get method
    def get(self, request, user_id, user_pswrd):
        if request.method == 'GET' and (user_id or user_pswrd) != "":
            return JsonResponse(self.user_login_auth(user_id, user_pswrd))

    # Get user profile details
    def get_user_dt(self, request, get_id):
        if request.method == 'GET' and get_id != '':
            return JsonResponse(self.get_user_details(get_id))

    # Update user profile
    @csrf_exempt
    def put_user_dt(self, request, get_id):
        try:
            if request.method == 'PUT' and get_id != '':
                data = request.body.decode('utf-8')
                return JsonResponse(self.upt_user_prf(get_id, data))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    # Update user profile picture
    @csrf_exempt
    def put_user_img(self, request):
        try:
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                return JsonResponse(self.user_prf_img(data))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    # Create new user
    @csrf_exempt
    def post_cre_user(self, request):
        try:
            if request.method == 'POST':
                data = request.body.decode('utf-8')
                return JsonResponse(self.create_nw_user(data))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    # user password reset
    @csrf_exempt
    def put_reset_psw(self, request):
        try:
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                return JsonResponse(self.res_usr_psw(data))
        except Exception as e:
            return JsonResponse({"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)})

    # Forget password module
    @csrf_exempt
    def put_forget(self, request):
        try:
            if request.method == 'PUT':
                data = request.body.decode('utf-8')
                return JsonResponse(self.frgt_user_psw(data))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    def ver_user(self, request, get_id):
        try:
            if request.method == 'GET':
                print("verify user get_id -", get_id)
                return JsonResponse(self.verify_user(get_id))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    @csrf_exempt
    def usr_logs(self, request):
        try:
            if request.method == 'POST':
                data = request.body.decode('utf-8')
                return JsonResponse(self.create_usr_logs(data))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})

    def otp_request(self, request, get_mob):
        try:
            if request.method == 'GET':
                return JsonResponse(self.user_get_otp(get_mob))
        except Exception as e:
            return JsonResponse({"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)})


def handler404(request):
    return JsonResponse({"msg": "Not Found", "msg_code": 404})


def handler500(request):
    return JsonResponse({"msg": "Server Error", "msg_code": 500})