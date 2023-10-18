import mysql.connector
import logging

from mysql.connector import Error

from app.config.config import (DB_HOST, DB_PORT,
                               DB_USERNAME, DB_PASSWORD,
                               DB_DATABASE)

from typing import Union, Any

from pypika import Query, Table, Order


class DB:
    def __init__(self):
        self.HOST = DB_HOST
        self.PORT = DB_PORT
        self.USERNAME = DB_USERNAME
        self.PASSWORD = DB_PASSWORD
        self.DATABASE = DB_DATABASE

        self.connection = None
        self.cursor = None

    def select(self, table_name: str, *args: Any) -> list:
        table = Table(table_name)
        if args:
            q = Query.from_(table).select(*[getattr(table, arg) for arg in args])
        else:
            q = Query.from_(table).select(table.star)
        result = self.__execute_query(q.get_sql(quote_char=None))
        return result

    def select_where(self, table_name: str, where_cond, where_value) -> list:
        table = Table(table_name)
        q = Query.from_(table).select(table.star).where(getattr(table, where_cond) == where_value)
        result = self.__execute_query(q.get_sql(quote_char=None))
        if not result:
            return []
        return result

    def insert(self, table_name: str, **kwargs: Any) -> bool:
        try:
            q = Query.into(Table(table_name)).columns(*kwargs.keys()).insert(*kwargs.values())
            self.__execute_query(q.get_sql(quote_char=None))
        except Exception:
            return False
        return True

    def delete(self, table_name: str, where_cond: Any, where_value: Any) -> bool:
        """

        :param table_name: Название таблицы
        :param where_cond: Условие WHERE
        :param where_value: Значение WHERE
        :return:
        """
        table = Table(table_name)
        try:
            q = Query.from_(table).delete().where(getattr(table, where_cond) == where_value)
            self.__execute_query(q.get_sql(quote_char=None))
        except Exception:
            return False
        return True

    def update(self, table_name: str, where_cond: Any, where_value: Any, **kwargs):
        """

        :param table_name: Название таблицы
        :param where_cond: Условие WHERE
        :param where_value: Значение WHERE
        :return:
        """
        table = Table(table_name)
        try:
            q = Query.update(table).where(getattr(table, where_cond) == where_value)
            print(q)
            for key, value in kwargs.items():
                q = q.set(key, value)
            self.__execute_query(q.get_sql(quote_char=None))
        except Exception:
            return False
        return True

    def get_last_row_id(self, table_name: str):
        try:
            table = Table(table_name)
            q = Query.from_(table).select('id').orderby('id', order=Order.desc).limit(1)
            result = self.__execute_query(q.get_sql(quote_char=None))
            if not result:
                return 1
            return int(result[0][0])
        except Error as err:
            logging.error(f"Error while getting LRid to {DB_USERNAME}@{DB_HOST}:{DB_PORT} | {err}")
        finally:
            self.__disconnect()

    def __connect(self) -> Union[mysql.connector.MySQLConnection, None]:
        try:
            self.connection = mysql.connector.connect(
                host=self.HOST,
                user=self.USERNAME,
                password=self.PASSWORD,
                database=self.DATABASE,
                charset='utf8'
            )
            if self.connection.is_connected():
                # logging.info(f"Successfully connected to {DB_USERNAME}@{DB_HOST}:{DB_PORT}")
                return self.connection
        except Error as err:
            logging.error(f"Error while connecting to {DB_USERNAME}@{DB_HOST}:{DB_PORT} | {err}")
            return None

    def __disconnect(self) -> None:
        if self.connection.is_connected():
            self.connection.close()
            # logging.info(f"Successfully closed connection to {DB_USERNAME}@{DB_HOST}:{DB_PORT}")

    def __execute_query(self, query: str) -> Any:
        try:
            self.__connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()
            # logging.info(f"Successfully executed query to {DB_USERNAME}@{DB_HOST}:{DB_PORT}")
            return result
        except Error as err:
            logging.error(f"Error while executing query to {DB_USERNAME}@{DB_HOST}:{DB_PORT} | {err}")
        finally:
            self.__disconnect()


if __name__ == '__main__':
    pass
