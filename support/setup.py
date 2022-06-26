'''
Created on 08-May-2022

@author: Abhishek Prajapati
'''

from manager.vars_manager import TableName, TrackerColumns, ApplicationTableColumns, RemoveTrackerColumns, AuthenticationTableColumns, NotificationColumns

def get_setup_statements():
    from manager.auth_manager import encode_password
    setup_statements = [
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {app_name} CHAR(20) NOT NULL,
           {task_name} VARCHAR (255) NOT NULL ,
           {job_url} VARCHAR (255),
           {execution_id} CHAR (20),
           {execution_status} VARCHAR (255) NOT NULL,
           {timestamp} VARCHAR (255) NOT NULL,
           {start_time} VARCHAR (255),
           {end_time} VARCHAR (255),
           {secret} CHAR(20),
           {job_name} VARCHAR (255),
           PRIMARY KEY ({app_name}, {task_name})
        )'''.format(
            table=TableName.TRACKERS,
            app_name=TrackerColumns.APP_NAME,
            task_name=TrackerColumns.TASK_NAME,
            job_url=TrackerColumns.JENKINS_JOB_URL,
            execution_id=TrackerColumns.JENKINS_JOB_ID,
            execution_status=TrackerColumns.EXECUTION_STATUS,
            timestamp=TrackerColumns.EXECUTION_TIMESTAMP,
            start_time=TrackerColumns.EXECUTION_START_TIME,
            end_time=TrackerColumns.EXECUTION_END_TIME,
            secret=TrackerColumns.RESUME_CODE,
            job_name=TrackerColumns.JENKINS_JOB_NAME
        ),
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {app_name} CHAR(20) NOT NULL PRIMARY KEY,
           {description} VARCHAR (255) NOT NULL ,
           {email} VARCHAR (255) NOT NULL
        )'''.format(
            table=TableName.APP,
            app_name= ApplicationTableColumns.NAME,
            description=ApplicationTableColumns.DESCRIPTION,
            email=ApplicationTableColumns.EMAIL_IDS
        ),
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {app_name} CHAR(20) NOT NULL PRIMARY KEY,
           {secret} CHAR(10) NOT NULL
        )'''.format(
            table=TableName.REMOVE_TRACKER,
            app_name=RemoveTrackerColumns.APP_NAME,
            secret=RemoveTrackerColumns.SECRET_CODE
        ),
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {username} TEXT NOT NULL PRIMARY KEY,
           {password} TEXT NOT NULL
        )'''.format(
            table=TableName.AUTH,
            username=AuthenticationTableColumns.USERNAME,
            password=AuthenticationTableColumns.PASSWORD
        ),
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {title} TEXT NOT NULL,
           {message} TEXT NOT NULL,
           {is_displayed} INTEGER  NOT NULL
        )'''.format(
            table=TableName.NOTIFICATION,
            title=NotificationColumns.HEADING,
            message=NotificationColumns.MESSAGE,
            is_displayed=NotificationColumns.IS_DISPLAYED
        ),
        
        '''CREATE TABLE IF NOT EXISTS {table}(
           {id} INTEGER PRIMARY KEY CHECK (ID = 0),
           {is_queue_paused} INTEGER NOT NULL
        )'''.format(
            table="BUILD_QUEUE",
            id="ID",
            is_queue_paused="IS_QUEUE_PAUSED",
        ),
         '''INSERT OR IGNORE INTO {table} VALUES(0,0)'''.format(table="BUILD_QUEUE"),
        '''INSERT OR IGNORE INTO {table} VALUES("admin","{secret}")'''.format(table=TableName.AUTH,secret=encode_password("admin")),
        
        ]
    
    return setup_statements