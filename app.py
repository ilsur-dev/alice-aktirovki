from flask import Flask, request
import logging
from database import Database
from handler import AliceHandler

IP = '127.0.0.1'
PORT = 19823

FORMAT = '[%(asctime)-15s] [%(levelname)s] - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.info('Запуск сервера...')

db = Database('database.sqlite')
db.setup()

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.json
    return str(AliceHandler(db, data))


if __name__ == '__main__':
    app.run(host=IP, port=PORT)