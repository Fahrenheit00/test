# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

requestStorage={
    "greetings":('привет','кто ты','здравствуй'),
    "about":('расскажи о вузе','расскажи о университете','расскажи о вас'),
    "location":('комиссия','где находится комиссия','отборочная комисиия'),
    "help":('Сколько направлений я могу выбрать','на какие направления я могу попасть','расскажи про поступление'),
    "score":('какой минимальный балл','какой у вас проходной балл','')

}


#Хранилище для ответов на приветсвтие
aboutRequest = ['расскажи о вузе','расскажи о университете','расскажи о вас']

#Хранилище для ответов на приветсвтие
locationRequest = ['комиссия','где находится комиссия','отборочная комисиия']

#Хранилище для ответов на приветсвтие
helpRequest = ['Сколько направлений я могу выбрать','на какие направления я могу попасть','расскажи про поступление']

#Хранилище для ответов на приветсвтие
scoreRequest = ['какой минимальный балл','какой у вас проходной балл','']


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

#функция для обработки ответа пользователя
#def handle_text():



# Функция для непосредственной обработки диалог
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Привет",
                "расскажи о вузе",
                "где находится комиссия",
            ]
        }

        res['response']['text'] = 'Говори, кожаный мешок'
        res['response']['buttons'] = get_suggests(user_id)
        return


    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in requestStorage["greetings"]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Привет я робот ТГУ. Моя задача помогать студентам ориентироваться в Томском государственном университете. Моя задача приветствие абитуриентов и помощь при первом посещении вуза. Я могу дать информацию о поступлении, помочь связаться с приемной комиссией.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in requestStorage["about"]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'В ТГУ 20 факультетов и учебных институтов, на которых  реализуется более 135 направлений подготовки и специальностей в различных областях знания: естественные, физико-математические, технические, компьютерные и информационные, гуманитарные и социальные.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in requestStorage["location"]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Все отборочные комиссии размещаются в холле Центра культуры ТГУ на 3-м этаже. Главный Штаб - Центральная приемная комиссия, -  находится в Главном корпусе ТГУ в 128 аудитории.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in requestStorage["help"]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Вы можете выбрать не более 3-х направлений/специальностей, на которые планируете участвовать в конкурсном отборе при поступлении.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in requestStorage["score"]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Вы сможете участвовать в конкурсе только в том случае, если по каждому вступительному испытанию (ЕГЭ) преодолен установленный  минимальный порог баллов, подтверждающий успешное прохождение вступительных испытаний.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Если нет, то убеждаем его купить слона!
    else:
        res['response']['text'] = 'не понимаю'
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 3:
        suggests.append({
            "title": "Перейти на сайт университета",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests