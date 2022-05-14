'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Manages the generic variables.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath("blaze.py"))
LICENSE_FILE = "LICENSE"

class BlazeUrls:
    # Path for index
    INDEX = '/'
    
    # Paths for application APIs
    REGISTRATION = '/application/registration'
    UNREGISTRATION =  '/application/unregistration'
    
    # Paths for dashboard APIs
    DASHBOARD_PAGE = '/<app_name>/view/dashboard'
    DASHBOARD_GET_TASKS = '/<app_name>/getTasks'
    DASHBOARD_RESUME_PIPELINE = '/<app_name>/task/resumePipeline'
    
    # Paths for task APIs
    ADD_TASK = '/<app_name>/task/add/details'
    UPDATE_TASK_STATUS = '/<app_name>/task/updateStatus'
    GET_TASK_STATUS = '/<app_name>/task/<task_name>/getStatus'
    DELETE_TASK = '/<app_name>/task/deleteTask'
    VERIFY_TASK_AUTH = '/task/verifyTaskAuthentication'
    
    # Paths for Job ID APIs
    GET_TASK_JOB_ID = '/<app_name>/task/<task_name>/getJobId'
    UPDATE_TASK_JOB_ID = '/<app_name>/task/updateJobId'
    
    # Paths for Admin APIs
    ADMIN_LOGIN = "/admin/login"
    ADMIN_HOME = '/admin/home'
    ADMIN_PASSWORD_CHANGE = '/admin/passwordChange'
    ADMIN_LOGOUT = '/admin/logout'
    UPDATE_APPLICATION_DETAILS = '/admin/applicationUpdate'
    UPDATE_REGISTRATION_DETAILS = '/admin/registrationUpdate'
    GET_APPLICATION_DETAILS = '/admin/<app_name>/getApplicationDetails'
    
    # Paths for Tracker Remove APIs
    REMOVE_TRACKER_WITH_CODE = '/<app_name>/removeTracker/<code>'
    GET_REMOVE_TRACKER_CODE = '/<app_name>/getRemoveTrackerCode'
    LICENSE_PAGE = '/license'
    ABOUT = "/about"
    
    
class ResourceTemplatesName:
    ADMIN_LOGIN = "admin_login.j2"
    ADMIN_BASE = "admin_base.j2"
    ADMIN_UPDATE_PASSWORD = "update_admin_pass_form.j2"
    DASHBOARD_PAGE = "dashboard.j2"
    ERROR_PAGE = "err.j2"
    ERROR_404_PAGE = "err_404.j2"
    TASK_TEMPLATE = "tasks.j2"
    INDEX_PAGE = "index.j2"
    REGISTRATION_PAGE = "registration.j2"
    UNREGISTRATION_PAGE = "unregistration.j2"
    UPDATE_APPLICATION = "update_application.j2"
    BLAZE_UPDATE_PASSWORD = "update_blaze_pass_form.j2"
    LICENSE_PAGE = "license.j2"
    ABOUT_PAGE = "about.j2"
    
class TableName:
    AUTH = "AUTHENTICATION"
    APP = "APPLICATION"
    REMOVE_TRACKER = "REMOVE_TRACKER"
    TRACKERS = "TRACKERS"

class AuthenticationTableColumns:
    PASSWORD = "PASSWORD"
    USERNAME = "USERNAME"
    
class ApplicationTableColumns:
    NAME = "APPLICATION_NAME"
    DESCRIPTION = "APPLICATION_DESCRIPTION"
    EMAIL_IDS = "NOTIFICATION_EMAIL_IDS"
    
class RemoveTrackerColumns:
    APP_NAME = "APPLICATION_NAME"
    SECRET_CODE = "CODE"
    
class TrackerColumns:
    APP_NAME = "APPLICATION_NAME"
    TASK_NAME = "TASK_NAME"
    JENKINS_JOB_URL = "JOB_URL"
    JENKINS_JOB_ID = "JOB_ID"
    EXECUTION_START_TIME = "START_TIME"
    EXECUTION_STATUS = "STATUS"
    EXECUTION_TIMESTAMP = "TIMESTAMP"
    RESUME_CODE = "CODE"
    EXECUTION_END_TIME = "END_TIME"
    JENKINS_JOB_NAME = "JOB_PATH"
    
class ResponseStatus:
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    
class ExecutionStatus:
    
    SUCCESS = "SUCCESS"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FAILURE = "FAILURE"
    RESUMED = "RESUMED"

    