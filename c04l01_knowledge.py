from task_helpers import TaskHelper
from openai import OpenAI
import requests

# Wykonaj zadanie API o nazwie ‘knowledge’. Automat zada Ci losowe pytanie na temat kursu walut, populacji wybranego kraju lub wiedzy ogólnej.
# Twoim zadaniem jest wybór odpowiedniego narzędzia do udzielenia odpowiedzi (API z wiedzą lub skorzystanie z wiedzy modelu).
# W treści zadania uzyskanego przez API, zawarte są dwa API, które mogą być dla Ciebie użyteczne.
# Jeśli zwracasz liczbę w odpowiedzi, to zadbaj, aby nie miała ona zbytecznego formatowania e.g.: 123456, not 123 456

class UnknownThemeTypeExpeption(Exception):
    pass

# CLASS START
class Knowledge:

    def __init__(self, question) -> None:
        self.currency_api_endpoint = 'http://api.nbp.pl/api/exchangerates/tables/A'
        self.country_info_endpoint = 'https://restcountries.com/v3.1/name'
        self.question = question
        self.openai_client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)

    # Wrap AI request to function.
    def aiRquest(self, systemPrompt, userPrompt):
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt
                },
                {
                    "role": "user",
                    "content": userPrompt
                }
            ]
        )

        return response.choices[0].message.content

    # Get theme of the question, so we can guide AI later.
    def getQuestionTheme(self) -> str:
        systemPrompt = 'Process user request and return the appropriate cathegory of the request. Available cathegories are: currency, population, general_knowledge. ###EXAMPLE\nuser: ile orientacyjnie ludzi mieszka w Polsce?\nAI: population"'
        theme = self.aiRquest(systemPrompt, self.question)

        return theme

    # This one returns required values from questions. E.g.: for currency question it returns international currency code like EUR or USD, etc.,
    # For country it returns country name in English as it is required in county_api to get it's data.
    # For general_question it just returns an answer.
    def processUserRequestData(self, theme) -> str:
        systemPrompt = ''
        if theme == 'currency':
            systemPrompt = 'You are aware of international currency codes in exchange services. Process user request end return currency code. ###EXAMPLE\nuser: jaki jest teraz kurs dolara?\nAI: USD'
        elif theme == 'population':
            systemPrompt = "You're capable to extract country name from user request in defferent languages. Extract country name in it's initial form and return result in English. ###EXAMPLE\nuser: ile orientacyjnie ludzi mieszka w Polsce?\nAI: poland"
        elif theme == 'general_knowledge':
            systemPrompt = "You're capable to answer on user request using your knowledge. Request might be in different language. Return answer in the same language as user request."
        else:
            raise UnknownThemeTypeExpeption('Unkonwn request theme.')

        response = self.aiRquest(systemPrompt, self.question)

        return response

    # Parse currency json and return exchange rate.
    def getCurrencyRate(self, currency) -> str | None:
        xml_data = requests.get(self.currency_api_endpoint)
        xml_data.raise_for_status()
        for item in xml_data.json():
            for currency_rate in item['rates']:
                if currency_rate['code'] == currency:
                    return currency_rate['mid']

        return None

    # Parse country data and return population.
    def getCountryPopulation(self, country) -> str:
        country_data = requests.get(self.country_info_endpoint + '/' + country)
        for item in country_data.json():
            return item['population']

    # Processes user question and answers it.
    def completeUserRequest(self):
        question_theme = self.getQuestionTheme()
        request_meta = self.processUserRequestData(question_theme)
        answer = ''

        if question_theme == 'currency':
            answer = self.getCurrencyRate(request_meta)
        elif question_theme == 'population':
            answer = self.getCountryPopulation(request_meta)
        elif question_theme == 'general_knowledge':
            answer = request_meta
        else:
            raise UnknownThemeTypeExpeption('Unkonwn request theme.')

        print('Question is:' + self.question)
        print('Answer is: ' + str(answer))

        return answer
# CLASS END

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("knowledge")
task = task_helper.get_task(token, True)

class_obj = Knowledge(task['question'])
task_helper.send_task(token, class_obj.completeUserRequest())





