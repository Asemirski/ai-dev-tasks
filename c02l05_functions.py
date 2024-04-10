from task_helpers import TaskHelper

#  Zadanie polega na zdefiniowaniu funkcji o nazwie addUser, która przyjmuje jako parametr obiekt z
# właściwościami: imię (name, string), nazwisko (surname, string) oraz rok urodzenia osoby (year, integer).
# Jako odpowiedź musisz wysłać jedynie ciało funkcji w postaci JSON-a.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("functions")
task = task_helper.get_task(token, True)

# Define function structure
tools = [
    {
        "type": "function",
        "name": "addUser",
        "description": "Add User",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the user"
                },
                "surname": {
                    "type": "string",
                    "description": "The surname of the user"
                },
                "year": {
                    "type": "integer",
                    "description": "user's year of born"
                }
            }
        },
        "required": ["name", "surname", "year"]
    }
]

task_helper.send_task(token, tools[0])