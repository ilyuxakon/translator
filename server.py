from flask import Flask, request
import logging
import json
import re
import translate


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

translator = translate.Translator('en', 'ru')
pattern = re.compile('^переведи слово .+$')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):
    message = req['request']['command']
    if pattern.match(message):
        message = message.split(' ', 2)[2]
        translation = translator.translate(message)
        res['response']['text'] = translation

    else:
        res['response']['text'] = 'Я могу перевести любой текст с английского на русский.\nДля этого введите запрос формата "Переведи слово ..."'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)