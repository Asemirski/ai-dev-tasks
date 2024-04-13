from modules.task_helper.task_helper import TaskHelper

# Service is here - https://github.com/Asemirski/myapi/tree/apiv1

task_helper = TaskHelper()
token = task_helper.auth("ownapi")
task = task_helper.get_task(token, True)
task_helper.send_task(token, 'https://myapiwebapp.azurewebsites.net/api/question')