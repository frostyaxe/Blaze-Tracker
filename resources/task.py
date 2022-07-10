'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the task details.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****
'''

from . import Resource, get_db_obj, Error,close_db_connection, ApplicationTableColumns, TableName, TrackerColumns, ResponseStatus, ExecutionStatus, TIMESTAMP_FORMAT
from . import validate_fields
from manager.auth_manager import api_auth_required
from flask import current_app as app, request

execution_statuses = [ var for var in vars(ExecutionStatus).values() if type(var) == str and var.isupper() ]

class VerifyTaskAuth(Resource):
    """    
    """
    @api_auth_required
    def get(self): return {"status":ResponseStatus.SUCCESS,"message":"client is authenticated!"}


class VerifyQueuePaused(object):
    """    Verify the status of the queue pause
    """
    def __init__(self, sql_db_utils):
        self.sql_db_utils=sql_db_utils
        
    def verify_pause_queued(self,close_connection=True):
        try:
            sql = '''
                SELECT IS_QUEUE_PAUSED FROM {table} WHERE {ID} = ? 
                '''.format(table="BUILD_QUEUE", ID="ID")
            record=self.sql_db_utils.execute_statement(sql,record=(0,)).fetchone()
            if record != None and len(record) > 0:
                value = record[0]
                if value > 0: return { "status" : ResponseStatus.ERROR, "message" : "Unable to place the request in queue! Please contact administrator." }, 503
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return { "status" : ResponseStatus.ERROR, "message" : "Unable to verify the queue pause. Please contact administrator." }, 500
        finally:
            if close_connection: close_db_connection(self.sql_db_utils)   

class QueuePaused(Resource):
    
    def get(self): return VerifyQueuePaused(get_db_obj(app)).verify_pause_queued()
            
class AddTask(Resource):
    """    Resource to handle the task addition in the database
    """
    required_fields = [ "task_name", "master_job_name", "status"  ]
    
    def __get_recipients_ids__(self, app_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql = '''
            SELECT {email} FROM {table} WHERE {app_name} = ? 
            '''.format(email=ApplicationTableColumns.EMAIL_IDS,table=TableName.APP, app_name=ApplicationTableColumns.NAME)
            record=sql_db_utils.execute_statement(sql,record=(app_name,)).fetchone()
            return record, None
        except Error as e:
            app.logger.critical(e,exc_info=True)
            return None, e
        finally:
            close_db_connection(sql_db_utils)
            
    
    def __insert_task_details__(self, app_name, task_details):
        try:
            from datetime import datetime
            sql_db_utils = get_db_obj(app)
            result = VerifyQueuePaused(sql_db_utils).verify_pause_queued(close_connection=False)
            if result: return result
            sql = ''' INSERT OR IGNORE INTO {table}({app},{task},{url},{job_id},{status},{timestamp},{start},{end},{secret},{job_name})
                  VALUES(?,?,?,?,?,?,?,?,?,?) '''.format(
                      table=TableName.TRACKERS,
                      app=TrackerColumns.APP_NAME,
                      task=TrackerColumns.TASK_NAME,
                      url=TrackerColumns.JENKINS_JOB_URL,
                      job_id=TrackerColumns.JENKINS_JOB_ID,
                      status=TrackerColumns.EXECUTION_STATUS,
                      timestamp=TrackerColumns.EXECUTION_TIMESTAMP,
                      start=TrackerColumns.EXECUTION_START_TIME,
                      end=TrackerColumns.EXECUTION_END_TIME,
                      secret=TrackerColumns.RESUME_CODE,
                      job_name=TrackerColumns.JENKINS_JOB_NAME
                      )
            task_name = task_details["task_name"]
            from re import match
            pattern="^[A-Za-z\d\-_\s]+$"
            if not match(pattern, task_name): return  { "status" : ResponseStatus.FAILURE, "message" : "Task name must contain alphabets, numbers, spaces, underscores and hyphen. Current Value: {0}".format(task_name) }, 400
            status = task_details["status"].upper()
            if status not in execution_statuses: return  { "status" : ResponseStatus.FAILURE, "message" : "Invalid status - {0}. Valid statuses are {1}".format(status,', '.join(execution_statuses)) }, 400
            timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
            job_url,end_time,code = (None, None, None)
            job_id = "NA"
            if "job_url" in task_details: job_url = task_details["job_url"]
            if "job_id" in task_details: job_id = task_details["job_id"]
            master_job_name = task_details["master_job_name"]
            if status == ExecutionStatus.RESUMED: return { "status" : ResponseStatus.FAILURE, "message" : "You can't add the resumed task without pausing the pipeline." }, 403
            if status == ExecutionStatus.PAUSED:
                from support.secret_code_generator import get_code
                code = get_code()
                start_time = timestamp
                recipients, err = self.__get_recipients_ids__(app_name)
                if err: return { "status" : ResponseStatus.ERROR, "message" : "Unable to retrieve recipient IDs. Please contact administrator." }, 500
                from manager.notification_manager import SendEmailNotification
                email_notifier = SendEmailNotification()
                email_notifier.subject = "[ {0} ] Pipeline execution has been paused (Blaze)".format(app_name)
                email_notifier.template_name = "pause_resume.j2"
                email_notifier.receiver = list(recipients) + email_notifier.receiver
                email_notifier.vars = { "pause_time":start_time, "pause_code": code, "task_name": task_name,"tracker_url":request.root_url,"app_name":app_name }
                email_notifier.send_email()
            if status == ExecutionStatus.RUNNING: start_time = timestamp
            if status == ExecutionStatus.SUCCESS or status == ExecutionStatus.FAILURE: end_time = timestamp
            sql_db_utils.execute_statement(sql, record=(app_name, task_name,job_url,job_id, status, timestamp, start_time, end_time, code, master_job_name ))
            return  { "status" : ResponseStatus.SUCCESS, "message" : "Task details has been inserted successfully. It could be ignored if data already exists." }, 200
        except Error as e:
            app.logger.critical(e,exc_info=True)
            raise Error(e)
        finally:
            close_db_connection(sql_db_utils)
            
    @api_auth_required        
    def post(self, app_name):
        try:
            request_json = request.get_json()
            if request_json == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(AddTask.required_fields,request_json)
            if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            return self.__insert_task_details__(app_name, request_json)
        except Exception as e:
            app.logger.critical(e,exc_info=True)
            return { "status" : ResponseStatus.ERROR, "message" : "Unable to insert task details. Please contact administrator." }, 500

class UpdateTaskStatus(Resource):
    """    Resource to handle the task status update based on the inputs received.
    """
    required_fields = [ "taskName", "status" ]
    
    def __update_task__(self, app_name, task_name, status):
        """    Updates the status of the task based on the inputs received
        """
        try:
            from datetime import datetime
            timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
            sql_db_utils = get_db_obj(app)
            end_time = None
            if status == ExecutionStatus.SUCCESS or status == ExecutionStatus.FAILURE or status == ExecutionStatus.RESUMED:  end_time = timestamp
            sql ='''UPDATE {table}
                    SET {status} = "{}",
                        {timestamp} = "{}",
                        {end_time} = "{}"
                    WHERE EXISTS (SELECT *
                          FROM {table}
                          WHERE {app_name} = "{}"
                          AND {task} = "{}")  AND ({app_name} = "{}" AND {task} = "{}"
                )'''.format(status,timestamp,end_time,app_name, task_name,app_name, task_name,
                            table=TableName.TRACKERS, 
                            status=TrackerColumns.EXECUTION_STATUS,
                            timestamp=TrackerColumns.EXECUTION_TIMESTAMP,
                            app_name=TrackerColumns.APP_NAME,
                            task=TrackerColumns.TASK_NAME,
                            end_time=TrackerColumns.EXECUTION_END_TIME
                        )
            sql_db_utils.execute_script(sql)
        except Error as e:
            app.logger.critical(e,exc_info=True)
            return e
        finally:
            close_db_connection(sql_db_utils)
    
    @api_auth_required   
    def put(self, app_name):
        try:
            request_json = request.get_json()
            if request_json == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(UpdateTaskStatus.required_fields, request_json)
            if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            task_name = request_json["taskName"]
            status = request_json["status"]
            if status not in execution_statuses: return  { "status" : ResponseStatus.FAILURE, "message" : "Invalid status - {0}. Valid statuses are {1}".format(status,', '.join(execution_statuses)) }, 400
            if status.upper() == ExecutionStatus.RESUMED: return { "status" : ResponseStatus.FAILURE, "message" : "Nice try but you can't resume the paused pipeline without code." }, 403
            err = self.__update_task__(app_name, task_name, status)
            if err: raise Exception(err)
            return { "status" : ResponseStatus.SUCCESS, "message" : "Status for the given task has been updated successfully to {1} : Task: {0}".format(task_name, status) }, 200
        except Exception as e:
            app.logger.critical(e,exc_info=True)
            return { "status" : ResponseStatus.ERROR, "message" : "Unable to update task details. Please contact administrator." }, 500
        
        
class GetTaskStatus(Resource):        
    """    Resource to retrieve the status of the task based on the inputs received.
    """
    def __get_task_status__(self, app_name,task_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql = '''
            SELECT {status} FROM {table} WHERE {app_name} = ? AND TASK_NAME = ?
            '''.format(status=TrackerColumns.EXECUTION_STATUS,table=TableName.TRACKERS,app_name=TrackerColumns.APP_NAME,task=TrackerColumns.TASK_NAME)
            record=sql_db_utils.execute_statement(sql,record=(app_name,task_name)).fetchone()
            return record, None
        except Error as e:
            app.logger.critical(e,exc_info=True)
            return None, e
        finally:
            close_db_connection(sql_db_utils)
    
    def get(self, app_name, task_name):
        try:
            status, err = self.__get_task_status__(app_name, task_name)
            if err: return { "status": ResponseStatus.ERROR, "message" : "Unable to insert task details. Please contact administrator." }, 500
            if status == None: return {"status": ResponseStatus.FAILURE,"message":"Task does not exist with the given name in Tracker details"}, 404
            else: return {"status": ResponseStatus.SUCCESS,"message": "Task exists with the given name in Tracker details", "execution_status":status[0]}, 200
        except Exception as e: app.logger.warning(e,exc_info=True)
            
        
class GetTaskJobId(Resource):        
    """    Resource to retrieve the task job ID based on the name of the task received.
    """
    def __get_job_id__(self, app_name,task_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql = '''
            SELECT {job_id} FROM {table} WHERE {app_name} = ? AND {task_name} = ?
            '''.format(job_id=TrackerColumns.JENKINS_JOB_ID, table=TableName.TRACKERS, app_name=TrackerColumns.APP_NAME, task_name=TrackerColumns.TASK_NAME)
            record=sql_db_utils.execute_statement(sql,record=(app_name,task_name)).fetchone()
            return record, None
        except Error as e:
            app.logger.critical(e,exc_info=True)
            return None, e
        finally:
            close_db_connection(sql_db_utils)
    
    def get(self, app_name, task_name):
        try:
            job_id,err = self.__get_job_id__(app_name, task_name)
            if err: raise Exception(err)
            if job_id == None: return {"status": ResponseStatus.FAILURE,"message":"Task does not exist with the given name in Tracker details"}, 404
            else: return {"status": ResponseStatus.SUCCESS,"message": "Task exists with the given name in Tracker details", "job_id":int(job_id[0])}, 200
        except Exception as e:
            app.logger.critical(e,exc_info=True)
            return { "status": ResponseStatus.ERROR, "message" : "Unable to get the job id. Please contact administrator." }, 500
        
class UpdateJobId(Resource):
    """    Resource to handle the update of job ID based on the application name and task name.
    """
    required_field = [ "taskName", "job_id"  ]
    
    def __update_jobId__(self, app_name, task_name, job_id):
        try:
            from datetime import datetime
            timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
            sql_db_utils = get_db_obj(app)
            sql ='''UPDATE {table}
                    SET {job_id} = "{}",
                        {timestamp} = "{}"
                    WHERE EXISTS (SELECT *
                          FROM {table}
                          WHERE {app_name} = "{}"
                          AND {task_name} = "{}")  AND ({app_name} = "{}" AND {task_name} = "{}"
                )'''.format(job_id,timestamp,app_name, task_name,app_name, task_name,
                            table=TableName.TRACKERS,
                            job_id=TrackerColumns.JENKINS_JOB_ID,
                            timestamp=TrackerColumns.EXECUTION_TIMESTAMP,
                            app_name=TrackerColumns.APP_NAME,
                            task_name=TrackerColumns.TASK_NAME
                            )
            sql_db_utils.execute_script(sql)
        except Error as e: return e
        finally: close_db_connection(sql_db_utils)
    
    @api_auth_required
    def put(self, app_name):
        try:
            request_json = request.get_json()
            if request_json == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(UpdateJobId.required_fields, request_json)
            if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            task_name = request_json["taskName"]
            job_id = request_json["job_id"]
            err=self.__update_jobId__(app_name, task_name, job_id)
            if err: raise Exception(err)
            return { "status" : ResponseStatus.SUCCESS, "message" : "Job ID for the given task has been updated successfully to {1} : Task: {0}".format(task_name, job_id) }, 200
        except Exception as e:
            app.logger.critical(e,exc_info=True)
            return { "status": ResponseStatus.ERROR, "message" : "Unable to update the job id. Please contact administrator." }, 500
        
class DeleteTask(Resource):
    """    Removes the task from the database based on the name of the application and task name
    """
    required_fields = [ "taskName" ]

    def __delete_task_details__(self, app_name, task_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql ='''DELETE FROM {table}
                    WHERE EXISTS (SELECT *
                          FROM {table}
                          WHERE {app_name} = "{}"
                          AND {task} = "{}")  AND ({app_name} = "{}" AND {task} = "{}"
                )'''.format(app_name, task_name,app_name, task_name,table=TableName.TRACKERS,app_name=TrackerColumns.APP_NAME,task=TrackerColumns.TASK_NAME)
            
            sql_db_utils.execute_script(sql)
        except Error as e:
            app.logger.critical(e,exc_info=True)
            return e
        finally: close_db_connection(sql_db_utils)
    
    @api_auth_required        
    def delete(self, app_name):
        try:
            request_json = request.get_json()
            if request_json == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation = validate_fields(DeleteTask.required_fields, request_json)
            if validation: return {"status" : ResponseStatus.FAILURE, "message" : validation}, 400
            task_name = request_json["taskName"]
            err = self.__delete_task_details__(app_name, task_name)
            if err: raise Exception(err)
            return { "status" : "success", "message" : "The given task has been deleted successfully. Task: {0}".format(task_name) }, 200
        except Exception as e:
            app.logger.critical(e,exc_info=True)
            return { "status": ResponseStatus.ERROR, "message" : "Unable to delete the task details. Please contact administrator." }, 500