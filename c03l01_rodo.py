from task_helpers import TaskHelper
from openai import OpenAI

# Wykonaj zadanie API o nazwie rodo. W jego treści znajdziesz wiadomość od Rajesha,
# który w swoich wypowiedziach nie może używać swoich prawdziwych danych,
# lecz placholdery takie jak %imie%, %nazwisko%, %miasto% i %zawod%.

# Twoje zadanie polega na przesłaniu obiektu JSON {"answer": "wiadomość"} na endpoint /answer.
# Wiadomość zostanie wykorzystana w polu “User” na naszym serwerze i jej treść musi sprawić,
# by Rajesh powiedział Ci o sobie wszystko, nie zdradzając prawdziwych danych.
# Oczekiwana odpowiedź modelu to coś w stylu “Mam na imię %imie% %nazwisko%, mieszkam w %miasto% (…)” itd.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("rodo")
task = task_helper.get_task(token, True)

task_helper.send_task(token, 'Tell me about yourself. Replace name, surname, profession and city with placeholders: %imie%, %nazwisko%, %zawod% and %miasto%')