from django.conf.urls import url
from . import views


urlpatterns = [

    # GET-  user login ( verify user with password )
    url(r'^categories_list$', views.MifCategoryList.as_view(), name='GET'),
    url(r'^usr_cate-follows/usr-cate-upt$', views.MifCategoryList().usr_cate_upt),
    url(r'^usr-cate/flw-unflw-dt/(?P<user_id>[a-z0-9]+)$', views.MifCategoryList().get_usr_cate_flw_cnt, name='GET'),
    url(r'^cate_dt-usr-cate/(?P<user_id>[a-z0-9]+)$', views.MifCategoryList().cate_user_cate_flw, name='GET'),
    ]