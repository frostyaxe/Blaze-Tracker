'''
Created on 19-Jun-2022

@author: Abhishek Prajapati
'''
from . import Resource
from . import make_response
from . import render_template
from . import get_db_obj
from factory import sqllite_dict_factory
from . import TableName,TrackerColumns, close_db_connection, ExecutionStatus, ResourceTemplatesName
from flask import current_app as app

class CurrentRunningTasks(Resource):
    """ Serves the page to display the currently running tasks for all the applications.
    """
    def get(self):
        return make_response(render_template(ResourceTemplatesName.CURRENT_TASKS_PAGE_TEMPLATE))
    
    
class FetchRunningTasks(Resource):
    """ Fetches the Currently running tasks from the database and display the details to the user over currently running tasks page.
    """
    def __get_task_details__(self):
        """ Retrieves the task details from the database for all the applications to find the currently running tasks.
        """
        try:
            sql_db_utils = get_db_obj(app)
            sql_db_utils.conn.row_factory = sqllite_dict_factory.dict_factory
            sql = '''
            select * from {trackers_table_name} where {status_column}=? ORDER BY {start_time_column} DESC
            '''.format(trackers_table_name=TableName.TRACKERS,app_name_column=TrackerColumns.APP_NAME,status_column=TrackerColumns.EXECUTION_STATUS,start_time_column=TrackerColumns.EXECUTION_START_TIME)
            sql_db_utils.execute_statement(sql,record=(ExecutionStatus.RUNNING,))
            all_records =  sql_db_utils.get_cursor().fetchall()
            return all_records, None
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return [], err
        finally:
            close_db_connection(sql_db_utils)
            
    def get(self):
        task_details, err = self.__get_task_details__()
        err_msg= None
        if err: err_msg = "Unable to fetch the currently running tasks due to some error. Please contact administrator."
        return make_response(render_template(ResourceTemplatesName.CURRENT_TASK_TEMPLATE,task_details=task_details,err_msg=err_msg))