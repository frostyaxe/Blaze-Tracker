'''
Created on 08-Jun-2022

@author: Abhishek Prajapati
'''

taskbook_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Blaze Taskbook Schema",
    "description": "Blaze Taskbook YAML schema validation",
    "type": "object",
    "properties": {
            "params": {
                "description": "Parameters section to provide details in the key value pair",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": { "type": "string" },
                        "value": {}
                    },
                    "required": [ "name", "value" ],
                    "additionalProperties": False

                }
            },
            "tasks": {
                "description": "Tasks to be executed",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties":{
                        "name": {
                            "description": "Name of the task",
                            "type": "string",
                            "pattern": "^[A-Za-z\\d\\-_\\s]+$",
                            "message": "Only alphanumeric, space, underscore and hypen allowed in the name."
                            

                        },
                        "category": {
                            "description": "Category Value. Usually depicts the phase of deployment",
                            "type": "string",
                            "pattern": "^[A-Za-z\\d\\-_\\s]+$"
                        },
                        "config":{
                            "description": "Name of the either pre-defined or user-defined configuration",
                            "type": "string",
                            "pattern": "^[A-Za-z\\d\\-_\\s]+$"
                        },
                        "parameters":{
                            "description": "User defined parameters required for the task execution",
                            "type": "object"
                        },
                        "monitor":{
                            "description": "Runs the tasks either in background if the provided value is false",
                            "type": "boolean"
                        },
                        "skip":{
                            "description": "Skips the task execution if the provided value is true",
                            "type": "boolean"
                        },
                        "replay":{
                            "description": "Re-run the task regardless of any status. Use skip flag as True else remove replay flag before resuming the pipeline or re-triggering the master job",
                            "type": "boolean"
                        },
                        "allowFailure":{
                            "description": "Ignores the current failed task execution and proceeding with the next task execution if the provided value is true",
                            "type": "boolean"
                        },
                        "dependsOn":{
                            "description": "Task dependencies",
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [ "name", "category", "config" ],
                    "additionalProperties": True,
                    "if": 
                    {
                        "properties": {
                          "config": { "const": "pause" }
                        },
                        "required": [ "config" ]
                    },
                    "then": { 
                        
                        "properties": {
                            "name": {
                                "description": "Name of the task",
                                "type": "string"
                            },
                            "category": {
                                "description": "Category Value. Usually depicts the phase of deployment",
                                "type": "string"
                            },
                            "config":{
                                "description": "Name of the either pre-defined or user-defined configuration",
                                "type": "string"
                            }
                        },
                        "required": [ "name","category","config" ],
                        "additionalProperties": False

                    }            
                },
                "uniqueItems": True
            }
        },
    "required": ["params","tasks"],
    "additionalProperties": False
    }

from jsonschema import Draft7Validator

def validate_json(json_data):

    validator = Draft7Validator(taskbook_schema)
    errors = sorted(validator.iter_errors(json_data), key=lambda e: e.path)
    
    if errors:
        return False, [ str(error) for error in errors ]
        

    message = "Given JSON data is Valid"
    return True, message
