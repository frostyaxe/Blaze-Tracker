'''
Created on 21-Jun-2022

@author: Abhishek Prajapati
'''
from . import Resource, auth_required, ResponseStatus, get_db_obj, TableName, close_db_connection, make_response, render_template,ResourceTemplatesName,BuildQueueColumns
from flask import current_app as app

class ManageBuildQueue(Resource):
    """ This resource manages the pausing and resuming the build queue based on the requirement.
    """
    
    @auth_required    
    def put(self,code=1):
        """    Handles the pause/resume of the build queue based on the request
        """
        try:
            sql_db_utils = get_db_obj(app)
            sql = '''UPDATE {table}
                     SET IS_QUEUE_PAUSED = {0}
                     WHERE ID = 0
            '''.format(code,table=TableName.BUILD_QUEUE)
            sql_db_utils.execute_script(sql)
            if code == 0:
                return {"status": ResponseStatus.SUCCESS, "message": "Build queue has been resumed successfully"}, 200
            elif code >0:
                return {"status": ResponseStatus.SUCCESS, "message": "Build queue has been paused successfully"}, 200
            else:
                return {"status":ResponseStatus.FAILURE,"message": "Invalid value provided by the user. code value must be either 0 or it must be greater than 0."}, 400
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return {"status":ResponseStatus.FAILURE,"message": str(err)}, 500
        finally:
            close_db_connection(sql_db_utils) 
            
class DisplayBuildQueue(Resource):
    """ Displays the current build queue status on the Admin page
    """
    @auth_required    
    def get(self):
        try:
            sql_db_utils = get_db_obj(app)
            status_code = 2
            sql = '''SELECT {queue_code_column} FROM {table} WHERE {id_column} = 0
                '''.format(queue_code_column=BuildQueueColumns.IS_QUEUE_PAUSED,table=TableName.BUILD_QUEUE,id_column=BuildQueueColumns.ID)
            status_code = sql_db_utils.execute_statement(sql).fetchone()
            if len(status_code) > 0: status_code = status_code[0]
            status = "Unknkown"
            if status_code == 0:  status = "Resumed"
            elif status_code == 1: status = "Paused"
            else: status = "Unknown"
            return make_response(render_template(ResourceTemplatesName.BUILD_QUEUE,status=status))
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return make_response(render_template(ResourceTemplatesName.BUILD_QUEUE,status="Unknown",err_msg="Unable to fetch the build queue details. Please check the logs."))
        finally:
            close_db_connection(sql_db_utils) 