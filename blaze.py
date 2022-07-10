'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Execution of the tasks from the taskbook YAML file using master & worker configuration
          This framework is compatible with the Jenkins only. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

__author__ = "Abhishek Prajapati"
__copyright__ = "Copyright (C) 2022 Abhishek Prajapati"
__license__ = "GNU AFFERO GENERAL PUBLIC LICENSE V3.0"
__version__ = "1.0"


# Dependencies import will be done below

from flask import Flask, render_template, request
from flask_restful import Api
from resources.index import Index
from resources.dashboard import Dashboard,DashboardTasks, DeploymentFlow
from resources.registration import Registration, UpdateRegistrationDetails
from resources.task import AddTask, UpdateTaskStatus, GetTaskStatus, GetTaskJobId, UpdateJobId, DeleteTask, VerifyTaskAuth, QueuePaused
from resources.resume import ResumeResource
from resources.admin import AdminLogin, AdminHome, AdminPasswordChange, AdminLogout, AdminNotifier, AdminControlNoticeDisplay
from resources.tracker import TrackerRemove, RemoveCode
from resources.build_queue import ManageBuildQueue, DisplayBuildQueue
from resources.unregistration import Unregistration
from resources.update_application import UpdateApplication,GetAppDetails
from resources.license import License
from resources.about import About
from resources.report import Report
from resources.current_running_tasks import CurrentRunningTasks, FetchRunningTasks
from secrets import token_hex
from datetime import timedelta
from manager.vars_manager import BlazeUrls, ResourceTemplatesName, NotificationColumns
from logging.config import dictConfig
from config import logger_dict_config
# Initialization of the variables
app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
api = Api(app)
dictConfig(logger_dict_config)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Adding index resource
api.add_resource(Index, BlazeUrls.INDEX)

# Adding registration and unregistration resources
api.add_resource(Registration, BlazeUrls.REGISTRATION)
api.add_resource(Unregistration, BlazeUrls.UNREGISTRATION)

# Adding resources related to the dashboard view
api.add_resource(Dashboard, BlazeUrls.DASHBOARD_PAGE)
api.add_resource(DashboardTasks, BlazeUrls.DASHBOARD_GET_TASKS)
api.add_resource(ResumeResource, BlazeUrls.DASHBOARD_RESUME_PIPELINE)

# Adding resources related to the task details retrieve and manipulation
api.add_resource(AddTask, BlazeUrls.ADD_TASK)
api.add_resource(UpdateTaskStatus, BlazeUrls.UPDATE_TASK_STATUS)
api.add_resource(GetTaskStatus, BlazeUrls.GET_TASK_STATUS)
api.add_resource(DeleteTask, BlazeUrls.DELETE_TASK)
api.add_resource(VerifyTaskAuth, BlazeUrls.VERIFY_TASK_AUTH)

# Adding resource to deal with job id
api.add_resource(GetTaskJobId,BlazeUrls.GET_TASK_JOB_ID)
api.add_resource(UpdateJobId, BlazeUrls.UPDATE_TASK_JOB_ID)

# Adding resources related to Admin details
api.add_resource(AdminLogin, BlazeUrls.ADMIN_LOGIN)
api.add_resource(AdminHome, BlazeUrls.ADMIN_HOME)
api.add_resource(AdminPasswordChange, BlazeUrls.ADMIN_PASSWORD_CHANGE)
api.add_resource(AdminLogout, BlazeUrls.ADMIN_LOGOUT)
api.add_resource(UpdateApplication, BlazeUrls.UPDATE_APPLICATION_DETAILS)
api.add_resource(UpdateRegistrationDetails, BlazeUrls.UPDATE_REGISTRATION_DETAILS)
api.add_resource(GetAppDetails, BlazeUrls.GET_APPLICATION_DETAILS)
api.add_resource(AdminNotifier, BlazeUrls.BLAZE_NOTIFIER)
api.add_resource(AdminControlNoticeDisplay, BlazeUrls.ADMIN_MANAGE_NOTICE)

# Adding resources related to handling the tracker removal process
api.add_resource(TrackerRemove, BlazeUrls.REMOVE_TRACKER_WITH_CODE)
api.add_resource(RemoveCode, BlazeUrls.GET_REMOVE_TRACKER_CODE)

# Adding resources to display license to the user.
api.add_resource(License, BlazeUrls.LICENSE_PAGE)

# Adding resources to display about page
api.add_resource(About, BlazeUrls.ABOUT)

# Adding resource to display the deployment flow based on the details present in YAML taskbook.
api.add_resource(DeploymentFlow, BlazeUrls.DEPLOYMENT_FLOW)

# Adding resources to handle the current running tasks dashboard page
api.add_resource(CurrentRunningTasks, BlazeUrls.DASHBOARD_CURRENT_TASKS)
api.add_resource(FetchRunningTasks, BlazeUrls.DASHBOARD_FETCH_RUNNING_TASKS)

# Adding resources to handle the pausing/resuming the build queue
api.add_resource(QueuePaused, BlazeUrls.GET_PAUSE_BUILD_QUEUE_STATUS)
api.add_resource(ManageBuildQueue, BlazeUrls.MANAGE_BUILD_QUEUE)
api.add_resource(DisplayBuildQueue, BlazeUrls.DISPLAY_BUILD_QUEUE)

api.add_resource(Report, BlazeUrls.REPORT)
def __set_up__():
    try:
        from utilities.sqlite_db_utils import SQLLiteUtils
        from config import DB
        from support.setup import get_setup_statements
        sql_db_utils = SQLLiteUtils(app)
        sql_db_utils.create_connection("{0}.db".format(DB["DATABASE_NAME"]))
        for statement in get_setup_statements():
            sql_db_utils.execute_statement(statement)
    except Exception as e:
        raise Exception(e)    
    finally:
        if sql_db_utils:
            if sql_db_utils.conn:
                sql_db_utils.conn.close()
   
def __validate_config__():
    from support.config_schema_validator import validate_config 
    validate_config()
    
def init():
    __validate_config__()
    __set_up__()
    
@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes['text/html']:
        return render_template(ResourceTemplatesName.ERROR_404_PAGE), 404
    return {"status":"failure","message":"Requested resource does not exist!"}, 404

@app.context_processor
def inject_dict_for_all_templates():
    try:
        from utilities.sqlite_db_utils import SQLLiteUtils
        from config import DB
        from factory.sqllite_dict_factory import dict_factory
        from manager.vars_manager import TableName
        sql_db_utils = SQLLiteUtils(app)
        sql_db_utils.create_connection("{0}.db".format(DB["DATABASE_NAME"]))
        sql_db_utils.conn.row_factory = dict_factory
        sql = '''
                select * from {notification_table}
              '''.format(notification_table=TableName.NOTIFICATION)
               
        sql_db_utils.execute_statement(sql)
        all_records =  sql_db_utils.get_cursor().fetchall()
        
        if all_records:
            data = all_records[-1]
            return dict({NotificationColumns.HEADING:data[NotificationColumns.HEADING],NotificationColumns.MESSAGE:data[NotificationColumns.MESSAGE],NotificationColumns.IS_DISPLAYED:data[NotificationColumns.IS_DISPLAYED]})
        else:
            return dict({NotificationColumns.IS_DISPLAYED:0})
    except Exception as e:
        print(e)
        return dict({NotificationColumns.IS_DISPLAYED:0})
    finally:
        if sql_db_utils:
            if sql_db_utils.conn:
                sql_db_utils.conn.close()
    

# Execution entry point

if __name__ == '__main__':
    init()
    app.run(debug=True,threaded=True)
