from modules.task_helper.task_helper import TaskHelper
from openai import OpenAI
from time import sleep

# Rozwiąż zadanie o nazwie “whoami”. Za każdym razem, gdy pobierzesz zadanie, system zwróci Ci jedną ciekawostkę na temat pewnej osoby.
# Twoim zadaniem jest zbudowanie mechanizmu, który odgadnie, co to za osoba.
# W zadaniu chodzi o utrzymanie wątku w konwersacji z backendem.
# Jest to dodatkowo utrudnione przez fakt, że token ważny jest tylko 2 sekundy (trzeba go cyklicznie odświeżać!).
# Celem zadania jest napisania mechanizmu, który odpowiada, czy na podstawie otrzymanych hintów jest w stanie powiedzieć,
# czy wie, kim jest tajemnicza postać. Jeśli odpowiedź brzmi NIE, to pobierasz kolejną wskazówkę i doklejasz ją do bieżącego wątku.
# Jeśli odpowiedź brzmi TAK, to zgłaszasz ją do /answer/. Wybraliśmy dość ‘ikoniczną’ postać, więc model powinien zgadnąć, o kogo
# chodzi, po maksymalnie 5-6 podpowiedziach. Zaprogramuj mechanizm tak, aby wysyłał dane do /answer/ tylko,
# gdy jest absolutnie pewny swojej odpowiedzi.

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("whoami")

# Initialize
client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)
i_am_certain = False
person_name = ''
data = ''

# Might be no very efficient (to make api call every time as it costs money :( ) and not correct form the perspective of prompt engineering techniques,
# but works well, as questions are not too complicated.
while not i_am_certain:
    person_raw_data = task_helper.get_task(token, True)
    data += person_raw_data['hint'] + '\n'

    raw_model_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You try to guess the person. User will give you facts about the person in Polish. If you 95% sure return person name. Otherwise return only NO word."
            },
            {
                "role": "user",
                "content": data
            }
        ]
    )
    model_response = raw_model_response.choices[0].message.content
    print("My reponse is: " + model_response)

    if model_response != 'NO':
        i_am_certain = True
        person_name = model_response
    else:
        sleep(2)

task_helper.send_task(token, person_name)