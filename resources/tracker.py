'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

@summary: Resource file for handling the removal of the trackers.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****
'''

from . import Resource, get_db_obj, TableName, RemoveTrackerColumns, Error, close_db_connection, ResponseStatus, ApplicationTableColumns
from manager.vars_manager import TrackerColumns

class TrackerRemove(Resource):
    
    def __init__(self, app):
        self.app = app
    
    def __get_tracker_code__(self, appName):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''
            SELECT {secret} FROM {table_name} WHERE {app_name} = ?
            '''.format(secret=RemoveTrackerColumns.SECRET_CODE,table_name=TableName.REMOVE_TRACKER,app_name=RemoveTrackerColumns.APP_NAME)
            record=sql_db_utils.execute_statement(sql,record=(appName,)).fetchone()
            return record, None
        except Error as e:
            return None, e
        finally:
            close_db_connection(sql_db_utils)
                
    def __delete_tracker_details__(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql ='''DELETE FROM {table_name}
                    WHERE EXISTS (SELECT *
                          FROM {table_name}
                          WHERE {app_name} = "{}" )  AND ({app_name} = "{}"
                )'''.format(app_name,app_name,table_name=TableName.TRACKERS,app_name=TrackerColumns.APP_NAME)
            sql_db_utils.execute_script(sql)
        except Error as e:
            return e
        finally:
            close_db_connection(sql_db_utils)
     
    def __delete_remove_tracker_code__(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql ='''DELETE FROM {table_name}
                    WHERE EXISTS (SELECT *
                          FROM {table_name}
                          WHERE {app_name} = "{}" )  AND ({app_name} = "{}"
                )'''.format(app_name,app_name, table_name=TableName.REMOVE_TRACKER, app_name=RemoveTrackerColumns.APP_NAME)
            
            sql_db_utils.execute_script(sql)
        except Error as e:
            return e
        finally:
            close_db_connection(sql_db_utils)
                
    def delete(self, app_name, code):
        record, err = self.__get_tracker_code__(app_name)
        if err: return {"status": ResponseStatus.ERROR, "message": "Unable to get the remove tracker code. Please contact administrator!"}, 500
        actual_code = None
        if record: 
            actual_code = record[0]
            if actual_code == code:
                err = self.__delete_tracker_details__(app_name)
                if err: return {"status": ResponseStatus.ERROR, "message": "Unable to delete the tracker details. Please contact administrator!"}, 500 
                err = self.__delete_remove_tracker_code__(app_name)
                if err: return {"status": ResponseStatus.ERROR, "message": "Unable to delete the remove tracker code. Please contact administrator!"}, 500 
                return {"status": ResponseStatus.SUCCESS, "message": "Removed the tracker details successfully!"}, 200
            else:
                return {"status": ResponseStatus.FAILURE, "message": "Provided code does not match with the actual code!"}, 400
        else:
            return {"status": ResponseStatus.FAILURE, "message": "Please generate the remove tracker code first!"}, 403
            
        

class RemoveCode(Resource):
    
    def __init__(self, app):
        self.app = app
        
    def __get_recipients_ids__(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''
            SELECT {email} FROM {table_name} WHERE {app_name} = ? 
            '''.format(email=ApplicationTableColumns.EMAIL_IDS, table_name=TableName.APP, app_name=ApplicationTableColumns.NAME)
            record=sql_db_utils.execute_statement(sql,record=(app_name,)).fetchone()
            return record, None
        except Error as e:
            return None, e
        finally:
            close_db_connection(sql_db_utils)
        
    def get(self, app_name):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''INSERT OR REPLACE INTO {table_name}({app_name},{secret})
                  VALUES(?,?)'''.format(table_name=TableName.REMOVE_TRACKER,app_name=RemoveTrackerColumns.APP_NAME,secret=RemoveTrackerColumns.SECRET_CODE)
            from support.secret_code_generator import get_code
            code = get_code()
            recipients, err = self.__get_recipients_ids__(app_name)
            if err: return {"status": ResponseStatus.ERROR, "message":"Unable to retrieve the recipients email ID. Please contact administrator."}, 500
            sql_db_utils.execute_statement(sql, record=(app_name, code ))
        except Error:
            return {"status": ResponseStatus.ERROR, "message":"Unable to add remove tracker code. Please contact administrator."}, 500
        finally:
            close_db_connection(sql_db_utils)

        from manager.notification_manager import SendEmailNotification
        email_notifier = SendEmailNotification()
        email_notifier.subject = "[ {0} ] Remove Tracker Request (Blaze)".format(app_name)
        email_notifier.template_name = "remove_tracker.j2"
        if len(recipients) > 0:
            email_notifier.receiver = recipients[0].split(",") + email_notifier.receiver
        else:
            return {"status": ResponseStatus.ERROR, "message": "Unable to find recipients. Please contact administrator."}, 500
        from flask import request
        email_notifier.vars = {"remove_tracker_code": code, "tracker_url":request.root_url,"app_name":app_name }
        email_notifier.send_email()  
        return {"status": ResponseStatus.SUCCESS, "message": "Code has been sent  to the following recipients -> \n{0}!".format('\n'.join([ email  for emails in email_notifier.receiver for email in emails.split(",")  ]))}
        