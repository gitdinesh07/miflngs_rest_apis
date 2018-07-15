from django.conf.urls import url
from . import views

# Create your tests here.

urlpatterns = [
    # Get Feeds ( All Post ) By particular User_id
    url(r'^usr-feeds/(?P<user_id>[a-z0-9]+)$', views.get_feeds_by_user),
    # Get Feeds ( All Post ) By particular category_name
    url(r'^cate-feeds/(?P<cate_name>[a-zA-Z &]+)$', views.get_feeds_by_cate),
    # Create New Post against particular User_id
    url(r'^create-usr-feeds$', views.post_feed, name="POST"),
    # Create comment against particular Post_id
    url(r'^comment-on-usr-feeds$', views.comm_on_user_feed, name="POST"),
    # Increment Like as per post_id
    # url((r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$',),
    url(r'^upt-usr-feeds/(?P<post_id>[0-9]+)/(?P<like>[-1,1]+)$', views.upt_feeds, name="PUT"),
    # Remove post and comment as per Post_id
    url(r'^del-usr-feeds$', views.del_feeds, name="DELETE"),
    # Top User and Categories find
    url(r'^top-trend-cate_n_users$', views.top_trending, name="GET"),
]