import logging


class User:
    def __init__(self, db, request):
        self.db = db
        self.request = request

        self.session = request['session']
        self.id = self.session['user']['user_id']
        self.city = None
        self.stage = None

        self.get_data()

    def get_data(self):
        data = self.db.cur.execute('SELECT * FROM users WHERE id = ?', (self.id, )).fetchall()
        if data:
            self.city = data[0][1]
            self.stage = data[0][2]
        else:
            # Если пользователь не найден, то регистрируем в БД
            self.register()
            logging.info(f'Пользователь {self.id[:12]}... зарегистрирован в БД')

    def set_stage(self, stage):
        self.db.cur.execute('UPDATE users SET stage = ? WHERE id = ?', (stage, self.id, )).fetchall()
        self.db.con.commit()
        self.get_data()

    def set_city(self, city):
        self.db.cur.execute('UPDATE users SET city = ? WHERE id = ?', (city, self.id, )).fetchall()
        self.db.con.commit()
        self.get_data()

    def register(self):
        self.db.cur.execute('INSERT INTO users (id) VALUES (?)', (self.id, )).fetchall()
        self.db.con.commit()
        data = self.db.cur.execute('SELECT * FROM users WHERE id = ?', (self.id, )).fetchall()
        self.city = data[0][1]
        self.stage = data[0][2]