from datetime import datetime
from pymongo.errors import PyMongoError
from pymongo.errors import DuplicateKeyError
from pymongo.errors import InvalidStringData
import json
from random import randint
import requests
from miflngs_rest_apis import models as db_connection
from base64 import decodebytes


class user_service():

    def user_login_auth(self, user_id, user_pswrd):
        try:
            with db_connection.database_conn() as collection:
                if collection["mif_user_dt"].find({"$and": [{"_id": user_id}, {"password": user_pswrd}]}, {'_id': 1}).count() > 0:
                    get_data = collection["mif_user_dt"].find({"$and": [{"_id": user_id}, {"password": user_pswrd}]}, {'_id': 1, 'status': 1, 'admin_status': 1}).__getitem__(0)
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

    def get_user_details(self, get_id):
        try:
            with db_connection.database_conn() as collection:
                if collection["mif_user_dt"].find({"$and": [{"_id": get_id}, {'status': 1}, {'admin_status': 1}]}, {'_id': 1}).count() > 0:
                    return collection["mif_user_dt"].find(
                                            {"_id": get_id},
                                            {'remark': 0, 'status': 0, 'update_fields': 0, 'account_created': 0, 'update_on': 0, "admin_status": 0}
                                           ).__getitem__(0)
                else:
                        return {"msg": "User & Password Not Exist", "msg_code": 11}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def upt_user_prf(self, get_id, data):
        try:
            data = json.loads(data)
            if ('password' in data) or ('admin_status' in data) or ('status' in data):
                return {"msg": "Can't Update fields Directly", "msg_code": 14}
            with db_connection.database_conn() as collection:
                data['update_on'] = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                upt_msg = collection["mif_user_dt"].update_one({'_id': get_id}, {'$push': {'update_fields': data}, '$set': data}).modified_count
                if upt_msg == 0:
                    if collection["mif_user_dt"].find({"$and": [{"_id": get_id}, {'status': 1}, {'admin_status': 1}]}, {'_id': 1}).count() == 0:
                        return {"msg": "User Does Not Exist", "msg_code": 11}
                    return {"msg": "Fail", "msg_code": 0}
            if upt_msg == 1:
                return {"msg": "Success", "msg_code": 1}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except PyMongoError:
            return {"msg": "DB Error", "msg_code": 83}
        except Exception as e:
            return {"msg": "Profile Updation Fail", "msg_code": 0, "msg_dec": str(e)}

    def user_prf_img(self, data):
        try:
            data = json.loads(data)
            print("data - ", data)
            userid = str(data['user_id'])
            get_image_data = (data['image'])
            with open("media/images/mif_users/" + userid + ".png", "wb") as fh:
                fh.write(decodebytes(get_image_data.encode()))

            '''del data['image']
            data['image'] = '/media/images/mif_users/'+userid+'.png'
            collection = db_connection.db_con()["mif_user_dt"]
            upt_msg = collection.update_one(
                                            {'_id': userid},
                                            {'$push': {'update_fields': data}, ).modified_count '''

            return {"msg": "Sucess", "msg_code": 1}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def create_nw_user(self, data):
        try:

            data = json.loads(data)
            user_id = str(data['_id']).lower()
            data = {
                    '_id': user_id,
                    'password': str(data['password']),
                    'user_name': str(data['user_name']).lower(),
                    'mob_no': str(data['mob_no']),
                    'email': str(data['email']),
                    'gender': str(data['gender']).lower(),
                    'age': int(data['age']),
                    'image': '/media/images/mif_users/' + user_id + '.png',
                    'balance': float(0),
                    'account_created': datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S"),
                    'status': 1,
                    'admin_status': 1,
                    'remark': ''
                    }

            cate_id_dt = {}
            cate_id_dt['_id'] = user_id
            with db_connection.database_conn() as collection:
                upt_msg = collection["mif_user_dt"].insert_one(data).inserted_id # create user details document
                data2 = collection["mif_category_dt"].find({'status': 1}, {'_id': 1}).sort('_id') # find all categories which exist in cate table have to insert on user_cate_flw.
                for get_cate_id in data2:
                    cate_id_dt.setdefault(get_cate_id['_id'], 0)
                upt_msg_cate = collection["user_cate_flw"].insert_one(cate_id_dt).inserted_id # create user categories follow unfollow document against user_id.

            if upt_msg and upt_msg_cate == user_id:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except DuplicateKeyError:
            return {"msg": "User ID Already Exist", "msg_code": 83}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": "User creation Fail", "msg_code": 0, "msg_dec": str(e)}

    def res_usr_psw(self, data):
        try:
            data = json.loads(data)
            self.upt_msg = 0
            user_id = (data['_id'])
            cur_date_time = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            del data['_id']
            if user_id == "" or data['password'] == "" or data['new_password'] == "":
                return {"msg": "Fail Password Reset - Fields Can not be Empty", "msg_code": 13}
            else:
                data['update_on'] = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                data['upt_dec'] = "Password Reset by User"
                with db_connection.database_conn() as collection:
                        self.upt_msg = collection['mif_user_dt'].update_one({"$and": [{"_id": user_id}, {"password": data['password']}, {'status': 1}]},
                                                {'$push': {'update_fields': data}, '$set': {'password': data['new_password'], 'update_on': cur_date_time}}
                                                        ).modified_count
                        if self.upt_msg == 0:
                            if collection['mif_user_dt'].find({"$and": [{"_id": user_id}, {"password": str(data["password"])}]}, {'_id': 1}).count() <= 0:
                                return {"msg": "Current Password Not Match with ID", "msg_code": 11}
                            return {"msg": "Password Reset Fail", "msg_code": 0}
                if self.upt_msg == 1:
                    return {"msg": "Success", "msg_code": 1}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except Exception as e:
            return {"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)}

    def frgt_user_psw(self, data):
        try:
            data = json.loads(data)
            upt_msg = 0
            # Get _id from database using verify_user method
            get_data = (user_service().verify_user(str(data['verify_id'])))
            # check user exist in DB or not user_id == False if it empty.
            if '_id' in get_data:
                userid = get_data['_id']
                del data['verify_id']
                data['update_on'] = datetime.strptime((datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                with db_connection.database_conn() as collection:
                    if 'status' in data:
                        upt_msg = collection['mif_user_dt'].update_one(
                                                    {'_id': userid},
                                                    {'$push': {'update_fields': data}, '$set': {'password': data['password'], 'status': data['status']}}
                                                       ).modified_count
                    else:
                        upt_msg = collection['mif_user_dt'].update_one(
                                                            {'_id': userid},
                                                            {'$push': {'update_fields': data}, '$set': {'password': data['password']}}
                                                        ).modified_count
                    if upt_msg == 1:
                        return {"msg": "Success", "msg_code": 1}
                    else:
                        return {"msg": "Password or Status Not Update", "msg_code": 0}
            elif '_id' not in get_data and 'msg_code' in get_data:
                return get_data
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": str(e), "msg_code": 0}
        finally:
            client = None

    def verify_user(self, get_id):
        try:
            if get_id == "":
                return {"msg": "Fail Password Forget - Fields Can not be Empty", "msg_code": 13}
            elif get_id != '':
                with db_connection.database_conn() as collection:
                    # check user exist in DB
                    if collection["mif_user_dt"].find({'$or': [{"_id": str(get_id)}, {"email": str(get_id)}]}, {'_id': 1}).count() > 0:
                        self.user_dt = collection["mif_user_dt"].find({'$or': [{"_id": str(get_id)}, {"email": str(get_id)}]},
                                                                 {'mob_no': 1, 'status': 1, 'admin_status': 1}).__getitem__(0)
                    else:
                        return {"msg": "User Does Not Exist", "msg_code": 11}
                if self.user_dt['admin_status'] == 0:
                    return {"msg": "Sorry Your Account Deactivated By Administrator", "msg_code": 3}
                else:
                    del self.user_dt['admin_status']
                    return self.user_dt
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def create_usr_logs(self, data):
        try:
            data = json.loads(data)
            user_id = str(data['user_id'])
            if user_id == "" or user_id is None:
                return {"msg": "User ID Can't be Null", "msg_code": 13}
            else:
                log_in_tm = (datetime.strptime((data['log_in']), "%Y-%m-%d %H:%M:%S"))
                log_out_tm = (datetime.strptime((data['log_out']), "%Y-%m-%d %H:%M:%S"))
                log_dur = str(log_out_tm - log_in_tm)
                data = {
                        'user_id': user_id,
                        'log_in': log_in_tm,
                        'log_out': log_out_tm,
                        # '_id': str(str(data['user_id'])+ str(datetime.now().strftime("%Y%m%d%H%M%S.f"))),
                        'login_duration': log_dur
                       }
                with db_connection.database_conn() as collection:
                    upt_msg = collection["user_login_logs"].insert_one(data).inserted_id
                if upt_msg:
                    return {"msg": "Success", "msg_code": 1}
                else:
                    return {"msg": "Fail", "msg_code": 0}

        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except DuplicateKeyError:
            return {"msg": "User Name Already Exist", "msg_code": 83}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
        finally:
            client = None

    def user_get_otp(self, get_mob):
        try:
            otp = str((randint(100000, 999999)))
            otp_msg = "Your OTP is " + str(otp) + " for reset mifeelings password\n\nmifeelings"
            get_res = requests.get("http://{your-sms-provider-ip}/TataApi/SMS.jsp?ani=" + str(get_mob) + "&message=" + otp_msg + "&cli=65656")
            if get_res.status_code == 200:
                print({"mob_no": str(get_mob), "otp": otp, "msg_code": 1})
                return {"mob_no": str(get_mob), "otp": otp, "msg_code": 1}
            else:
                return {"msg": "OTP Not Sent", "msg_code": 0}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
