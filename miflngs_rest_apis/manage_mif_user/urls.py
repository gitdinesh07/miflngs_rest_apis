from django.conf.urls import url
from . import  views

urlpatterns = [

    url(r'^$',views.default_page),
    # GET- for user login
    url(r'^user/(?P<user_id>[a-z0-9]+)/(?P<user_pswrd>[a-z0-9]+)$',views.MiUserList.as_view()),
    url(r'^user/create$',views.MiUserList.post())
    #url(r'^user_id$',views.default_page),
    #url('')
    #url(r'^city_name/$',views.hospitalList.as_view()),
]