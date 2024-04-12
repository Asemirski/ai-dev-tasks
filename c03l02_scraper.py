from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI
import urllib3
from time import sleep

# In this task I wanted to check urllib3 instead of requests lib.

# Rozwiąż zadanie z API o nazwie "scraper". Otrzymasz z API link do artykułu (format TXT), który zawiera pewną wiedzę,
# oraz pytanie dotyczące otrzymanego tekstu. Twoim zadaniem jest udzielenie odpowiedzi na podstawie artykułu.
# Trudność polega tutaj na tym, że serwer z artykułami działa naprawdę kiepsko — w losowych momentach
# zwraca błędy typu "error 500", czasami odpowiada bardzo wolno na Twoje zapytania, a do tego serwer
# odcina dostęp nieznanym przeglądarkom internetowym. Twoja aplikacja musi obsłużyć każdy z napotkanych błędów.
# Pamiętaj, że pytania, jak i teksty źródłowe, są losowe, więc nie zakładaj, że uruchamiając aplikację kilka razy,
# za każdym razem zapytamy Cię o to samo i będziemy pracować na tym samym artykule.

# Custom exceptions
class MaxRetriesReachedException(Exception):
    pass

class RequestFailedExeption(Exception):
    pass

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("scraper")
task = task_helper.get_task(token, True)

def get_text_data(url, max_retries=15, debug=False):
    # Initialize
    # Add header to avoid anti-bot protection
    retry_count = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Disable http/s warinigns of urllib3
    urllib3.disable_warnings()

    # Handle non 200 responses
    while retry_count < max_retries:
        try:
            # Disable certificate check and make request
            http = urllib3.PoolManager(cert_reqs='CERT_NONE', headers=headers)
            response = http.request('GET', url)
            if response.status == 200:
                if debug:
                    print(response.data.decode('utf-8'))
                return response.data.decode('utf-8')
            else:
                error_message = f'Request failed with the following error: {response.status} - {response.data.decode("utf-8")}'
                print(error_message)
                raise RequestFailedExeption(error_message)
        except:
            print(f'Retrying... Attempt {retry_count + 1}')
            retry_count += 1
            sleep(3)

            if max_retries == retry_count:
                raise MaxRetriesReachedException('Max retries reached')

text_data = get_text_data(task['input'], 15)

# AI Part
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": f"I'm capable to process huge text and answer to provided question regardign the text. I return answer in Polish language only. My answer is limited to 200 symbols. ###TEXT {text_data}###"
        },
        {
            "role": "user",
            "content": task['question']
        }
    ]
)

answer = response.choices[0].message.content
print('Question is: ' + task['question'] + '\nAnswer: ' + answer)
task_helper.send_task(token, answer)
