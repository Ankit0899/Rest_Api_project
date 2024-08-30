import mysql.connector
import json
from flask import make_response
from datetime import datetime
from datetime import timedelta
import jwt
from config.config import dbconfig

class user_model():

    def __init__(self):
        # connection establishment code
        try:
            self.con = mysql.connector.connect(
                host = dbconfig['hostname'],
                user =dbconfig['username'],
                password = dbconfig['password'],
                database = dbconfig['database']
                )
            # print("Mysql Connecct successful")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            
        except:
            print("Some Error")

    def user_getall_model(self):
        # Business logic
        self.cur.execute("SELECT * FROM flask_data.users")
        result = self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            # return result
            return make_response({"payload":result}, 200)
        else:
            return make_response({"message": "No Data Found"}, 204)
        
    def user_addone_model(self, data):
        # Business logic
        self.cur.execute(f"INSERT into users(name, email, phone, password, role) VALUES('{data['name']}', '{data['email']}','{data['phone']}', '{data['password']}', '{data['role']}') ")
        # return "User Create Successfully!!"
        return make_response({"message": "User Create Successfully!!"}, 201)
    

    def user_update_model(self, data):
        # Business logic
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role='{data['role']}', password='{data['password']}' WHERE id = {data['id']}")
        if self.cur.rowcount>0:
            # return "User Updated Successfully!!"
            return make_response({"message": "User Updated Successfully!!"}, 201)
        else:
            return make_response({"message": "Nothing to Update"}, 202)
        

    def user_delete_model(self, id):
        # Business logic
        self.cur.execute(f"DELETE FROM users WHERE id = {id} ")
        if self.cur.rowcount>0:
            # return "User Deleted Successfully!!"
            return make_response({"message": "User Deleted Successfully!!"})
        else:
            return make_response({"message": "Nothing to Update"}, 202)
        

    def user_patch_model(self, data, id):
        qry = "UPDATE users SET "
        for key in data :
            qry += f"{key} ='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {id}"

        self.cur.execute(qry)
        # return qry

        if self.cur.rowcount>0:
            # return "User Deleted Successfully!!"
            return make_response({"message": "User Update Successfully!!"})
        else:
            return make_response({"message": "Nothing to Update"}, 202)
        

    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)

        start = (page*limit) - limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"payload":result, "page_no":page, "limit":limit}, 200)
        else:
            return make_response({"message": "No Data Found"}, 204)
        
    
    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id = {uid}")
        if self.cur.rowcount>0:
            # return "User Updated Successfully!!"
            return make_response({"message": "File Upload Successfully!!"}, 201)
        else:
            return make_response({"message": "Nothing to Update"}, 202)
        

    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name,email,phone,avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}' " )
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time
        }
        jwt_token = jwt.encode(payload, "Ankit", algorithm="HS256")
        return make_response({"token":jwt_token}, 200)