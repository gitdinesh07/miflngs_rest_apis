from django.conf.urls import url
from . import  views
from django.http import JsonResponse


urlpatterns = [

    # GET- for user login
    url(r'^users/(?P<user_id>[a-z0-9]+)/(?P<user_pswrd>[a-z0-9]+)$', views.MiUserList.as_view()),
    # url(r'^user/(?P<user_id>(.*)+)/(?P<user_pswrd>[a-z0-9]+)$',views.MiUserList.as_view()),
    url(r'^users/create$', views.MiUserList().post, name='post'),
    url(r'^users/psw-rst$', views.MiUserList().put, name='PUT'),
    url(r'^users/psw-frgt$', views.MiUserList().put_forget, name='PUT'),
    url(r'^users/psw-frgt-user_chk/(?P<get_id>[a-z0-9@.]+)$', views.MiUserList().put_chk_usr, name='GET'),



]

handler404 = views.handler404
handler500 = views.handler500