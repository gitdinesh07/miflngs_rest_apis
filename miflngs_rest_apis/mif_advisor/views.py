from django.shortcuts import render
from django.http import JsonResponse
from .service import AdvisorService
# Create your views here.

class MifAdvisor(AdvisorService):

    def AdvisorLoginAuth(self, request):
            if request.method == 'GET':
                data = request.body.decode('utf-8')
                return JsonResponse(AdvisorService.advisor_login_auth(data))


    def AdvisorSignUp(self,request):
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            return JsonResponse(AdvisorService.advisor_signup(data))