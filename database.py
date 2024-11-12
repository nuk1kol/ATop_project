import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='Database.db'):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """
        Создает таблицу для хранения истории запросов, если она не существует.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                query TEXT,
                                response TEXT,
                                timestamp TEXT
                              )''')
        self.connection.commit()

    def add_history(self, user_id, query, response):
        """
        Добавляет запись в историю запросов.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''INSERT INTO history (user_id, query, response, timestamp)
                               VALUES (?, ?, ?, ?)''', (user_id, query, response, timestamp))
        self.connection.commit()

    def get_last_history(self, user_id, limit=10):
        """
        Возвращает последние `limit` записей из истории запросов для конкретного пользователя.
        """
        self.cursor.execute('''SELECT query, response, timestamp FROM history
                               WHERE user_id = ? ORDER BY id DESC LIMIT ?''', (user_id, limit))
        return self.cursor.fetchall()
    
    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()

# Создаем экземпляр базы данных
db = Database()