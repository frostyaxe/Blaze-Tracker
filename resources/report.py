'''
Created on 26-Jun-2022

@author: Abhishek Prajapati
'''
from . import Resource, render_template, TrackerColumns, datetime,TIMESTAMP_FORMAT, ExecutionStatus, send_file, make_response, ResourceTemplatesName
from resources.dashboard import get_task_details
from flask import request
from pytz import all_timezones,utc,timezone as pytz_timezone
from datetime import timedelta
from io import BytesIO
from flask import current_app as app

class Report(Resource):
    """    Resource to handle the report feature.
    """
    def get(self, app_name):
        try:
            timezone = request.args.get('timezone', "UTC", type=str)
            task_details, _ = get_task_details(app,app_name)
            
            if timezone != "UTC" and timezone in all_timezones:
                for data in task_details: data[TrackerColumns.EXECUTION_TIMESTAMP]=datetime.strptime(data[TrackerColumns.EXECUTION_TIMESTAMP],TIMESTAMP_FORMAT).replace(tzinfo=utc).astimezone(pytz_timezone(timezone)).strftime(TIMESTAMP_FORMAT)
            total_tasks = len(task_details)
            total_success_tasks, total_failed_tasks, total_pause_tasks, total_all_execution_time, total_success_execution_time, total_failure_execution_time, total_pause_execution_time = (0, 0, 0, 0, 0, 0, 0)
            info_msg = None
            for task_data in task_details:
                
                time_difference = 0
                
                if task_data[TrackerColumns.EXECUTION_END_TIME] == None: end_time = datetime.utcnow().astimezone(pytz_timezone(timezone)).timestamp()
                else: end_time = datetime.strptime(task_data[TrackerColumns.EXECUTION_END_TIME],TIMESTAMP_FORMAT).timestamp()
                
                start_time = datetime.strptime(task_data[TrackerColumns.EXECUTION_START_TIME],TIMESTAMP_FORMAT).timestamp()
                
                if end_time:
                    time_difference = end_time - start_time
                    task_data["TIME_DIFF"] = str(timedelta(seconds=int(round(time_difference))))
                    total_all_execution_time += int(round(time_difference))
                
                if task_data[TrackerColumns.EXECUTION_STATUS] == ExecutionStatus.SUCCESS:
                    total_success_tasks += 1
                    if end_time: total_success_execution_time += int(round(time_difference))
                elif task_data[TrackerColumns.EXECUTION_STATUS] == ExecutionStatus.FAILURE:  
                    total_failed_tasks += 1
                    if end_time: total_failure_execution_time += int(round(time_difference))
                elif task_data[TrackerColumns.EXECUTION_STATUS] == ExecutionStatus.PAUSED or task_data[TrackerColumns.EXECUTION_STATUS] == ExecutionStatus.RESUMED:
                    total_pause_tasks  += 1
                    if end_time: total_pause_execution_time += int(round(time_difference))
                else: info_msg = "There might be an unknown or running task present. Please verify it on the Dashboard page."
            
            tasks_data = {'Task' : 'Task Count',"Total Successful Tasks":total_success_tasks,"Total Failed Tasks":total_failed_tasks,"Total Pauses":total_pause_tasks}
            execution_time_data = {'Task' : 'Execution Time',"Successful Tasks":{'v':total_success_execution_time,'f':str(timedelta(seconds=total_success_execution_time))},"Failed Tasks":{'v':total_failure_execution_time,'f':str(timedelta(seconds=total_failure_execution_time))},"Pause ":{'v':total_pause_execution_time,'f':str(timedelta(seconds=total_pause_execution_time))}}   
            response = render_template("report.j2",task_details=task_details,app_name=app_name,execution_time_data=execution_time_data,tasks_data=tasks_data,total_tasks=total_tasks,total_success_tasks=total_success_tasks,
                                                 total_failed_tasks=total_failed_tasks,total_pause_tasks=total_pause_tasks,info_msg=info_msg,total_all_execution_time=str(timedelta(seconds=total_all_execution_time)),
                                                 total_success_execution_time=str(timedelta(seconds=total_success_execution_time)),total_failure_execution_time=str(timedelta(seconds=total_failure_execution_time)),
                                                 total_pause_execution_time=str(timedelta(seconds=total_pause_execution_time))
                                                 )
            return send_file(BytesIO(bytes(response,"UTF-8")),download_name="{0}.html".format(app_name),as_attachment=True)
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return make_response(render_template(ResourceTemplatesName.ERROR_PAGE,500,"INTERNAL SERVER ERRROR","Unable to generate report due to some error. Please contact administrator."))
