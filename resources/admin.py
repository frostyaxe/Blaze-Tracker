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
            # Field validation is missing!
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
        