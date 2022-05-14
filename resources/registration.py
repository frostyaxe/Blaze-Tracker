'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the registration details of the applications.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''
from . import Resource, render_template, make_response, auth_required, ResourceTemplatesName, Error, get_db_obj, close_db_connection, ResponseStatus, TableName, ApplicationTableColumns, validate_fields

required_fields = [ "applicationName","shortDescription","emailAddress" ]

class Registration(Resource):
    
    def __init__(self, app):
        self.app = app
    
    @auth_required
    def get(self):
        return make_response(render_template(ResourceTemplatesName.REGISTRATION_PAGE))
    
    @auth_required
    def post(self):
        try:
            from flask import request
            db_utils_obj = get_db_obj(self.app)
            request_json = request.get_json()
            if request_json == None:
                return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(required_fields, request_json)
            if validation != None:
                return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            application_name = request_json["applicationName"]
            short_description = request_json["shortDescription"]
            email_address = request_json["emailAddress"]
            try:
                if db_utils_obj.is_application_exist(application_name) == 1:
                    return {"status" : ResponseStatus.FAILURE, "message" : "Application details exists with the same name!"}, 409
                sql = ''' INSERT INTO {application_table_name}({name},{description},{email})
                      VALUES(?,?,?) '''.format(application_table_name=TableName.APP,name=ApplicationTableColumns.NAME,description=ApplicationTableColumns.DESCRIPTION,email=ApplicationTableColumns.EMAIL_IDS)
                db_utils_obj.execute_statement(sql,record=(application_name, short_description, email_address))
                return {"status": ResponseStatus.SUCCESS, "message":"Application has been registered successfully."}, 200
            except Error as e:
                print(e)    #Replace it with the logger
                return {"status" : ResponseStatus.FAILURE, "message" : "Unable to register the application at the moment. Please check logs."}, 500
        finally:
            close_db_connection(db_utils_obj)
            
class UpdateRegistrationDetails(Resource):
    
    def __init__(self, app):
        self.app = app
    
    @auth_required
    def put(self):
        try:
            from flask import request
            db_utils_obj = get_db_obj(self.app)
            request_json = request.get_json()
            if request_json == None:
                return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(required_fields, request_json)
            if validation != None:
                return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            application_name = request_json["applicationName"]
            short_description = request_json["shortDescription"]
            email_address = request_json["emailAddress"]
            try:
                if db_utils_obj.is_application_exist( application_name) == 0:
                    return {"status" : ResponseStatus.FAILURE, "message" : "Application details does not exists"}, 400
                sql = '''
                        UPDATE {app_table_name}
                        SET {description} = ?,
                            {emails} = ?
                        WHERE {name} = ?
                      '''.format(app_table_name=TableName.APP,description=ApplicationTableColumns.DESCRIPTION,emails=ApplicationTableColumns.EMAIL_IDS,name=ApplicationTableColumns.NAME)
                db_utils_obj.execute_statement(sql,record=(short_description, email_address,application_name))
            except Error as e:
                print(e)    #Replace it with the logger
                return {"status" : ResponseStatus.FAILURE, "message" : "Unable to update the registration details at the moment. Please check logs."}, 500
            return {"status": ResponseStatus.SUCCESS, "message":"Application details has been updated successfully."}, 200
        finally:
            close_db_connection(db_utils_obj)