'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Utilities class to handle the transactions related to the SQLLite DB.

Created on 11-April-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''
from . import Error, connect, version

class SQLLiteUtils(object):
    
    def __init__(self,app):
        self.app = app
        self.conn = None
        self.cursor = None
        
    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
       
        try:
            self.conn = connect(db_file,timeout=90)
            self.app.logger.info("Current Version of SQL lite is {0}".format(version))
            return self.conn, None
        except Error as e:
            self.app.logger.error("Error has been detected while creating sqllite db connection. Reason: {0}".format(e))
            return None, e
    

    def is_application_exist(self, application_name):
        response = self.conn.execute("SELECT EXISTS(SELECT * FROM APPLICATION WHERE APPLICATION_NAME='{application_name}')".format(application_name=application_name))
        return response.fetchone()[0] 
    
    
    def execute_statement(self, sql ,**options):
        #Creating table as per requirement
        
        self.cursor = self.conn.cursor()
        
        response = None
        
        if "record" in options:
            response = self.cursor.execute(sql, options["record"])
        else:
            response = self.cursor.execute(sql)
            
        self.app.logger.info("Statement execution is completed successfully........")

        # Commit your changes in the database
        self.conn.commit()
        
        return response
        
    def execute_script(self, sql ):
        #Creating table as per requirement
        
        self.cursor = self.conn.cursor()
        self.cursor.executescript(sql)
            
        self.app.logger.info("Statement execution is completed successfully........")

        # Commit your changes in the database
        self.conn.commit()

    def get_cursor(self):
        return self.cursor
