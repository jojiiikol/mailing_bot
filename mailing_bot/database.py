from datetime import date
from psycopg2 import connect
import os
from dotenv import load_dotenv

load_dotenv()


class Database():
    def __init__(self):
        self.connection = connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host='127.0.0.1',
            port='5432',
            database='mailing_bot_db'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT version();")
        print(f"Succefully connected to database: {self.cursor.fetchone()[0]}")

    async def get_id_from_tg_id(self, tg_id):
        try:
            query = f"SELECT id FROM users WHERE tg_id ={tg_id}"
            self.cursor.execute(query)
            user_id = self.cursor.fetchone()
            return user_id
        except Exception as e:
            print(f"get_id_from_tg_id: При возращении пользователя произошла ошибка: {str(e)}")

    async def insert_user(self, tg_id, nickname):
        try:
            user = await self.get_id_from_tg_id(tg_id)
            if user is None:
                date_now = date.today()
                query = f"INSERT INTO users (tg_id, nickname, date_joined) VALUES ('{tg_id}', '{nickname}', '{date_now}')"
                self.cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(f"insert_user: При добавлении пользователя произошла ошибка: {str(e)}")

    async def insert_admin(self, tg_id):
        try:
            user = await self.get_admin_id_from_tg_id(tg_id)
            if user is None:
                query = f"INSERT INTO admins (tg_id) VALUES ('{tg_id}')"
                self.cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(f"insert_admin: При добавлении админа произошла ошибка: {str(e)}")

    async def get_admin_id_from_tg_id(self, tg_id):
        try:
            query = f"SELECT id FROM admins WHERE tg_id ={tg_id}"
            self.cursor.execute(query)
            user_id = self.cursor.fetchone()
            return user_id
        except Exception as e:
            print(f"get_id_from_tg_id: При возращении админа произошла ошибка: {str(e)}")


    async def update_subscription_status_user(self, tg_id):
        try:
            date_now = date.today()
            query = f"UPDATE users SET confirmed = true, channel_date_joined = '{date_now}' WHERE tg_id ={tg_id}"
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(
                f"update_subscription_status_user: Произошла ошибка в изменении статуса подписанного на канал пользователя: {str(e)}")

    async def update_blocked__status_user(self, tg_id):
        try:
            query = f"UPDATE users SET is_block = true where tg_id = {tg_id}"
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(
                f"update_blocked__status_user: Произошла ошибка при изменении статуса блокировки пользователем бота: {str(e)}")

    async def update_unblocked__status_user(self, tg_id):
        try:
            query = f"UPDATE users SET is_block = false where tg_id = {tg_id}"
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(
                f"update_blocked__status_user: Произошла ошибка при изменении статуса блокировки пользователем бота: {str(e)}")

    async def get_all_user_for_mailing(self):
        try:
            query = "SELECT tg_id FROM users WHERE confirmed = true AND is_block = false"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"get_all_user_for_mailing: Ошибка в выборке всех пользователей для рассылки: {str(e)}")
