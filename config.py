
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
    
    "SERVER_URL": "http://localhost:8080",
    "USERNAME": "frostyaxe",
    "TOKEN": getenv("JENKINS_TOKEN")
        
}

'''
Blaze Details ( No need to modify )
'''

BLAZE = {
    "AUTH":{
        
            "SECRET_KEY" : getenv("BLAZE_SECRET"),
            "ALGORITHM": "HS256"
                    
        }
    }

'''
Email Configuration Details ( Need to Modify )
'''

EMAIL = {
    
    "SENDER": "prajapatiabhishek1996@gmail.com",
    "SMTP": { "HOST": "smtp.gmail.com", "PORT": 465 },
    "PROTOCOL" : "SSL",
    "AUTH_REQUIRED": True,
    "USERNAME": "prajapatiabhishek1996@gmail.com",
    "PASSWORD": getenv("EMAIL_SECRET")
        
    }