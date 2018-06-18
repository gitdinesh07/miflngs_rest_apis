from django.http import HttpResponse
from rest_framework.response import Response
from datetime import datetime
from pymongo.errors import WriteError
from pymongo.errors import PyMongoError
from pymongo.errors import DuplicateKeyError
from pymongo.errors import InvalidStringData
import json
from miflngs_rest_apis import models as db_connection



collection = db_connection.db_con()["mif_user_reg"]


class user_service():

    def user_login_auth(self, user_id, user_pswrd):
        try:
            if collection.find({"$and": [{"_id": str(user_id)}, {"password": str(user_pswrd)}, {'status': {'$eq': 1}}]}).count() > 0:
                data = ({"msg": "Success", "msg_code": 1})
            elif collection.find({"$and": [{"_id": str(user_id)}, {"password": str(user_pswrd)}, {'status': {'$eq': 0}}]}).count() > 0:
                data = {"msg": "Account Deactivated", "msg_code": 3}
            else:
                data = {"msg": "User & Password Not Exist", "msg_code": 11}
            return data
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
        finally:
            global client
            client = None


    def get_user_details(self,get_id):
        try:
                if collection.find({"_id": str(get_id)}).count() > 0:
                    data = collection.find({"_id": str(get_id)}).__getitem__(0)
                else:
                    data = {"msg": "User & Password Not Exist", "msg_code": 11}
                return data
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}

    def upt_user_prf(self, get_id, data):
        try:
                data = json.loads(data)
                print("type of data 44", type(data))
                if collection.find({"_id": str(get_id).lower()}).count() > 0:
                    upt_msg = collection.update_one({'_id': str(get_id)}, {'$set': data, }).acknowledged
                    data['as_on'] = datetime.now()
                    ins_upt_fld = collection.update_one({'_id': str(get_id)}, {'$push': {'update_fields': data}}).acknowledged
                else:
                    return {"msg": "User Does Not Exist", "msg_code": 11}
                global client
                client = None
                if upt_msg == 1 and ins_upt_fld == 1:
                    return {"msg": "Success", "msg_code": 1}
                elif upt_msg == 0:
                    return {"msg": "Fail", "msg_code": 0}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86}
        except DuplicateKeyError:
            return {"msg": "User Name Already Exist", "msg_code": 83}

        except Exception as e:
            return {"msg": "Profile Updation Fail", "msg_code": 0, "msg_dec": str(e)}
        finally:
            client = None

    def create_nw_user(self, data):
        try:
            upt_msg = False
            print("data 1 - ", data)
            data = json.loads(data)
            data = {'_id': str(data['_id']).lower(), 'password': str(data['password']), 'user_name': str(data['user_name']).lower(),
                    'mob_no': str(data['mob_no']),
                    'email': str(data['email']), 'gender': str(data['gender']).lower(), 'balance': float((data['balance'])), 'sub_dt': datetime.now(),
                    'status': 0, 'remark': ''}
            upt_msg = collection.insert_one(data).inserted_id

            global client
            client = None
            if str(upt_msg).lower() == str(data['_id']).lower():
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except DuplicateKeyError:
            return {"msg": "User Name Already Exist", "msg_code": 83}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except WriteError:
            return {"msg": "Write Error", "msg_code": 86}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
        finally:
            client = None

    def res_usr_psw(self, data):
        try:
            data = json.loads(data)
            upt_msg = 0
            if data['_id'] == "" or str(data['password']) == "" or str(data['new_password']) == "":
                return {"msg": "Fail Password Reset - Fields Can not be Empty", "msg_code": 13}
            elif data['_id'] != '' and str(data['password']) != "" and str(data['new_password']) != "":
                # collection = db_connection.db_con()["mif_user_reg"]
                if collection.find({"_id": str(data["_id"]), "password": str(data['password'])}, {'_id': 1}).count() > 0:
                    upt_msg = collection.update_one({'_id': data['_id']}, {'$set': {'password': data['new_password']}}).modified_count
                    get_id = str(data['_id']).lower()
                    del data['_id']
                    data['as_on'] = datetime.now()
                    ins_upt_fld = collection.update_one({'_id': get_id}, {'$push': {'update_fields': data}}).acknowledged
                    print("ins_upt_fld- ", ins_upt_fld)
                else:
                    return {"msg": "User Does Not Exist", "msg_code": 11}
            global client
            client = None
            if upt_msg == 1:
                return {"msg": "Success", "msg_code": 1}
            elif upt_msg == 0:
                return {"msg": "Fail", "msg_code": 0}
        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86}
        except Exception as e:
            return {"msg": "Password Reset Fail", "msg_code": 0, "msg_dec": str(e)}
        finally:
            client = None

    def frgt_user_psw(self, data):
        try:
            data = json.loads(data)
            # collection = db_connection.db_con()["mif_user_reg"]
            user_id = {}
            upt_msg = 0
            # Get _id from database
            user_id = json.loads(user_service().verify_user(str(data['verify_id'])).getvalue())
            print("user_id ", user_id)
            # check user exist in DB or not user_id == False if it empty.
            if '_id' in user_id:
                upt_msg = collection.update_one(user_id,
                                                {'$set': {'password': data['password']}}).modified_count

            elif '_id' not in user_id and 'msg_code' in user_id:
                return user_id
            global client
            client = None
            if upt_msg == 1:
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Password Not Change", "msg_code": 0}
        except ValueError as e:
            print("error --", e)
            return {"msg": "Value Error", "msg_code": 86}
        except DuplicateKeyError as e:
            return {"msg": "User Name Exist", "msg_code": 83}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": str(e), "msg_code": 0}
        finally:
            client = None

    def verify_user(self, get_id):
        try:

            # collection = db_connection.db_con()["mif_user_reg"]
            if get_id == "":
                return {"msg": "Fail Password Forget - Fields Can not be Empty", "msg_code": 13}
            elif get_id != '':
                # check user exist in DB or not user_id == False if it empty.
                if collection.find({'$or': [{"_id": str(get_id)}, {"email": str(get_id)}]}).count() > 0:
                    user_id = collection.find({'$or': [{"_id": str(get_id)}, {"email": str(get_id)}]}, {'mob_no': 1}).__getitem__(0)
                    return user_id
                else:
                    return {"msg": "User Does Not Exist", "msg_code": 11}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
        finally:
            global client
            client = None

    def create_usr_logs(self, data):
        try:
            data = json.loads(data)
            data = {'_id': str(data['_id']).lower(), 'user_id': str(data['user_id']), 'log_in': (data['log_in']),'log_out': datetime.now()}
            upt_msg = collection.insert_one(data).inserted_id

            global client
            client = None
            if str(upt_msg).lower() == str(data['_id']).lower():
                return {"msg": "Success", "msg_code": 1}
            else:
                return {"msg": "Fail", "msg_code": 0}

        except ValueError as e:
            return {"msg": "Value Error", "msg_code": 86, "msg_dec": str(e)}
        except PyMongoError as e:
            return {"msg": "pymongo  Error", "msg_code": 86, "msg_dec": str(e)}
        except DuplicateKeyError:
            return {"msg": "User Name Already Exist", "msg_code": 83}
        except WriteError:
            return {"msg": "Write Error", "msg_code": 86}
        except InvalidStringData:
            return {"msg": "Invalid Data", "msg_code": 91}
        except Exception as e:
            return {"msg": "Parent Exception", "msg_code": 0, "msg_dec": str(e)}
        finally:
            client = None