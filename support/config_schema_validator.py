'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Schema validation of the blaze configuration.

Created on 13-May-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

from schemadict import schemadict
from config import BLAZE, DB, EMAIL, JENKINS

DB_SCHEMA = schemadict({ 
    
    "DATABASE_NAME": {
            'type': str,
            'regex': r'[a-z]+',
    },
    
    "$required_keys": [ "DATABASE_NAME" ]
             
})   

JENKINS_SCHEMA = schemadict({
    
    "SERVER_URL": {
        'type': str,
        'regex': r"^(http(s)?:\/\/)[\w.-]+[\w\-\._~:?[\]@!\$&'\(\)\*\+,;=.]+$"
    },
    "USERNAME": {
        'type': str,
    },
    "TOKEN": {
        'type': str
    },
    
    "$required_keys": [ "SERVER_URL", "USERNAME", "TOKEN" ]
    
})

BLAZE_AUTH_DICT_SCHEMA = {
    
     "SECRET_KEY" : {
        'type': str
    },
    "ALGORITHM": {
        'type': str,
        'regex': r"^HS256$"
    },
    
    "$required_keys": [ "SECRET_KEY", "ALGORITHM" ]
}


BLAZE_AUTH_SCHEMA = schemadict({
    "AUTH": {
        'type': dict,
        'schema': BLAZE_AUTH_DICT_SCHEMA
    },
    
    "$required_keys": [ "AUTH" ]
    
})

EMAIL_SMTP_SCHEMA = {
    "HOST": {
        'type': str
    }, 
    "PORT": {
        'type': int
    },
    
    "$required_keys": [ "HOST", "PORT" ]
}


EMAIL_SCHEMA = schemadict({
    
    "SENDER": {
        'type': str,
        'regex': r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    },
    "SMTP": { 
        'type': dict,
        'schema': EMAIL_SMTP_SCHEMA
    },
    "PROTOCOL" : {
        'type': str,
        'regex': "(SSL|TLS)"
    },
    "AUTH_REQUIRED": {
        'type': bool
    },
    "USERNAME": {
        'type': str,
        'regex': r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    },
    "PASSWORD": {
        'type': str,
    },
    
    "$required_keys": [ "SENDER", "SMTP", "PROTOCOL", "AUTH_REQUIRED" ]
        
})



def validate_config():
    schemas = [ {"schema":DB_SCHEMA,"dictionary":DB}, {"schema":JENKINS_SCHEMA,"dictionary":JENKINS}, {"schema":BLAZE_AUTH_SCHEMA,"dictionary":BLAZE},{"schema":EMAIL_SCHEMA,"dictionary":EMAIL} ]
    
    for schema_validation in schemas:
        schema_validation["schema"].validate(schema_validation["dictionary"])




