from datetime import datetime
from pymongo.errors import PyMongoError
import json
from miflngs_rest_apis import models as db_connection


class cate_service():

    def get_cate(self):
        try:
            self.data = {}
            cate_list = list()
            with db_connection.database_conn() as collection:
                self.data = collection['mif_category_dt'].find({'status': {'$eq': 1}})
                for GetAllCategories in self.data:
                    cate_list.append(GetAllCategories)
            return {"category_dt": cate_list}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def upt_user_cate_flw(self, data):
        try:
            data = json.loads(data)
            user_id = str(data['_id'])
            del data['_id']
            ''' 
               # bulk = collection["mif_category_dt"].initialize_unordered_bulk_op()
               for key, value in data.items():
                   bulk.find({'_id': key}).update_one({'$inc': {"cate_flw_cnt": value}})
                   if data[key] == -1:
                       data[key] = 0
               upt_msg = bulk.execute()'''
            with db_connection.database_conn() as collection:
                    upt_msg = 0
                    # update mif categories follow unfollow count
                    for key, value in data.items():
                        upt_msg = collection['mif_category_dt'].update_one({'_id': key}, {'$inc': {"cate_flw_cnt": value}}).modified_count
                        if data[key] == -1:
                            data[key] = 0
                    # update user category follow unfollow collection
                    usr_cate_upt = collection['user_cate_flw'].update_one({'_id': user_id}, {'$set': data}, upsert=False).modified_count

            if (upt_msg and usr_cate_upt) == 1:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except PyMongoError as e:
            return {"msg": "MongoDB Error", "msg_code": 0, "msg_dec": str(e)}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def get_user_cate_flw(self, user_id):
        try:
            with db_connection.database_conn() as collection:
                if collection["user_cate_flw"].find({"_id": str(user_id)}, {'_id': 1}).count() > 0:
                    data = collection["user_cate_flw"].find({"_id": str(user_id)}).__getitem__(0)
                else:
                    data = {"msg": "User Does Not Exist", "msg_code": 11}
            return data
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def get_cate_by_user(self, user_id):
        try:
            self.data1 = {}
            cate_list = list()
            with db_connection.database_conn() as collection:
                if collection["user_cate_flw"].find({"_id": str(user_id)}, {'_id': 1}).count() > 0:
                    data1 = collection["user_cate_flw"].find({"_id": str(user_id)}, {'_id': 0}).__getitem__(0)
                    self.data = collection['mif_category_dt'].find(
                        {'status': {'$eq': 1}},
                        {'_id': 1, 'cate_name': 1, 'cate_image': 1, 'cate_flw_cnt': 1})
                    for GetAllCategories in self.data:
                        GetAllCategories['user_cate_flw_status'] = data1[GetAllCategories['_id']]
                        cate_list.append(GetAllCategories)
                    return {"category_dt": cate_list}
                else:
                    return {"msg": "User Does Not Exist", "msg_code": 11}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}