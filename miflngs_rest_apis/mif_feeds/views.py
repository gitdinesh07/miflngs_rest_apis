from .service import mif_feeds
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create New Post against particular User_id
@csrf_exempt
def post_feed(request):
    try:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            return JsonResponse(mif_feeds.post_feeds_by_user(data))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


# Get Feeds ( All Post ) By particular User_id
def get_feeds_by_user(request, user_id):
    try:
        if request.method == 'GET':
            return JsonResponse(mif_feeds.get_feeds_by_user(user_id))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


# Get Feeds ( All Post ) By particular category name
def get_feeds_by_cate(request, cate_name):
    try:
        if request.method == 'GET':
            return JsonResponse(mif_feeds.get_feeds_by_cate_id(cate_name))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


# Increment Like as per post_id
@csrf_exempt
def upt_feeds(request, post_id, like):
    try:
        if request.method == 'PUT':
            return JsonResponse(mif_feeds.upt_feeds_by_user(post_id, like))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


# Create comment against particular Post_id
@csrf_exempt
def comm_on_user_feed(request):
    try:
        if request.method == 'POST':
            data = request.body.decode('utf-8')
            return JsonResponse(mif_feeds.create_comm_on_user_feed(data))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


# Remove post and comment as per Post_id
@csrf_exempt
def del_feeds(request):
    try:
        if request.method == 'DELETE':
            data = request.body.decode('utf-8')
            return JsonResponse(mif_feeds.del_feeds_by_user(data))
    except Exception as e:
        return JsonResponse({"msg": "View Parent Exception", "msg_code": 0, "msg_dec": e})


def top_trending(request):
        if request.method == 'GET':
            return JsonResponse(mif_feeds.top_trending())