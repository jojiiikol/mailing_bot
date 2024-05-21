import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host="127.0.0.1",
            port="5432",
            database="draw"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT version();")
        print(f"Connected to db: {self.cursor.fetchone()[0]}")

    async def get_id_from_tg_id(self, tg_id):
        try:
            query = f"SELECT id FROM draw_app_drawusers WHERE tg_id = {tg_id}"
            self.cursor.execute(query)
            user_id = self.cursor.fetchone()
            return user_id[0]
        except Exception as e:
            print(f"get_id_from_tg_id: При извлечении id произошла ошибка: {str(e)}")

    async def insert_user(self, tg_id, tg_name, joined_to_chanel=False, winner=False):
        try:
            user = await self.get_id_from_tg_id(tg_id)
            if user is None:
                query = f"INSERT INTO draw_app_drawusers (tg_id, tg_name, joined_to_chanel, winner) VALUES ('{tg_id}', '{tg_name}', '{joined_to_chanel}', '{winner}')"
                self.cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(f"insert_user: При добавлении пользователя произошла ошибка: {str(e)}")

    async def update_subscription_status_user(self, tg_id):
        try:
            query = f"UPDATE draw_app_drawusers SET joined_to_chanel = true WHERE tg_id ={tg_id}"
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(
                f"update_subscription_status_user: Произошла ошибка в изменении статуса подписанного на канал пользователя: {str(e)}")
