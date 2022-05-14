'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the unregistration of the applications.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****
'''

from . import Resource, render_template, make_response, auth_required, get_db_obj, close_db_connection, Error, ResourceTemplatesName, ResponseStatus, TableName, ApplicationTableColumns, validate_fields

class Unregistration(Resource):
    
    def __init__(self, app):
        self.app = app
    
    @auth_required
    def get(self):
        return make_response(render_template(ResourceTemplatesName.UNREGISTRATION_PAGE))
    
    @auth_required
    def delete(self):
        try:
            from flask import request
            db_utils_obj = get_db_obj(self.app)
            request_json = request.get_json()
            if request_json == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            required_fields = ["applicationName"]
            validation = validate_fields(required_fields,request_json)
            if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            application_name = request_json["applicationName"]
            if db_utils_obj.is_application_exist( application_name) == 0:
                return {"status" : ResponseStatus.FAILURE, "message" : "Application details does not exists!"}, 400
            sql = ''' DELETE FROM {table_name} WHERE {name} = ? '''.format(table_name=TableName.APP,name=ApplicationTableColumns.NAME)
            db_utils_obj.execute_statement(sql,record=(application_name,))
            return {"status": ResponseStatus.SUCCESS, "message":"Application has been unregistered successfully."}, 200
        except Error:
            return {"status" : ResponseStatus.FAILURE, "message" : "Unable to delete the application details. Please check logs."}, 500
        finally:
            close_db_connection(db_utils_obj)