'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Handles the execution related to the Jenkins.

Created on 18-Apr-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''
from . import Jenkins
import requests

class JenkinsManager():
    
    def __init__(self, jenkins_server_url, username, token):
        
        self.__jenkins_server_url = jenkins_server_url
        self.__username = username
        self.__token = token
        self.__jenkins = Jenkins(jenkins_server_url, username=username, password=token)
        self.__build_progress_api = "api/json?tree=executor[progress]"
        
    
    def build_job(self, job_path):
        try:
            params = {"pipelineStatus":"resumed"}
            return self.__jenkins.build_job(job_path,params), None
        except Exception as e:
            return None, e
    
    
    def verify_build_in_queue(self, queue_number):
        queue_details = self.__jenkins.get_queue_item(queue_number)
        
        queue_classes = [ "hudson.model.Queue$WaitingItem", "hudson.model.Queue$BuildableItem", "hudson.model.Queue$LeftItem", "org.jenkinsci.plugins.workflow.job.WorkflowRun" ]
        
        while queue_details["_class"] in queue_classes:
            queue_details = self.__jenkins.get_queue_item(queue_number)
            if queue_details:
                return True
            return False
        
        
    def get_build_progress(self, build_url):
        
        request = requests.Request("GET", build_url + self.__build_progress_api)
        executor = self.__jenkins.jenkins_request(request).json()["executor"]
       
        if executor == None:
            return "100"
        return str(executor["progress"])
    
