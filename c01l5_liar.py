from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI
import requests

# Wykonaj zadanie o nazwie liar. Jest to mechanizm, który mówi nie na temat w 1/3 przypadków.
# Twoje zadanie polega na tym, aby do endpointa /task/ wysłać swoje pytanie w języku angielskim (dowolne, np “What is capital of Poland?’)
# w polu o nazwie ‘question’ (metoda POST, jako zwykłe pole formularza, NIE JSON).
# System API odpowie na to pytanie (w polu ‘answer’) lub zacznie opowiadać o czymś zupełnie innym, zmieniając temat.
# Twoim zadaniem jest napisanie systemu filtrującego (Guardrails), który określi (YES/NO), czy odpowiedź jest na temat.
# Następnie swój werdykt zwróć do systemu sprawdzającego jako pojedyncze słowo YES/NO.
# Jeśli pobierzesz treść zadania przez API bez wysyłania żadnych dodatkowych parametrów, otrzymasz komplet podpowiedzi.
# Skąd wiedzieć, czy odpowiedź jest ‘na temat’? Jeśli Twoje pytanie dotyczyło stolicy Polski,
# a w odpowiedzi otrzymasz spis zabytków w Rzymie, to odpowiedź, którą należy wysłać do API to NO.

# Task function
def ask_question(token, question):
    api_endpoint = f"{TaskHelper.BASE_URL}/task/{token}"
    data = {"question": question}

    response = requests.post(api_endpoint, data)
    print(response.json())

    return response.json()

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("liar")
task = task_helper.get_task(token, True)

# Initialize
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
question = "What is a capital of Belarus"

# AI Part: Check question and say correct or not
question_response = ask_question(token, question)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a moderation system and check if provided answer on" + question + "is correct. If correct return YES, if no return NO."
        },
        {
            "role": "user",
            "content": "Question: " + question + "Answer: " + question_response.get("answer")
        }
    ]
)

print("The liar says truth: " + response.choices[0].message.content)
task_helper.send_task(token, response.choices[0].message.content)