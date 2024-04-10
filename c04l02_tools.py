from task_helpers import TaskHelper
from openai import OpenAI
import json

# Rozwiąż zadanie API o nazwie ‘tools’. Celem zadania jest zdecydowanie, czy podane przez API zadanie powinno
# zostać dodane do listy zadań (ToDo), czy do kalendarza (jeśli ma ustaloną datę).
# Oba narzędzia mają lekko różniące się od siebie definicje struktury JSON-a (różnią się jednym polem).
# Spraw, aby Twoja aplikacja działała poprawnie na każdym zestawie danych testowych.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("tools")
task = task_helper.get_task(token, True)

# Everything is pretty self-explaining :)
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
systemPrompt = """
    You can differ to-do actions from calendar events. You need to process user prompt and decide which kind of action this is.
    Today's date is 09.04.2024
    Return JSON of the following structure for todo action {\"tool\": \"ToDo\", \"desc\": \"action\"} or the following structure for calendar event {\"tool\": \"Calendar\", \"desc\": \"event\", \"date\": \"date\"}
    ###EXAMPLE
    user: Przypomnij mi, że mam kupić mleko
    AI: {"tool": "ToDo" ,"desc": "Kup mleko"}
    user: Jutro mam spotkanie z Marianem
    AI: {"tool": "Calendar", "desc": "Spotkanie z Marianem", "date": "2024-04-10"}
"""

response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": task['question']
            }
        ]
    )

print(response.choices[0].message.content)
task_helper.send_task(token, json.loads(response.choices[0].message.content))