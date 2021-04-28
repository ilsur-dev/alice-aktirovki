from database import Database
from objects.user import User
import json
from aktirovkiAPI import get_prognoz_now, get_nearest

CITIES = {1: 'сургут', 2: 'ханты-мансийск', 3: 'нижневартовск',
          4: 'норильск', 6: 'ноябрьск', 7: 'муравленко', 8: 'салехард'}

CITIES_BUTTONS = [
    {'title': city[1].capitalize(), 'payload': {'type': 'setCity', 'id': city[0]}, 'hide': True}
    for city in CITIES.items()
]

HELP_BUTTONS = [
    {'title': 'Актировка сегодня', 'payload': {'type': 'aktirovka', 'when': 'today'}, 'hide': True},
    {'title': 'Актировка завтра', 'payload': {'type': 'aktirovka', 'when': 'tomorrow'}, 'hide': True},
    {'title': 'Прогноз', 'payload': {'type': 'predict'}, 'hide': True},
    {'title': 'Сменить город', 'payload': {'type': 'changeCity'}, 'hide': True}
]


class AliceHandler():
    def __init__(self, db, request):
        self.db = db
        self.request = request

        self.response = {
            "version": request['version'],
            "session": request['session'],
            "response": {
                "end_session": False
            }
        }

        self.user = User(db, request)
        self.user.log_query(' '.join(request['request']['nlu']['tokens']))
        if self.user.stage == 'init':
            self.initMessage()
        elif self.user.stage == 'selectCity':
            self.cityHandler()
        elif self.user.stage == 'main':
            intents = request['request']['nlu']['intents']
            if 'aktirovkiTomorrow' in intents or 'nearest' in intents \
                    or 'targetDay' in intents or 'prognoz' in intents:
                self.nearestAktirovki()
            elif 'aktirovkiToday' in intents:
                self.aktirovkiToday()
            elif 'changeCity' in intents:
                self.cityHandler()
                self.user.set_stage('selectCity')
            else:
                self.response['response'] = {
                    'text': f"Выбран город {CITIES[self.user.city].capitalize()}. Я могу подсказать \
                            актировку на сегодня, либо ближайшую актировку. Также ты можешь сменить город",
                    "buttons": HELP_BUTTONS,
                    "end_session": False
                }

    def initMessage(self):
        self.response['response'] = {
            'text': "Привет! Я могу подсказать актированные дни для школьников, \
                когда занятия отменяются из-за низкой температуры. В каком городе ты живёшь?",
            "buttons": CITIES_BUTTONS,
            "end_session": False
        }

        self.user.set_stage('selectCity')

    def cityHandler(self):
        geo_entities = list(filter(lambda x: x['type'] == 'YANDEX.GEO', self.request['request']['nlu']['entities']))
        city_id = None
        for entity in geo_entities:
            if 'city' in entity['value']:
                city = entity['value']['city']
                if city.lower() in CITIES.values():
                    city_id = list(filter(lambda x: x[1] == city.lower(), CITIES.items()))[0][0]

        if city_id:
            self.response['response'] = {
                'text': f"Выбран город {CITIES[city_id].capitalize()}. \
                        Теперь ты можешь узнать о наличии актировки сегодня или прогноз на завтра или на неделю",
                "buttons": HELP_BUTTONS,
                "end_session": False
            }

            self.user.set_stage('main')
            self.user.set_city(city_id)
        else:
            self.response['response'] = {
                'text': "Доступные города: Сургут, Ханты-Мансийск, Нижневартовск, \
                        Норильск, Ноябрьск, Муравленко, Салехард. Выбери один из них.",
                "buttons": CITIES_BUTTONS,
                "end_session": False
            }

    def aktirovkiToday(self):
        response = get_prognoz_now(self.user.city)
        self.response['response'] = {
            'text': response,
            "buttons": HELP_BUTTONS,
            "end_session": False
        }

    def nearestAktirovki(self):
        response = get_nearest(self.user.city)
        self.response['response'] = {
            'text': response,
            "buttons": HELP_BUTTONS,
            "end_session": False
        }

    def __str__(self):
        return json.dumps(self.response)