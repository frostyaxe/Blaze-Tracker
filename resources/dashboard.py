'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for dashboard page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''

from . import Resource
from . import make_response, render_template
from factory import  sqllite_dict_factory
from . import Error
from . import get_db_obj, close_db_connection
from . import ResourceTemplatesName
from . import verify_error_response
from gc import collect
from . import ApplicationTableColumns
from . import TableName
from . import TrackerColumns

class Dashboard(Resource):
    
    def __init__(self, app):
        self.app = app
        
    def __get_application_description__(self, app_details): 
        if app_details:
            return app_details[ApplicationTableColumns.DESCRIPTION]
        else:
            return "No Description Available"
     
    def __get_app_details__(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql_db_utils.conn.row_factory = sqllite_dict_factory.dict_factory
            sql = '''
            select * from {app_table_name} where {app_name_column} = ? 
            '''.format(app_table_name=TableName.APP, app_name_column=ApplicationTableColumns.NAME)
            sql_db_utils.execute_statement(sql, record=(app_name,))
            app_details =  sql_db_utils.get_cursor().fetchone()
            return app_details
        except Error as e:
            print(e) #replace it with the logger
            return e
        finally:
            close_db_connection(sql_db_utils)
          
    def get(self, app_name):
        try:
            app_details = None
            app_description = None
            response_obj = None
            app_details = self.__get_app_details__(app_name)
            response_obj = verify_error_response(app_details,500,"INTERNAL SERVER ERROR","Unable to fetch the application details. Please check the logs.")
            if response_obj: return response_obj
            app_description = self.__get_application_description__(app_details)
            from config import JENKINS
            if app_details:
                response_obj = make_response(render_template(ResourceTemplatesName.DASHBOARD_PAGE,jenkins_server_url=JENKINS["SERVER_URL"],app_name=app_name,app_description=app_description),200)
            else:
                response_obj = make_response(render_template(ResourceTemplatesName.ERROR_404_PAGE),404)
            return response_obj
        finally:
            del app_details
            del app_description
            del response_obj
    
class DashboardTasks(Resource):
    
    def __init__(self, app):
        self.app = app

    def __get_task_details__(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql_db_utils.conn.row_factory = sqllite_dict_factory.dict_factory
            sql = '''
            select * from {trackers_table_name} where {app_name_column} = ? ORDER BY {start_time_column} 
            '''.format(trackers_table_name=TableName.TRACKERS,app_name_column=TrackerColumns.APP_NAME,start_time_column=TrackerColumns.EXECUTION_START_TIME)
            sql_db_utils.execute_statement(sql, record=(app_name,))
            all_records =  sql_db_utils.get_cursor().fetchall()
            if all_records:
                from manager.jenkins_manager import JenkinsManager
                from config import JENKINS
                jenkins_manager_obj = JenkinsManager(JENKINS["SERVER_URL"], JENKINS["USERNAME"], JENKINS["TOKEN"])
                for record in all_records:
                    if record[TrackerColumns.JENKINS_JOB_URL] != None:
                        record.update( {"PROGRESS":jenkins_manager_obj.get_build_progress(record[TrackerColumns.JENKINS_JOB_URL])} )
            return all_records
        except Error as e:
            print(e) #replace it with the logger
            return e
        finally:
            close_db_connection(sql_db_utils)
   
    def get(self,app_name):
        try:
            task_details = self.__get_task_details__(app_name)
            response_obj = verify_error_response(task_details,500,"INTERNAL SERVER ERROR","Unable to fetch the task details. Please check the logs.")
            if response_obj: return response_obj
            return make_response(render_template(ResourceTemplatesName.TASK_TEMPLATE, task_details=task_details),200)
        finally:
            del task_details
            collect()
        