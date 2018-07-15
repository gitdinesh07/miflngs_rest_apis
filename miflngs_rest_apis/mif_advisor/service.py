from django.test import TestCase
from miflngs_rest_apis import models as db_connection
import json
import datetime
# Create your tests here.

class AdvisorService():

    def advisor_login_auth(self,data):
        try:
            data = json.loads(data)
            advisor_id = data['adv_id']
            advisor_paswrd = data['adv_pass']
            with db_connection.database_conn() as collection:
                if collection["mif_advisor_dt"].find({"$and": [{"_id": advisor_id}, {"password": advisor_paswrd}]}, {'_id': 1}).count() > 0:
                    get_data = collection["mif_advisor_dt"].find({"$and": [{"_id": advisor_id}, {"password": advisor_paswrd}]}, {'_id': 1, 'status': 1, 'admin_status': 1}).__getitem__(0)
                else:
                    return {"msg": "User & Password Not Match", "msg_code": 11}
            if get_data['admin_status'] == 0:
                return {"msg": "Sorry Your Account Deactivated By Administrator", "msg_code": 3}
            elif get_data['status'] == 0 and get_data['admin_status'] == 1:
                return {"msg": "Account Deactivated,You Will Have To Activate Your Account", "msg_code": 5}
            else:
                return {"msg": "Success", "msg_code": 1}

        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}


    def advisor_signup(self,data):
        try:
            data = json.loads(data)
            advisor_id = str(data['adv_id']).lower()
            data = {
                    '_id': advisor_id,
                    'password': str(data['password']),
                    'advisor_name': str(data['advisor_name']).lower(),
                    'mob_no': str(data['mob_no']),
                    'email': str(data['email']),
                    'gender': str(data['gender']).lower(),
                    'age': int(data['age']),
                    'image': '/media/images/mif_users/' + advisor_id + '.png',
                    'balance': float(0),
                    'account_created': datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S"),
                    'status': 1,
                    'admin_status': 1,
                    'remark': ''
                    }

        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}