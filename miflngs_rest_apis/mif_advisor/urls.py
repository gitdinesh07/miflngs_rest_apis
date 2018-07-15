from django.conf.urls import url
from . import views



urlpatterns = [

    # GET-  user login ( verify user with password )
    url(r'^advisors/login-auth$', views.MifAdvisor.advisor_login_auth),
]