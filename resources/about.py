'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for about page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''
from . import Resource
from . import make_response, render_template
from . import ResourceTemplatesName

class About(Resource):
    
    def __init__(self,app):
        self.app = app
    
    def get(self):
        return make_response(render_template(ResourceTemplatesName.ABOUT_PAGE))
