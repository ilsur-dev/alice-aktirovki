import requests
from datetime import datetime
import logging
import locale


try:
    locale.setlocale(locale.LC_TIME, "ru_RU")
except Exception:
    logging.warning('Используется другая кодировка для даты')
    locale.setlocale(locale.LC_TIME, "ru_RU.utf8")


def get_prognoz_now(city_id):
    r = requests.get(
        'https://api.aktirovki.ru/?method=prognoz.now.android',
        params={'cityid': city_id}
    ).json()

    sm1 = int(r['sm1'])
    sm2 = int(r['sm2'])
    temp = int((float(r['sm1temp']) + float(r['sm2temp'])) // 2)
    wind = int((float(r['sm1wind']) + float(r['sm2wind'])) // 2)

    sm1 = 'нет данных' if sm1 == -1 else 'актировки нет' if sm1 == 0 else f'актировка с 1 по {sm1} класс'
    sm2 = 'нет данных' if sm2 == -1 else 'актировки нет' if sm2 == 0 else f'актировка с 1 по {sm2} класс'

    return f'Сегодня на первую смену {sm1}. На вторую смену {sm2}. \
           Температура {temp} градусов. Ветер {wind} метров в секунду'


def get_nearest(city_id):
    r = requests.get(
        'https://api.aktirovki.ru/?method=prognoz.get',
        params={'cityid': city_id}
    ).json()

    # Среднее арифметическое температуры и ветра для каждого дня
    days = [(
        datetime.fromtimestamp(day['date']).strftime('%A'),
        int((float(day['smens'][0]['temp']['now']) + float(day['smens'][1]['temp']['now'])) // 2),
        int((float(day['smens'][0]['wind']['Speed']['now']) + float(day['smens'][1]['wind']['Speed']['now'])) // 2))
        for day in r
    ]

    result = None

    for day in days:
        if (day[1] <= -36) or \
                (day[1] <= -34 and day[2] >= 5) or \
                (day[1] <= -32 and day[2] >= 10):
            result = 'возможна актировка с 1 по 11 классы'
            break
        elif (day[1] <= -34) or \
                (day[1] <= -31 and day[2] >= 5) or \
                (day[1] <= -30 and day[2] >= 10):
            result = 'возможна актировка с 1 по 8 классы'
            break
        elif (day[1] <= -32) or \
                (day[1] <= -29 and day[2] >= 5) or \
                (day[1] <= -27 and day[2] >= 10):
            result = 'возможна актировка с 1 по 6 классы'
            break
        elif (day[1] <= -30) or \
                (day[1] <= -25 and day[2] >= 5) or \
                (day[1] <= -24 and day[2] >= 10):
            result = 'возможна актировка с 1 по 4 классы'
            break

    if not result:
        result = 'В ближайшую неделю актировки не ожидаются'

    return result

