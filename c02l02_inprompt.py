from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI

# Skorzystaj z API COURSE_API, aby pobrać dane zadania inprompt.
# Znajdziesz w niej dwie właściwości — input, czyli tablicę / listę zdań na temat różnych osób
# (każde z nich zawiera imię jakiejś osoby) oraz question będące pytaniem na temat jednej z tych osób.
# Lista jest zbyt duża, aby móc ją wykorzystać w jednym zapytaniu, więc dowolną techniką odfiltruj te zdania, które
# zawierają wzmiankę na temat osoby wspomnianej w pytaniu. Ostatnim krokiem jest wykorzystanie odfiltrowanych
# danych jako kontekst na podstawie którego model ma udzielić odpowiedzi na pytanie. Zatem: pobierz listę zdań oraz pytanie,
# skorzystaj z LLM, aby odnaleźć w pytaniu imię, programistycznie lub z pomocą no-code odfiltruj zdania zawierające to imię.
# Ostatecznie spraw by model odpowiedział na pytanie, a jego odpowiedź prześlij do naszego API w obiekcie JSON zawierającym jedną właściwość “answer”.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("inprompt")
task = task_helper.get_task(token, True)

client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Return only the name of the person mentioned in question"
        },
        {
            "role": "user",
            "content": "Question: " + task['question']
        }
    ]
)

# Get person info
person_info = ''
for info in task['input']:
   print(info + '\n')
   if response.choices[0].message.content in info:
      person_info = info

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Answer the question base on the provided context. \n###CONTEXT" + person_info + "###"
        },
        {
            "role": "user",
            "content": "Question: " + task['question']
        }
    ]
)

print(response.choices[0].message.content)
task_helper.send_task(token, response.choices[0].message.content)

