from typing import List

import pymysql


class Client(object):
    def __init__(self,
                 host,
                 port,
                 user,
                 password,
                 db,
                 charset='utf8mb4'):
        self._connection = pymysql.connect(host=host,
                                           user=user,
                                           port=port,
                                           password=password,
                                           db=db,
                                           charset=charset,
                                           cursorclass=pymysql.cursors.DictCursor)

    @property
    def connection(self):
        return self._connection

    def select(self,
               table: str,
               fields: List[str],
               filters: List[str] = None):

        sql_query = self._gen_select_sql_string(
            table=table,
            fields=fields,
            filters=filters
        )

        with self.connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql_query)
            result = cursor.fetchall()

        return result

    def insert(self,
               table: str,
               fields: List[str],
               data: list,
               on_duplicate: str = None) -> None:

        if on_duplicate == 'update':
            sql_query = self._gen_upsert_sql_string(table=table,
                                                    fields=fields)
        else:
            sql_query = self._gen_insert_sql_string(table=table,
                                                    fields=fields)

        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute(sql_query, data)
            self.connection.commit()
        except Exception as e:
            if on_duplicate == 'ignore':
                pass
            else:
                raise e

    @staticmethod
    def _gen_fields(fields: List[str]) -> (str, str):
        fields_str = ", ".join(["`" + pymysql.escape_string(field) + "`" for field in fields])
        placeholders_str = ", ".join(["%s" for field in fields])
        return fields_str, placeholders_str

    def _gen_select_sql_string(self,
                               table: str,
                               fields: List[str],
                               filters: List[str] = None) -> str:

        table = "`" + pymysql.escape_string(table) + "`"
        fields, placeholders = self._gen_fields(fields)

        sql_string = """
        SELECT {fields}
        FROM {table}
        """.format(
            table=table,
            fields=fields
        )

        if filters:
            sql_string = """
            {sql_string}
            WHERE {filters}""".format(
                sql_string=sql_string,
                filters=" and ".join(filters)
            )

        return sql_string

    def _gen_insert_sql_string(self,
                               table: str,
                               fields: List[str]) -> str:

        table = "`" + pymysql.escape_string(table) + "`"
        fields, placeholders = self._gen_fields(fields)

        sql_string = """
        INSERT INTO {table}
            ({fields})
        VALUES
            ({placeholders})""".format(
            table=table,
            fields=fields,
            placeholders=placeholders
        )

        return sql_string

    def _gen_upsert_sql_string(self,
                               table: str,
                               fields: List[str]) -> str:

        insert_sql_string = self._gen_insert_sql_string(table=table,
                                                        fields=fields)

        assignments = ["`{x}` = VALUES(`{x}`)".format(
            x=pymysql.escape_string(x)
        ) for x in fields]

        upsert_sql_string = """
        {insert_sql_string}
        ON DUPLICATE KEY UPDATE {assignments}
        """.format(insert_sql_string=insert_sql_string,
                   assignments=", ".join(assignments))

        return upsert_sql_string
