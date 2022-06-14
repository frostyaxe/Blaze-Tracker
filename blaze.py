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
from resources.task import AddTask, UpdateTaskStatus, GetTaskStatus, GetTaskJobId, UpdateJobId, DeleteTask, VerifyTaskAuth
from resources.resume import ResumeResource
from resources.admin import AdminLogin, AdminHome, AdminPasswordChange, AdminLogout
from resources.tracker import TrackerRemove, RemoveCode
from resources.unregistration import Unregistration
from resources.update_application import UpdateApplication,GetAppDetails
from resources.license import License
from resources.about import About
from secrets import token_hex
from datetime import timedelta
from manager.vars_manager import BlazeUrls, ResourceTemplatesName

# Initialization of the variables
app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
api = Api(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Adding index resource
api.add_resource(Index, BlazeUrls.INDEX, resource_class_kwargs={'app': app})

# Adding registration and unregistration resources
api.add_resource(Registration, BlazeUrls.REGISTRATION, resource_class_kwargs={'app': app})
api.add_resource(Unregistration, BlazeUrls.UNREGISTRATION, resource_class_kwargs={'app': app})

# Adding resources related to the dashboard view
api.add_resource(Dashboard, BlazeUrls.DASHBOARD_PAGE,resource_class_kwargs={'app': app})
api.add_resource(DashboardTasks, BlazeUrls.DASHBOARD_GET_TASKS,resource_class_kwargs={'app': app})
api.add_resource(ResumeResource, BlazeUrls.DASHBOARD_RESUME_PIPELINE,resource_class_kwargs={'app': app})

# Adding resources related to the task details retrieve and manipulation
api.add_resource(AddTask, BlazeUrls.ADD_TASK,resource_class_kwargs={'app': app})
api.add_resource(UpdateTaskStatus, BlazeUrls.UPDATE_TASK_STATUS,resource_class_kwargs={'app': app})
api.add_resource(GetTaskStatus, BlazeUrls.GET_TASK_STATUS,resource_class_kwargs={'app': app})
api.add_resource(DeleteTask, BlazeUrls.DELETE_TASK,resource_class_kwargs={'app': app})
api.add_resource(VerifyTaskAuth, BlazeUrls.VERIFY_TASK_AUTH)

# Adding resource to deal with job id
api.add_resource(GetTaskJobId,BlazeUrls.GET_TASK_JOB_ID,resource_class_kwargs={'app': app})
api.add_resource(UpdateJobId, BlazeUrls.UPDATE_TASK_JOB_ID,resource_class_kwargs={'app': app})

# Adding resources related to Admin details
api.add_resource(AdminLogin, BlazeUrls.ADMIN_LOGIN, resource_class_kwargs={'app': app})
api.add_resource(AdminHome, BlazeUrls.ADMIN_HOME, resource_class_kwargs={'app': app})
api.add_resource(AdminPasswordChange, BlazeUrls.ADMIN_PASSWORD_CHANGE, resource_class_kwargs={'app': app})
api.add_resource(AdminLogout, BlazeUrls.ADMIN_LOGOUT, resource_class_kwargs={'app': app})
api.add_resource(UpdateApplication, BlazeUrls.UPDATE_APPLICATION_DETAILS, resource_class_kwargs={'app': app})
api.add_resource(UpdateRegistrationDetails, BlazeUrls.UPDATE_REGISTRATION_DETAILS, resource_class_kwargs={'app': app})
api.add_resource(GetAppDetails, BlazeUrls.GET_APPLICATION_DETAILS,resource_class_kwargs={'app': app})

# Adding resources related to handling the tracker removal process
api.add_resource(TrackerRemove, BlazeUrls.REMOVE_TRACKER_WITH_CODE, resource_class_kwargs={'app': app})
api.add_resource(RemoveCode, BlazeUrls.GET_REMOVE_TRACKER_CODE, resource_class_kwargs={'app': app})

# Adding resources to display license to the user.
api.add_resource(License, BlazeUrls.LICENSE_PAGE, resource_class_kwargs={'app': app})

# Adding resources to display about page
api.add_resource(About, BlazeUrls.ABOUT, resource_class_kwargs={'app': app})

# Adding resource to display the deployment flow based on the details present in YAML taskbook.
api.add_resource(DeploymentFlow, BlazeUrls.DEPLOYMENT_FLOW, resource_class_kwargs={'app': app})

def __set_up__():
    from utilities.sqlite_db_utils import SQLLiteUtils
    from config import DB
    from support.setup import get_setup_statements
    sql_db_utils = SQLLiteUtils(app)
    sql_db_utils.create_connection("{0}.db".format(DB["DATABASE_NAME"]))
    for statement in get_setup_statements():
        sql_db_utils.execute_statement(statement)
    
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

# Execution entry point

if __name__ == '__main__':
    init()
    app.run(debug=True,threaded=True)
