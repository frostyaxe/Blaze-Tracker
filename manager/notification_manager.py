'''

Copyright (C) 2022 Abhishek Prajapati, Frostyaxe. All rights reserved.

 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 

@summary: Handles the email notifications based on the details provided by the user.

Created on 18-Apr-2022

@author: Abhishek Prajapati

***** You don't have any permission to modify any code in this framework without having prior approval from the author. *****

'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import ssl
from config import EMAIL

class SendEmailNotification(object):
    
    def __init__(self):
        self.context = ssl.create_default_context()
        self.subject = "Pipeline execution has been paused!"
        self.receiver = [ EMAIL["SENDER"] ]
        self.template_name = None
        self.vars = {}
    
    
    def __login_and_send_notification__(self, server):
        if EMAIL["AUTH_REQUIRED"]:
            server.login(EMAIL["USERNAME"],EMAIL["PASSWORD"])
            
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = EMAIL["SENDER"]
        message["To"] = ','.join(self.receiver)
        from jinja2 import Environment, FileSystemLoader
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        from manager.vars_manager import PROJECT_ROOT_DIR
        from os import path
        static_folder = path.join(PROJECT_ROOT_DIR,"static")
        img_folder = path.join(static_folder,"img")
        header_logo = path.join(img_folder, "email_logo.PNG")
        with open(header_logo, 'rb') as fp:
            msgImage = MIMEImage(fp.read())
        
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)
        template = env.get_template( self.template_name )
        rendered_template = MIMEText(template.render(self.vars), "html")

        message.attach(rendered_template)
        server.sendmail(
        
        EMAIL["SENDER"], self.receiver, message.as_string()
    )
            
    def send_email(self):
        if EMAIL["PROTOCOL"] == "SSL":
            with smtplib.SMTP_SSL(EMAIL["SMTP"]["HOST"], EMAIL["SMTP"]["PORT"], context=self.context) as server:
                self.__login_and_send_notification__(server)
        else:
            with smtplib.SMTP(EMAIL["SMTP"]["HOST"], EMAIL["SMTP"]["PORT"], context=self.context) as server:
                server.starttls(context=self.context)
                self.__login_and_send_notification__(server)