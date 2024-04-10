from task_helpers import TaskHelper
from openai import OpenAI

# Korzystając z modelu text-embedding-ada-002 wygeneruj embedding dla frazy Hawaiian pizza —upewnij się, że to dokładnie to zdanie.
# Następnie prześlij wygenerowany embedding na endpoint /answer.
# Konkretnie musi być to format {"answer": [0.003750941, 0.0038711438, 0.0082909055, -0.008753223, -0.02073651, -0.018862579, -0.010596331, -0.022425512, ..., -0.026950065]}. 
# Lista musi zawierać dokładnie 1536 elementów.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("embedding")
task = task_helper.get_task(token, True)

# Initialize openAI client and get embedding
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
response = client.embeddings.create(
    input='Hawaiian pizza',
    model='text-embedding-ada-002'
)

print(response.data[0].embedding)
task_helper.send_task(token, response.data[0].embedding)