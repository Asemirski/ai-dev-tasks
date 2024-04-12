from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI
import json
import requests
import os

# Rozwiąż zadanie o nazwie “people”. Pobierz, a następnie zoptymalizuj odpowiednio pod swoje potrzeby bazę danych XXXXX.json.
# Twoim zadaniem jest odpowiedź na pytanie zadane przez system. Uwaga! Pytanie losuje się za każdym razem na nowo, gdy odwołujesz się do /task.
# Spraw, aby Twoje rozwiązanie działało za każdym razem, a także, aby zużywało możliwie mało tokenów. Zastanów się, czy wszystkie operacje
# muszą być wykonywane przez LLM-a - może warto zachować jakiś balans między światem kodu i AI?

# TODO: move everything to class to simplify and to make it look better.

collection_name = 'people'
people_parsed_data = []
memory_file = 'people.json'
memory = []

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("people")
task = task_helper.get_task(token, True)

# Initialize
openai_client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)

# Download JSON lib file and create memory file with suitable structure,
# as initial JSON has a lot of noise.
if not os.path.exists(memory_file):
    json_data = requests.get(f'{TaskHelper.BASE_URL}/data/people.json').json()
    for person in json_data:
        people_parsed_data.append({"name": person['imie'],
            "surname": person['nazwisko'],
            "favourite_color": person['ulubiony_kolor'],
            "favourite_food": person['o_mnie'].split('.')[0],
            "place_of_residence": person['o_mnie'].split('.')[1]
        })

    json_people_parsed_data = json.dumps(people_parsed_data)
    with open(memory_file, 'w') as file:
        file.write(json_people_parsed_data)

with open(memory_file, 'r') as file:
    memory = json.load(file)

# Transform task question to json format.
# Also transforms short names to full names e.g. Krysia -> Krystyna.
response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "For provided user question return json only in the format given in example. There are three question cathegories: favourite_color, favourite_food, place_of_residence. Transform short names to full names. ###EXAMPLE user: jaki kolor się podoba Mariuszowi Kaczorowi?\nAI: {\"name\": \"Mariusz\", \"surname\": \"Kaczor\", \"question_type\": \"favourite_color\"}\nuser:Gdzie mieszka Krysia Ludek?\nAI: {\"name\": \"Krystyna\" \"surname\": \"Ludek\", \"question_type\": \"place_of_residence\"}"
        },
        {
            "role": "user",
            "content": task['question']
        }
    ]
)
json_question = json.loads(response.choices[0].message.content)

# Compare values to get required item from memory file.
# As question has name and surname in it, we can get required item as these fields are unique.
required_item = ''
for item in memory:
    if item['name'] == json_question['name'] and item['surname'] == json_question['surname']:
        required_item = item

# ????
# Process question cathegories and apply required appoach to get answer.
system_prompt = ''
user_prompt = ''
answer = ''

if json_question['question_type'] == 'favourite_color':
    answer = required_item['favourite_color']
elif json_question['question_type'] == 'favourite_food':
    format_prompt = "You're language expert and know Polish. Extract the food name from the user prompt and return only food name in the inital word form."
    user_prompt = required_item['favourite_food']
elif json_question['question_type'] == 'place_of_residence':
    format_prompt = "You're language expert and know Polish. Extract the city name from the user prompt and return it in the initial form."
    user_prompt = required_item['place_of_residence']

if json_question['question_type'] == 'favourite_food' or json_question['question_type'] == 'place_of_residence':
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": format_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    answer = response.choices[0].message.content

task_helper.send_task(token, answer)
