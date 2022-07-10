'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for dashboard page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''

from gc import collect
import random, string
from yaml import safe_load, YAMLError 
from factory import  sqllite_dict_factory
from . import ApplicationTableColumns
from . import Resource
from . import ResourceTemplatesName
from . import TableName
from . import TrackerColumns
from . import all_timezones, TIMESTAMP_FORMAT
from . import datetime, timezone as pytz_timezone, utc
from . import get_db_obj, close_db_connection
from . import make_response, render_template
from flask import request, current_app as app
from . import secure_filename, path, remove, flash
from . import validate_json

def get_task_details(app, app_name):
    """ Retrieves the details related to the tasks for displaying it over the dashboard page to the users.
    """
    try:
        sql_db_utils = get_db_obj(app)
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
                del record[TrackerColumns.RESUME_CODE]
                if record[TrackerColumns.JENKINS_JOB_URL] != None:
                    record.update( {"PROGRESS":jenkins_manager_obj.get_build_progress(record[TrackerColumns.JENKINS_JOB_URL])} )
        return all_records, None
    except Exception as err:
        app.logger.critical(err,exc_info=True)
        return [], err
    finally:
        close_db_connection(sql_db_utils)
        
class Dashboard(Resource):
    """ This resource allows the user to access the dashboard page having the details related to the tasks for the current application.
    """
    def __get_application_description__(self, app_details): 
        """ Fetches the application description from the database to display it on the dashboard page.
        """
        if app_details: return app_details[ApplicationTableColumns.DESCRIPTION]
        else: return "No Description Available"
     
    def __get_app_details__(self, app_name):
        try:
            sql_db_utils = get_db_obj(app)
            sql_db_utils.conn.row_factory = sqllite_dict_factory.dict_factory
            sql = '''
            select * from {app_table_name} where {app_name_column} = ? 
            '''.format(app_table_name=TableName.APP, app_name_column=ApplicationTableColumns.NAME)
            sql_db_utils.execute_statement(sql, record=(app_name,))
            app_details =  sql_db_utils.get_cursor().fetchone()
            return app_details, None
        except Exception as err:
            app.logger.warning(err,exc_info=True)
            return [], err
        finally:
            close_db_connection(sql_db_utils)
          
    def get(self, app_name):
        """ Displays the application details and base page to the user without task details
        """
        try:
            app_details,app_description,response_obj,warn_msg = (None,None,None,None)
            app_details, err = self.__get_app_details__(app_name)
            if err: warn_msg = "Unable to fetch application details. Please contact administrator."
            app_description = self.__get_application_description__(app_details)
            from config import JENKINS
            if app_details or err: response_obj = make_response(render_template(ResourceTemplatesName.DASHBOARD_PAGE,jenkins_server_url=JENKINS["SERVER_URL"],app_name=app_name,app_description=app_description,warn_msg=warn_msg),200)
            else: response_obj = make_response(render_template(ResourceTemplatesName.ERROR_404_PAGE),404)
            return response_obj
        finally:
            del app_details
            del app_description
            del response_obj
    
class DashboardTasks(Resource):
    """ Displays the task details in a div container of the parent dashboard page.
    """
    def get(self,app_name):
        try:
            timezone = request.args.get('timezone', "UTC", type=str)
            err_msg=None
            task_details, err = get_task_details(app,app_name)
            if timezone != "UTC" and timezone in all_timezones:
                for data in task_details:
                    data[TrackerColumns.EXECUTION_TIMESTAMP]=datetime.strptime(data[TrackerColumns.EXECUTION_TIMESTAMP],TIMESTAMP_FORMAT).replace(tzinfo=utc).astimezone(pytz_timezone(timezone)).strftime(TIMESTAMP_FORMAT)
            if err: err_msg = "Unable to fetch task details for the current application. Please contact administrator"
            return make_response(render_template(ResourceTemplatesName.TASK_TEMPLATE, task_details=task_details,timezone=timezone,err_msg=err_msg),200)
        except Exception as e:
            print(e)
        finally:
            del task_details
            collect()
            
class DeploymentFlow(Resource):
    ALLOWED_EXTENSIONS = {'yaml',"YAML","yml","YML"}
    
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in DeploymentFlow.ALLOWED_EXTENSIONS
               
    def post(self, app_name):
        try:
            from . import  redirect
            if 'file' not in request.files:
                flash('No selected file')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                try:
                    with open(filepath) as f:
                        yaml_data = safe_load(f)
                except YAMLError as e:
                    flash_error = ""
                    flash_error += "Error while parsing YAML file:\n"
                    if hasattr(e, 'problem_mark'):
                        if e.context != None:
                            flash_error += '  Error says\n' + str(e.problem_mark) + '\n  ' + \
                                str(e.problem) + ' ' + str(e.context) + \
                                '\nPlease correct data and retry.'
                        else:
                            flash_error += '  parser says\n' + str(e.problem_mark) + '\n  ' + \
                                str(e.problem) + '\nPlease correct data and retry.'
                    else:
                        flash_error +=  "Something went wrong while parsing yaml file: " + str(e)
                    flash(flash_error)
                    return redirect(request.url) 
                if f.closed:
                    remove(filepath)     
                status, err_msgs = validate_json(yaml_data)
                if status:
                    task_data = [ {
                        task_data["name"]:
                            {   "is_skip": task_data["skip"] if "skip" in task_data else False, 
                                "is_pause": True if task_data["config"] == "pause" else False,
                                "is_monitor": task_data["monitor"] if "monitor" in task_data else True,
                                "category":  task_data["category"] if "category" in task_data else "Unknown",
                                "is_failure_allowed": task_data["allow_failure"] if "allow_failure" in task_data else False,
                            }
                           
                        } 
                    for task_data in yaml_data["tasks"]  ]
                
                    
                    task_data_len = len(task_data)
                    indexes = []
                    def get_random_ids():
                        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                    for index in range(0,task_data_len):
                        random_index = get_random_ids()
                        while random_index in indexes:
                            random_index = get_random_ids()
                        indexes.append(random_index)
                        for _, details in task_data[index].items():
                            details.update({"index":random_index})
                    return make_response(render_template(ResourceTemplatesName.DEPLOYMENT_FLOW,app_name=app_name, task_data=task_data,error=status),200)
                return make_response(render_template(ResourceTemplatesName.DEPLOYMENT_FLOW,app_name=app_name,error=status,err_messages=err_msgs),200)
            else:
                flash('Only YAML Files are allowed!')
                return redirect(request.url)
        except Exception as e:
            flash("Some error occurred while proceeding with the creation of deployment flow automatically!")
            app.logger.warning(e,exc_info=True)
        
        
        
    def get(self, app_name):  
        return make_response(render_template(ResourceTemplatesName.DEPLOYMENT_FLOW,app_name=app_name),200)