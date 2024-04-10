from task_helpers import TaskHelper
from openai import OpenAI
import requests

# W ramach zadania otrzymasz plik MP3 (15 sekund), który musisz wysłać do transkrypcji, a otrzymany z niej tekst odeślij jako rozwiązanie zadania.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("whisper")
task = task_helper.get_task(token, True)

#Get file
url = f'{TaskHelper.BASE_URL}/data/mateusz.mp3'
local_file_name = 'task_sound.mp3'
download = requests.get(url)
with open(local_file_name, 'wb') as file:
    file.write(download.content)

# Open file
file_data = open(local_file_name, 'rb')

# Transcritp voice to text
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
response = client.audio.transcriptions.create(
    model='whisper-1',
    file=file_data
)

print(response.text)
task_helper.send_task(token, response.text)
