from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI

# Rozwiąż zadanie API o nazwie ‘gnome’. Backend będzie zwracał Ci linka do obrazków przedstawiających gnomy/skrzaty.
# Twoim zadaniem jest przygotowanie systemu, który będzie rozpoznawał, jakiego koloru czapkę ma wygenerowana postać.
# Uwaga! Adres URL zmienia się po każdym pobraniu zadania i nie wszystkie podawane obrazki zawierają zdjęcie postaci w czapce.
# Jeśli natkniesz się na coś, co nie jest skrzatem/gnomem, odpowiedz “error”. Do tego zadania musisz użyć GPT-4V (Vision).

# Get Task
task_helper = TaskHelper()
token = task_helper.auth('gnome')
task = task_helper.get_task(token, True)

client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
gnome = False
answer = ''

while not gnome:
    task = task_helper.get_task(token, True)
    response = client.chat.completions.create(
        model='gpt-4-turbo',
        messages=[
            {
                "role": "system",
                "content": "I'm capable to process images and find gnomes.\nProcess image provided by user. If it has gnome on it and this gnome has a hat, identify hat color and return its name in Polish language. Otherwise, return 'ERROR' word only."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": task['url']
                        }
                    }
                ]
            }
        ]
    )

    if response.choices[0].message.content != 'ERROR':
        gnome = True
        answer = response.choices[0].message.content

task_helper.send_task(token, answer)