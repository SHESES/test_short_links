import psycopg2
from typing import Union
import os

pg_host = 'localhost'
pg_user = 'postgres'
pg_pwd = 'admin'
pg_db = 'postgres'
pg_port = 5432


class DBLinks:
    def __init__(self):
        """
        Создание подключения к базе данных PostgreSQL.
        Принимает экземпляр класса
        """
        self.conn = psycopg2.connect(dbname=pg_db, user=pg_user,
                                     password=pg_pwd, host=pg_host, port=pg_port)

    def _con_cursor(self):
        """
        Производит подключение
        """
        self.cursor = self.conn.cursor()

    def ping_version(self) -> Union[None, int]:
        """
        Проверка подключения к базе данных. Выводит платформу
        :return: 505 - ошибка базы данных
        """
        try:
            self._con_cursor()
            self.cursor.execute(
                "SELECT version();")
            records = self.cursor.fetchone()
            self.cursor.close()

            print('Соединение с PostgreSQL успешно установлено')
            print('Версия PostgreSQL: ', records[0])
        except Exception as error:
            print(f"ERROR: {error}")
            return 505

    def new_link(self, link: str, hash_link: str) -> Union[int, bool]:
        """
        Создание новой пары длинная ссылка - хэш
        :param link: Длинная (полная) ссылка
        :param hash_link: Хэш-код для короткой ссылки
        :return: 505 - ошибка базы данных, True - успешная запись в базу
        """
        try:
            self._con_cursor()
            self.cursor.execute(f"CALL public.new_link('{link}', '{hash_link}');")
            self.conn.commit()
            self.cursor.close()

            return True
        except Exception as error:
            print(f"ERROR: {error}")
            return 505

    def get_link(self, hash_link: str) -> Union[int, bool, str]:
        """
        Получение длинной ссылки по короткому хэшу
        :param hash_link: хэш-код
        :return: 505 - ошибка базы данных, полная ссылка (строка), False - такого хэша нет
        """
        try:
            self._con_cursor()
            self.cursor.execute(f"SELECT public.get_long_url('{hash_link}');")
            records = self.cursor.fetchone()
            self.cursor.close()

            if records == ():
                return False
            elif records[0] is None:
                return False
            else:
                return records[0]

        except Exception as error:
            print(f"ERROR: {error}")
            return 505
