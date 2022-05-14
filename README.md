# Blaze - A Production Deployment Framework

A production deployment framework using various DevOps tools. It uses **Jenkins jobs** for the different tasks execution. Each task could perform any specific job like execution of any script for initiating the deployment in any other DevOps tools like uDeploy or Ansible. It gives you flexibility to execute the different tasks using same configuration multiple times based on the requirement. It has a dashboard page to display all the tasks execution in the single page. It follows the Master-Worker architecture that allows you to handle the execution of all tasks with ease.


# Prerequisites

- **Python 3.10** must be installed in the system
- Installation of **required python modules** must be done using requirements.txt file present in the current repository.
- Latest version of **Jenkins** installed in the system for the creation of master and worker job configuration (we will discuss about this in detail later on)

