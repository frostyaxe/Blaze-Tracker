'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resources for the Admin page requests.

Created on 03-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

from . import Resource
from . import render_template
from . import make_response
from flask import request, session
from . import redirect
from . import decode_password
from . import ResourceTemplatesName, BlazeUrls
from . import Error
from . import auth_required
from . import get_db_obj
from . import close_db_connection
from . import AuthenticationTableColumns
from . import TableName
from . import ResponseStatus
from . import validate_fields


NEW_CONFIRM_PASSWORD_FIELDS = [ "newPassword", "confirmPassword" ]
NOTIFICATION_FIELDS = [ "notificationTitle", "notificationMessage" ]

class AdminLogin(Resource):
    
    def __init__(self,app):
        self.app = app
   
    def get(self):
        return make_response(render_template(ResourceTemplatesName.ADMIN_LOGIN))
    
    def __get_secret__(self, username):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''
            SELECT {password} FROM {auth_table_name} WHERE {username} = ?
            
            '''.format(password=AuthenticationTableColumns.PASSWORD, auth_table_name=TableName.AUTH,username=AuthenticationTableColumns.USERNAME)
            record=sql_db_utils.execute_statement(sql,record=(username,)).fetchone()
            return record
        except Error as e:
            print(e) #replace it with logger
            return e
        finally:
            close_db_connection(sql_db_utils)
            
 
    def post(self):
        username = request.form['userId']
        secret = request.form['password']
        current_secret = None
        record = self.__get_secret__(username)
        if isinstance(record, Error):
            return make_response(render_template(ResourceTemplatesName.ADMIN_LOGIN, alert_message="Unable to verify the credentials. Please check logs.",alert_type="danger")) 
        if record and len(record) > 0:
            current_secret = decode_password(record[0])["secret"]
        else:
            return make_response(render_template(ResourceTemplatesName.ADMIN_LOGIN, alert_message="Invalid Credentials",alert_type="danger")) 
        if secret != current_secret:
            return make_response(render_template(ResourceTemplatesName.ADMIN_LOGIN, alert_message="Invalid Credentials",alert_type="danger"))
        else:
            session["authenticated"] = True
            session["username"] = request.form['userId']
            return redirect(BlazeUrls.ADMIN_HOME)
        

class AdminHome(Resource):
    
    def __init__(self,app):
        self.app = app
    
    @auth_required    
    def get(self):
        return make_response(render_template(ResourceTemplatesName.ADMIN_BASE))
    
class AdminPasswordChange(Resource):
    
    def __init__(self,app):
        self.app = app
    
    @auth_required    
    def get(self):
        return make_response(render_template(ResourceTemplatesName.ADMIN_UPDATE_PASSWORD))
    
    def __update_admin_password__(self, username, secret):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql ='''UPDATE {auth_table_name}
                    SET {password_column} = "{}"
                    WHERE {username_column} = "{}"
                '''.format(secret,username, auth_table_name=TableName.AUTH,password_column=AuthenticationTableColumns.PASSWORD,username_column=AuthenticationTableColumns.USERNAME)
            sql_db_utils.execute_script(sql)
            return True
        except Error as e:
            print(e) #replace with the logger
            return False
        finally:
            close_db_connection(sql_db_utils)
            
    @auth_required   
    def post(self):
        if "authenticated" in session and session["authenticated"]:
            request_json = request.get_json()
            if request_json == None:
                return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(NEW_CONFIRM_PASSWORD_FIELDS, request_json)
            if validation != None:
                return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            new_password = request_json["newPassword"]
            confirm_password = request_json["confirmPassword"]
            if new_password != confirm_password:
                return {"status": ResponseStatus.FAILURE,"message": "New Password does not match with the confirm password."}, 400
            from manager.auth_manager import encode_password
            if "username" in session:
                execution_status = self.__update_admin_password__(session["username"], encode_password(new_password))
                if not execution_status:
                    return {"status": ResponseStatus.FAILURE, "message": "Unable to update password. Please check the logs."}, 400
            else:
                return {"status": ResponseStatus.FAILURE, "message": "User does not exist in the session"}, 400 
            return {"status": ResponseStatus.SUCCESS, "message": "Password has been updated successfully"}, 200
        else:
            return {"status":ResponseStatus.FAILURE,"message": "User is not authenticated"}, 401
        
        
class AdminLogout(Resource):
    
    def __init__(self,app):
        self.app = app
        
    @auth_required     
    def get(self):
        if "authenticated" in session:
            session["authenticated"] = False
            [session.pop(key) for key in list(session.keys())]
        return make_response(render_template(ResourceTemplatesName.ADMIN_LOGIN, alert_message="You have been logged out!", alert_type="info"))
    

class AdminNotifier(Resource):
    
    def __init__(self,app):
        self.app = app
     
    @auth_required    
    def get(self):
        return make_response(render_template(ResourceTemplatesName.NOTIFICATION))
    
    def __add_notification__(self,notification_title,notification_message):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''DELETE FROM {table}
            '''.format(table=TableName.NOTIFICATION)
            sql_db_utils.execute_script(sql)
            sql ='''INSERT INTO {table} VALUES(?,?,?)
                '''.format(table=TableName.NOTIFICATION)
            sql_db_utils.execute_statement(sql,record=(notification_title, notification_message,0))
            return True
        except Error as e:
            print(e) #replace with the logger
            return False
        finally:
            close_db_connection(sql_db_utils) 
     
    @auth_required   
    def post(self):
        request_json = request.get_json()
        if request_json == None:
            return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
        validation = validate_fields(NOTIFICATION_FIELDS, request_json)
        if validation != None:
            return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
        notification_title = request_json["notificationTitle"]
        notification_message= request_json["notificationMessage"]
        if self.__add_notification__(notification_title,notification_message):
            return {"status": ResponseStatus.SUCCESS, "message": "Notification details have been added successfully"}, 200
        return {"status":ResponseStatus.FAILURE,"message": "Unable to add the notification details. Please check the logs"}, 500
        

class AdminControlNoticeDisplay(Resource):        
    
    def __init__(self,app):
        self.app = app
    
    @auth_required    
    def put(self,display_code=0):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''UPDATE {table}
                     SET IS_DISPLAYED = {0}
            '''.format(display_code,table=TableName.NOTIFICATION)
            sql_db_utils.execute_script(sql)
            if display_code == 0:
                return {"status": ResponseStatus.SUCCESS, "message": "Notification has been hidden successfully"}, 200
            elif display_code >0:
                return {"status": ResponseStatus.SUCCESS, "message": "Notification has been displayed successfully"}, 200
            else:
                return {"status":ResponseStatus.FAILURE,"message": "Invalid value provided by the user. is_displayed value must be either 0 or it must be greater than 0."}, 400
        except Error as e:
            print(e) #replace with the logger
            return {"status":ResponseStatus.FAILURE,"message": str(e)}, 500
        finally:
            close_db_connection(sql_db_utils) 
        