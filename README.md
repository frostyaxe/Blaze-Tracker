# Blaze - A Production Deployment Framework

A production deployment framework using various DevOps tools. It uses **Jenkins jobs** for the different tasks execution. Each task could perform any specific job like execution of any script for initiating the deployment in any other DevOps tools like uDeploy or Ansible. It gives you flexibility to execute the different tasks using same configuration multiple times based on the requirement. It has a dashboard page to display all the tasks execution in the single page. It follows the Master-Worker architecture that allows you to handle the execution of all tasks with ease.


# Prerequisites

- **Python 3.10** must be installed in the system
- Installation of **required python modules** must be done using requirements.txt file present in the current repository.
- Latest version of **Jenkins** installed in the system for the creation of master and worker job configuration (we will discuss about this in detail later on)
- Download blaze client: https://github.com/frostyaxe/Blaze-Client/releases/tag/v1.0-beta.1</br>
  (Use blaze-client for linux platform and blaze-client.exe for windows platform)

# Preview (Dashboard Page - Execution progress & Paused Pipeline)

![Alt Text](https://github.com/frostyaxe/Blaze-Tracker/blob/master/static/img/blaze-preview.gif)

# Setup Instructions

### Step 1: Blaze Configuration Update
- Open the config.py file present in this repository
- Update the Jenkins configuration
  <table>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>SERVER_URL</td>
      <td>Jenkins server base url. For example: http://localhost:8000</td>
    </tr>
    <tr>
      <td>USERNAME</td>
      <td>Jenkins User ID. <strong>Note: Framework does not support anonymous access.</strong></td>
    </tr>
    <tr>
      <td>TOKEN</td>
      <td>Jenkins Authentication Token. Set the environment variable in the system named as "JENKINS_TOKEN" and keep the authentication there. <b>Do not hardcode authentication token in the file</b></td>
    </tr>
  <table>
- Update the blaze authentication details
  <table>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>SECRET_KEY</td>
      <td>Random Secret Key String. <strong>Tip: Use MD5 string of any text that will be easy to remember. Please check the following link: <a href="https://www.md5hashgenerator.com"> Text to MD5 string</a></strong>. Store it in the environment variable named as "BLAZE_SECRET".</td>    
    </tr>
  </table>
    
- Update Email Configuration Details
  <table>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>SENDER</td>
      <td>EMAIL ID of the sender.</td>
    </tr>
    <tr>
      <td>PROTOCOL</td>
      <td>Supports TLS & SSL</td>
    </tr>
    <tr>
      <td>SMTP</td>
      <td>Host & Port details. </br><strong>For Example ( GMAIL Details ):</strong></br>
      Gmail SMTP server address: <i><u>smtp.gmail.com</u></i>                    </br>
      Gmail SMTP port (TLS): <i><u>587</u></i>                                     </br>
      Gmail SMTP port (SSL): <i><u>465</u></i>                     
      </td> 
    </tr>
    <tr>
      <td>USERNAME</td>
      <td>Email ID of the User</td>
    </tr>
    <tr>
      <td>PASSWORD</td>
      <td>Password/Authentication token of the user. For gmail, Please generate the app password and use it instead of actual login password: https://myaccount.google.com/apppasswords.  Store it in the environment variable named as "EMAIL_SECRET".</td>
    </tr>
  </table>
