'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the Application details updates.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****
'''

from factory.sqllite_dict_factory import dict_factory
from . import Resource, render_template, make_response, auth_required, get_db_obj, close_db_connection, ResourceTemplatesName, TableName, ApplicationTableColumns, ResponseStatus
from flask import current_app as app

class UpdateApplication(Resource):
    
    @auth_required
    def get(self): return make_response(render_template(ResourceTemplatesName.UPDATE_APPLICATION))
    
class GetAppDetails(Resource):

    @auth_required
    def get(self,app_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql_db_utils.conn.row_factory = dict_factory
            sql = '''
            SELECT * FROM {table_name} WHERE {name} = ? 
            '''.format(table_name=TableName.APP, name=ApplicationTableColumns.NAME)
            sql_db_utils.execute_statement(sql, record=(app_name,))
            app_details =  sql_db_utils.get_cursor().fetchone()
            if app_details: return {"status": ResponseStatus.SUCCESS,"message":"Application details exist","details":app_details}, 200
            else: return {"status": ResponseStatus.FAILURE,"message":"Application details does not exist"}, 400
        except Exception as e:
            app.logger.critical(e,exc_info=True) 
            return {"status" : ResponseStatus.FAILURE, "message" : "Unable to get the application details. Please check logs."}, 500
        finally:
            close_db_connection(sql_db_utils)
    