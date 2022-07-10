'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for about page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''
from . import Resource
from . import ResourceTemplatesName
from . import make_response, render_template
from flask import request,current_app as app


class About(Resource):
    
    
    def get(self):
        app.logger.critical("---------------------------- Starting Application ----------------------------",extra={"ip_addr":request.remote_addr})
        return make_response(render_template(ResourceTemplatesName.ABOUT_PAGE))
