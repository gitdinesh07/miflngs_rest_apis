from django.conf.urls import url
from . import views
from rest_framework.request import clone_request as request
from django.conf.urls import handler404, handler500


urlpatterns = [

    # GET-  user login ( verify user with password )
    url(r'^users/(?P<user_id>[a-z0-9]+)/(?P<user_pswrd>.+)$', views.MiUserList.as_view()),
    # Get User Profile Details
    url(r'^users/users-profile/(?P<get_id>[a-z0-9]+)$', views.MiUserList().get_user_dt, name='GET'),

    # Update user details
    url(r'^users/alter-users-profile/(?P<get_id>[a-z0-9]+)$', views.MiUserList().put_user_dt, name='PUT'),
    # Create new user
    url(r'^users/create$', views.MiUserList().post_cre_user, name='post'),
    # Update user image
    url(r'^users/usr-prf-img$', views.MiUserList().put_user_img, name='PUT'),
    # user password reset
    url(r'^users/psw-rst$', views.MiUserList().put_reset_psw, name='PUT'),

    # -- forget password
    # check user exist or not with user_id or email
    url(r'^users/psw-frgt/user_chk/(?P<get_id>[a-z0-9@.]+)$', views.MiUserList().ver_user, name='GET'),
    # otp send to the user
    url(r'^users/psw-frgt/otp-req/(?P<get_mob>[a-z0-9@.]+)$', views.MiUserList().otp_request, name='GET'),
    # update password if forget
    url(r'^users/psw-frgt/upt-psw-req$', views.MiUserList().put_forget, name='PUT'),

    # User LogIn LogOut Logs
    url(r'^users/usr-session-logs$', views.MiUserList().usr_logs)



]

# handler404 = views.handler404
# handler500 = views.handler500