from task_helpers import TaskHelper

task_helper = TaskHelper()
token = task_helper.auth("helloapi")
task = task_helper.get_task(token, True)
task_helper.send_task(token, task["cookie"])