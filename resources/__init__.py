from datetime import datetime
from os import path, remove
from sqlite3 import Error

from flask import render_template, make_response, redirect, url_for, flash, send_file
from flask_restful import Resource
from pytz import all_timezones, timezone, utc
from werkzeug.utils import secure_filename

from config import DB
from manager.auth_manager import decode_password, auth_required
from manager.vars_manager import LICENSE_FILE, ResourceTemplatesName, BlazeUrls, AuthenticationTableColumns, TableName, ResponseStatus, ApplicationTableColumns, TrackerColumns, ExecutionStatus, RemoveTrackerColumns, BuildQueueColumns
from support.taskbook_schema_validator import validate_json
from utilities.sqlite_db_utils import SQLLiteUtils


DATABASE_NAME = "{}.db".format(DB["DATABASE_NAME"])
TIMESTAMP_FORMAT = "%d-%m-%Y %H:%M:%S %p"

def verify_error_response(obj, status_code, error_title, error_description):
    if isinstance(obj, Exception):
        return make_response(render_template(ResourceTemplatesName.ERROR_PAGE,status_code=status_code,error_title=error_title,error_description=error_description))
    
def get_db_obj(app):
    sql_db_utils = SQLLiteUtils(app)
    sql_db_utils.create_connection(DATABASE_NAME)
    return sql_db_utils

def close_db_connection(sql_db_utils): 
    if sql_db_utils:
        if sql_db_utils.conn:
            sql_db_utils.conn.close()
        del sql_db_utils
        
def validate_fields(required_fields, json_data):
    for required_field in required_fields:
        if required_field not in json_data:
            return "Value for the {} field is missing!".format(required_field)
        
        
def get_license():
    if path.exists(LICENSE_FILE):
        with open(LICENSE_FILE) as license_text:
            return license_text.read()
    else:
        return "LICENSE is not available. Please contact the author immediately to get the new license."