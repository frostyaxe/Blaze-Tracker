'''
Created on 19-Jun-2022

@author: Abhishek Prajapati
'''
from . import Resource
from . import make_response
from . import render_template
from . import get_db_obj
from factory import sqllite_dict_factory
from . import TableName,TrackerColumns, Error, close_db_connection, ExecutionStatus, ResourceTemplatesName

class CurrentRunningTasks(Resource):
    
    def __init__(self, app):
        self.app = app
        
    def get(self):
        return make_response(render_template(ResourceTemplatesName.CURRENT_TASKS_PAGE_TEMPLATE))
    
    
class FetchRunningTasks(Resource):
    
    def __init__(self, app):
        self.app = app
        
    def __get_task_details__(self):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql_db_utils.conn.row_factory = sqllite_dict_factory.dict_factory
            sql = '''
            select * from {trackers_table_name} where {status_column}=? ORDER BY {start_time_column} DESC
            '''.format(trackers_table_name=TableName.TRACKERS,app_name_column=TrackerColumns.APP_NAME,status_column=TrackerColumns.EXECUTION_STATUS,start_time_column=TrackerColumns.EXECUTION_START_TIME)
            sql_db_utils.execute_statement(sql,record=(ExecutionStatus.RUNNING,))
            all_records =  sql_db_utils.get_cursor().fetchall()
            return all_records
        except Error as e:
            print(e) #replace it with the logger
            return e
        finally:
            close_db_connection(sql_db_utils)
            
    def get(self):
        return make_response(render_template(ResourceTemplatesName.CURRENT_TASK_TEMPLATE,task_details=self.__get_task_details__()))