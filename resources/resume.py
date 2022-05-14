'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the resumption of the paused pipeline.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''
from . import Resource, get_db_obj, Error, close_db_connection, TableName, TrackerColumns, ExecutionStatus, ResponseStatus, TIMESTAMP_FORMAT, validate_fields
from manager.jenkins_manager import JenkinsManager
from config import JENKINS
from factory.sqllite_dict_factory import dict_factory

class ResumeResource(Resource):
    
    required_fields = [ "resumeCode", "taskName" ]
    
    def __init__(self, app):
        self.app = app
        
    def __get_resume_code__(self, app_name, task_name): 
        try:
            sql_db_utils = get_db_obj(self.app)
            sql_db_utils.conn.row_factory = dict_factory
            sql = '''
            SELECT {secret} FROM {trackers_table} WHERE {name} = ? AND {task} = ? AND {status} = "{execution_status}"
            '''.format(
                trackers_table=TableName.TRACKERS,
                secret=TrackerColumns.RESUME_CODE,
                name=TrackerColumns.APP_NAME,
                task=TrackerColumns.TASK_NAME,
                status=TrackerColumns.EXECUTION_STATUS,
                execution_status=ExecutionStatus.PAUSED
                )
            sql_db_utils.execute_statement(sql, record=(app_name,task_name))
            app_details =  sql_db_utils.get_cursor().fetchone()
            if app_details:
                return app_details[TrackerColumns.RESUME_CODE], None
            else:
                return None, None
        except Error as e:
            return None, e
        finally:
            close_db_connection(sql_db_utils)
        
        
    def __update_paused_status__(self, app_name, task_name):
        try:
            from datetime import datetime
            timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
            sql_db_utils = get_db_obj(self.app)
            sql ='''UPDATE {table_name}
                    SET {status} = "{}",
                        {timestamp} = "{}",
                        {end_time} = "{}",
                        {secret} = null
                    WHERE EXISTS (SELECT *
                          FROM {table_name}
                          WHERE {name} = "{}"
                          AND {task_name} = "{}")  AND ({name} = "{}" AND {task_name} = "{}" AND {status} = "{execution_status}"
                )'''.format(
                    ExecutionStatus.RESUMED,timestamp,timestamp,app_name, task_name,app_name,task_name,
                    table_name=TableName.TRACKERS,
                    status=TrackerColumns.EXECUTION_STATUS,
                    timestamp=TrackerColumns.EXECUTION_TIMESTAMP,
                    end_time=TrackerColumns.EXECUTION_END_TIME,
                    secret=TrackerColumns.RESUME_CODE,
                    name=TrackerColumns.APP_NAME,
                    execution_status=ExecutionStatus.PAUSED,
                    task_name=TrackerColumns.TASK_NAME
                    )
            sql_db_utils.execute_script(sql)
        except Error as e:
            return e
        finally:
            close_db_connection(sql_db_utils)
        
    def __get_job_path__(self, app_name, task_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql_db_utils.conn.row_factory = dict_factory
            sql = '''
            SELECT {path} FROM {table_name} WHERE {app_name} = ? AND {task_name} = ? AND {execution_status} = "{paused}"
            '''.format(
                path=TrackerColumns.JENKINS_JOB_NAME,
                table_name=TableName.TRACKERS,
                app_name=TrackerColumns.APP_NAME,
                task_name=TrackerColumns.TASK_NAME,
                execution_status=TrackerColumns.EXECUTION_STATUS,
                paused=ExecutionStatus.PAUSED
                )
            sql_db_utils.execute_statement(sql, record=(app_name,task_name))
            app_details =  sql_db_utils.get_cursor().fetchone()
            if app_details:
                return app_details[TrackerColumns.JENKINS_JOB_NAME], None
            else:
                return None, None
        except Error as e:
            print(e)
            return None, e
        finally:
            close_db_connection(sql_db_utils)
            
    def post(self,app_name):
        from flask import request
        request_json = request.get_json()
        if request_json == None:
            return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
        validation = validate_fields(ResumeResource.required_fields, request_json)
        if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
        resume_code = request_json["resumeCode"]
        task_name = request_json["taskName"]
        db_resume_code, err = self.__get_resume_code__(app_name,task_name)
        if err:
            return  {"status": ResponseStatus.ERROR, "message": "Unable to retrieve the resume code for the verification. Please contact administrator."}, 500
        if db_resume_code:
            if db_resume_code == resume_code:
                job_path, err = self.__get_job_path__(app_name, task_name)
                if err:
                    return {"status": ResponseStatus.ERROR, "message": "Unable to retrieve the master job path. Please contact administrator."}, 500
                if job_path == None:
                    return  {"status": ResponseStatus.FAILURE, "message": "Unable to find the master Jenkins job path."}, 400
                jenkins_manager_obj = JenkinsManager(JENKINS["SERVER_URL"], JENKINS["USERNAME"], JENKINS["TOKEN"])
                queue_id, exception = jenkins_manager_obj.build_job(job_path)
                if exception == None:
                    if jenkins_manager_obj.verify_build_in_queue(queue_id):
                        err = self.__update_paused_status__(app_name, task_name)
                        if err:
                            return  {"status": ResponseStatus.ERROR, "message": "Unable to update the pause status after verification. Please contact administrator."}, 500
                        return {"status": ResponseStatus.SUCCESS, "message": "Execution has been resumed."}, 200
                    else:
                        return {"status": ResponseStatus.FAILURE,"message":"Executed job is not added in queue."}, 404
                else:
                    return {"status": ResponseStatus.FAILURE,"message":"Exception occurred. Reason: {0}".format(str(exception))}, 400
            else:
                return {"status": ResponseStatus.FAILURE,"message":"Provided code does not match with the actual code."}, 400
        else:
            return {"status": ResponseStatus.FAILURE,"message":"Either task has been resumed or name of the task/application is/are incorrect."}, 400
        
        
        
    