'''
Created on 21-Jun-2022

@author: Abhishek Prajapati
'''
from . import Resource, auth_required, ResponseStatus, get_db_obj, TableName, close_db_connection, Error, make_response, render_template,ResourceTemplatesName

class ManageBuildQueue(Resource):
    
    def __init__(self,app):
        self.app = app
    
    @auth_required    
    def put(self,code=1):
        try:
            sql_db_utils = get_db_obj(self.app)
            sql = '''UPDATE {table}
                     SET IS_QUEUE_PAUSED = {0}
                     WHERE ID = 0
            '''.format(code,table=TableName.BUILD_QUEUE)
            sql_db_utils.execute_script(sql)
            if code == 0:
                return {"status": ResponseStatus.SUCCESS, "message": "Build queue has been resumed successfully"}, 200
            elif code >0:
                return {"status": ResponseStatus.SUCCESS, "message": "Build queue has been paused successfully"}, 200
            else:
                return {"status":ResponseStatus.FAILURE,"message": "Invalid value provided by the user. code value must be either 0 or it must be greater than 0."}, 400
        except Error as e:
            print(e) #replace with the logger
            return {"status":ResponseStatus.FAILURE,"message": str(e)}, 500
        finally:
            close_db_connection(sql_db_utils) 
            
class DisplayBuildQueue(Resource):
    
    def __init__(self,app):
        self.app = app
    
    
    @auth_required    
    def get(self):
        return make_response(render_template(ResourceTemplatesName.BUILD_QUEUE))