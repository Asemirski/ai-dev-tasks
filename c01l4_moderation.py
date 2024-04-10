from task_helpers import TaskHelper
from openai import OpenAI
import json

# Zastosuj wiedzę na temat działania modułu do moderacji treści i rozwiąż zadanie o nazwie “moderation” z użyciem naszego API do sprawdzania rozwiązań.
# Zadanie polega na odebraniu tablicy zdań (4 sztuki), a następnie zwróceniu tablicy z informacją, które zdania nie przeszły moderacji.
# Jeśli moderacji nie przeszło pierwsze i ostatnie zdanie, to odpowiedź powinna brzmieć [1,0,0,1].
# Pamiętaj, aby w polu ‘answer’ zwrócić tablicę w JSON, a nie czystego stringa.
# P.S. wykorzystaj najnowszą wersję modelu do moderacji (text-moderation-latest)

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("moderation")
task = task_helper.get_task(token, True)

# Initialize
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
flagged_results = []

# Send input to moderation model
response = client.moderations.create(input=task["input"], model="text-moderation-latest").model_dump_json()
raw_data = json.loads(response)
# Parse response data
for result in raw_data["results"]:
    if result["flagged"]:
        flagged_results.append(1)
    elif not result["flagged"]:
        flagged_results.append(0)
    else:
        print("Error. Unknown result.")

# one more way to do this. But this one is not mine :)
# [int(result.flagged) for result in raw_data.results]

task_helper.send_task(token, flagged_results)
