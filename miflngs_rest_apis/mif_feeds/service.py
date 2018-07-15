import json
from miflngs_rest_apis import models as db_connection
from datetime import datetime, timedelta
from random import randint
from pymongo.errors import PyMongoError
from django.core.paginator import InvalidPage
from django.core.paginator import Paginator as DjangoPaginator


# Create your models here.


class mif_feeds():

    @staticmethod
    def get_feeds_by_user(user_id):
        try:
            feed_list = list()
            with db_connection.database_conn() as collection:
                data = collection['mif_feeds'].find({'user_id': user_id}).sort('feed_dt', -1)
                # data = collection['mif_feeds'].find({'user_id': user_id},{"comment_dec":{"$elemMatch":{"comment_status":1}}}).sort('feeds',-1)
                # data = collection['mif_feeds'].find({'user_id': user_id, 'status': 1, "comment_dec": {"$elemMatch":{"comment_status":1}}}).sort('feeds',-1)
                for GetAllfeeds in data:
                    feed_list.append(GetAllfeeds)
            return {"feeds_dt": feed_list}

        except Exception as e:
            return {{"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}}

    @staticmethod
    def get_feeds_by_cate_id(cate_name):
        try:
            feed_list = list()
            cate_name = str(cate_name).upper()
            print("cate_name - ",cate_name)
            with db_connection.database_conn() as collection:
                data = collection['mif_feeds'].find({'cate_name': cate_name, 'post_type': 1}).sort('feed_dt', -1)
                for GetAllfeeds in data:
                    feed_list.append(GetAllfeeds)
            return {"feeds_dt": feed_list}

        except Exception as e:
            return {{"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}}

    @staticmethod
    def post_feeds_by_user(data):
        try:
            data = json.loads(data)
            '''data = {
                    'user_id': data['user_id'],
                    'feeds': data['feeds'],
                    'cate_id': data['cate'],
                    'feed_dt': datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S"),
                    }'''
            data['feed_dt'] = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            data['likes'] = 0
            data['post_type'] = int(data['post_type'])  # if post_type = 0 then it is private post || if post_type = 1 then it is public post
            data['comment_dec'] = []
            with db_connection.database_conn() as collection:
                # Check if User is valid or not
                if collection["mif_user_dt"].find({"$and": [{"_id": str(data['user_id'])}, {"admin_status": 1}, {"status": 1}]}, {'_id': 1}).count() > 0:
                    if collection['mif_feeds'].find({}, {'_id': 1}).sort('_id', -1).limit(1).count() > 0:
                        get_last_inserted_id = collection['mif_feeds'].find({}, {'_id': 1}).sort('_id', -1).limit(1).__getitem__(0)
                        data['_id'] = str(int(get_last_inserted_id['_id']) + 1)  # increment _id by 1
                    else:
                        data['_id'] = "101"  # First Default  _id (post_id) 101
                    ins_msg = collection['mif_feeds'].insert_one(data).acknowledged
                    if ins_msg:
                        return {"msg": "Success", "msg_code": 1}
                    else:
                        return {"msg": "Fail", "msg_code": 0}
                else:
                    return {"msg": "Sorry User Does Not Exist OR Account Deactivated", "msg_code": 3}
        except PyMongoError as e:
            return {{"msg": "Service PyMongo Exception", "msg_code": 0, "msg_dec": e}}
        except Exception as e:
            return {{"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}}

    # Increment Like as per post_id
    @staticmethod
    def upt_feeds_by_user(post_id, like):
        try:
            print("like is -",like)
            with db_connection.database_conn() as collection:
                upt_msg = collection['mif_feeds'].update_one({'_id': post_id}, {'$inc': {"likes": int(like)}}).modified_count
            if upt_msg >= 1:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except Exception as e:
            return {{"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}}

    @staticmethod
    def del_feeds_by_user(data):
        try:
            data = json.loads(data)
            upt_msg = 0
            post_id = data['post_id']
            user_id = data['user_id']
            print("your data is ",data)
            with db_connection.database_conn() as collection:
                # Check that data exist only comment_id or not if yes then it must be delete any comment.
                if 'post_id' in data and 'comment_id' not in data:
                    if collection['mif_feeds'].find({"$and": [{'_id': post_id}, {"user_id": user_id}]}, {'_id': 1}).count() >= 1:
                        upt_msg = collection['mif_feeds'].delete_one({'_id': post_id}).deleted_count
                    else:
                        return {"msg": "Sorry You are not Authorize User", "msg_code": 8}
                elif 'comment_id' in data and 'post_id' in data:
                    # check comment_id which will delete that comment only delete by who create that comment OR who create that particular post
                    if collection['mif_feeds'].find({"$and": [{'comment_dec.comment_id': data['comment_id']},
                                                              {'$or': [{'comment_dec.user_id': user_id},
                                                                       {"user_id": user_id}]
                                                              }]}, {'_id': 1}).count() >= 1:
                        upt_msg = collection['mif_feeds'].update_one({'_id': post_id}, {'$pull': {'comment_dec': {'comment_id': data['comment_id']}}}
                                                                     ).modified_count
                    else:
                        return {"msg": "Sorry You are not Authorize User", "msg_code": 8}
            if upt_msg >= 1:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except Exception as e:
            return {{"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}}

    @staticmethod
    def create_comm_on_user_feed(data):
        try:
            data = json.loads(data)
            data['comment_dt'] = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            data['comment_id'] = randint(1, 199)
            post_id = data['post_id']
            del data['post_id']
            with db_connection.database_conn() as collection:
                ins_msg = collection['mif_feeds'].update_one({'_id': post_id}, {'$push': {'comment_dec': data}}, upsert=False).modified_count
            if ins_msg == 1:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except Exception as e:
            return {"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}

    @staticmethod
    def top_trending():
        try:
            all_data = dict()
            get_all_data = list()
            from_date = datetime.today() - timedelta(days=31)
            print("from_Date- ", from_date)
            with db_connection.database_conn() as collection:
                top_cate = collection['mif_feeds'].aggregate([
                                                            {'$match': {'feed_dt': {'$gte': from_date}}},
                                                            {'$group': {'_id': "$cate_name", 'count': {'$sum': 1}}},
                                                            {'$sort': {'count': -1}},
                                                            {'$limit': 5}
                                                        ])
                for Top_categories in top_cate:
                    get_all_data.append(Top_categories)
                all_data['top_categories'] = get_all_data
                top_users = collection['mif_feeds'].aggregate([
                                                            {'$match': {'comment_dec.comment_dt': {'$gte': from_date}}},
                                                            {'$project': {'_id': 0, 'comment_dec': {'user_id': 1}}},
                                                            {'$unwind': "$comment_dec"},
                                                            {'$group': {'_id': "$comment_dec.user_id", 'count': {'$sum': 1}}},
                                                            {'$sort': {'count': -1}},
                                                            {'$limit': 10}
                                                        ])
                get_all_data = []
                for Top_users in top_users:
                    get_all_data.append(Top_users)
                all_data['top_users'] = get_all_data
            del get_all_data
            return all_data
        except Exception as e:
            return {"msg": "Service Parent Exception", "msg_code": 0, "msg_dec": e}


