from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI
import json

# Napisz wpis na bloga (w języku polskim) na temat przyrządzania pizzy Margherity. Zadanie w API nazywa się ”blogger”.
# Jako wejście otrzymasz spis 4 rozdziałów, które muszą pojawić się we wpisie (muszą zostać napisane przez LLM).
# Jako odpowiedź musisz zwrócić tablicę (w formacie JSON) złożoną z 4 pól reprezentujących te cztery napisane rozdziały, np.:
# {"answer":["tekst 1","tekst 2","tekst 3","tekst 4"]}

# Initialize
task_helper = TaskHelper()
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
token = task_helper.auth("blogger")
task = task_helper.get_task(token, True)

# AI part
article_list = []
content = f"Write a blog about pizza Margarita that consists of 4 sections: {task['blog']}. Resulting json should have section key filled with section name and article field filled with generated article"
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a food blogger. You return results on Polish language. You return json array only of the following format [{\"section\": \"sectionName\", \"article\": \"eneratedArticleText\"}]. Number of elements may vary depending on number of articles."
        },
        {
            "role": "user",
            "content": content
        }
    ]
)

# Split response by articles and send to answer endpoint
article_data = response.choices[0].message.content
for article in json.loads(article_data):
    article_list.append(article["article"])

task_helper.send_task(token, article_list)