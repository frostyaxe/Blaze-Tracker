'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Resource class file for license page. 

Created on 09-Apr-2022

@author: Abhishek Prajapati

'''
from . import Resource
from . import make_response, render_template
from . import ResourceTemplatesName
from . import get_license

class License(Resource):
    """ Flask resource to handle license details page
    """
    def get(self):
        return make_response(render_template(ResourceTemplatesName.LICENSE_PAGE, license=get_license().replace("<", "&lt;").replace(">", "&gt;")))
