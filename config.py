
'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Handles the generic blaze configurations.

Created on 11-April-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''




'''
Database Details ( No need to modify )
'''

from os import getenv                       # Using getenv to retrieve the secrets securely from the environment variables


DB = {
    
    "DATABASE_NAME": "blaze"
    
}

'''
Jenkins Details ( Need to Modify )
''' 

JENKINS = {
    
    "SERVER_URL": "< Jenkins server base url >",			# example: http://localhost:8080
    "USERNAME": "< username >",				
    "TOKEN": getenv("JENKINS_TOKEN")					# Add jenkins token in the environment variable
        
}

'''
Blaze Details ( No need to modify )
'''

BLAZE = {
    "AUTH":{
        
            "SECRET_KEY" : getenv("BLAZE_SECRET"),			# Add blaze secret in the environment variable
            "ALGORITHM": "HS256"
                    
        }
    }

'''
Email Configuration Details ( Need to Modify )
'''

EMAIL = {
    
    "SENDER": "< sender email ID >",
    "SMTP": { "HOST": "< smtp host >", "PORT": < smtp port >},
    "PROTOCOL" : "< protocol >",				 # Either TLS or SSL
    "AUTH_REQUIRED": True,					 # Default True. If authentication is not required then update it to False
    "USERNAME": "< sender email ID >",
    "PASSWORD": getenv("EMAIL_SECRET")				 # Get the password or token from the environment variable
        
    }