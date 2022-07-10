'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for index page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''
from . import Resource
from . import ResourceTemplatesName
from . import ResponseStatus
from . import get_db_obj, close_db_connection
from . import make_response, render_template
from flask import current_app as app

class Index(Resource):
    """ Resource for handling the Index page
    """
    def get(self):
        """ Displays the index page to the users
        """
        return make_response(render_template(ResourceTemplatesName.INDEX_PAGE))
    
    def __validate_fields__(self, response):
        """ Verifies the required fields present in the index form.
        """
        required_fields = [ {"applicationName": "Value for the \"applicationName\" is missing."} ]
        for field in required_fields:
            for key, value in field.items():
                if key not in response:
                    return {"status": ResponseStatus.FAILURE, "message": value}, 400
    
    def post(self):
        """ Verifies the existence of the application in the database based on name and redirects the user to the dashboard page
        """
        try:
            from flask import request
            sql_db_utils = get_db_obj(app)
            response = request.get_json()
            if response == None: return {"status" : ResponseStatus.FAILURE, "message" : "Unable to read the details from payload. Please make sure it is in JSON format"}, 400
            validation_response = self.__validate_fields__(response)
            if validation_response: return validation_response
            if "applicationName" in response:
                if sql_db_utils.is_application_exist(response["applicationName"]) == 1:
                    return {"status": ResponseStatus.SUCCESS, "message": "Application exists!"}, 200
                else:
                    return {"status": ResponseStatus.FAILURE, "message": "Application does not exist!"}, 404
            else:
                return {"status": ResponseStatus.FAILURE, "message": "Value for applicationName is missing!"}, 400
        except Exception as err:
            app.logger.critical(err,exc_info=True)
            return {"status": ResponseStatus.ERROR, "message": "Unable to fetch application details. Please contact administrator."}, 500
        finally:
            close_db_connection(sql_db_utils)