import datetime
import unittest

import pymysql
import testing.mysqld
from sqlalchemy import create_engine, MetaData, Table

from mysqltoolkit import Client

import db_model as db_model

MYSQLD_FACTORY = testing.mysqld.MysqldFactory(cache_initialized_db=True)


def tearDownModule():
    """Tear down databases after test script has run.
    https://docs.python.org/3/library/unittest.html#setupclass-and-teardownclass
    """
    MYSQLD_FACTORY.clear_cache()


class TestClient(unittest.TestCase):

    table = 'ComplexTable'

    @classmethod
    def setUpClass(cls):
        cls.mysql = MYSQLD_FACTORY()
        cls.params = cls.mysql.dsn()
        cls.db_engine = create_engine(cls.mysql.url())
        cls.session = db_model.db_init(cls.db_engine)
        metadata = MetaData(bind=cls.db_engine)
        line_item = Table(cls.table, metadata, autoload=True)

        cls.db_config = {
            'engine': cls.db_engine,
            'table': line_item
        }

    def setUp(self) -> None:
        self.client = Client(
            host=self.params['host'],
            user=self.params['user'],
            port=self.params['port'],
            password='',
            db=self.params['db']
        )

    def test_get_connection_success(self):
        self.assertTrue(isinstance(self.client.connection, pymysql.connections.Connection))

    def test_select_with_filter_succeed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        data = ['DS_0',
                '2020-03-13',
                1,
                2,
                3,
                4,
                5,
                6,
                7]

        self.client.insert(
            table=table,
            fields=schema,
            data=data
        )

        client_result = self.client.select(
            table=table,
            fields=['id'],
            filters=['itemId="DS_0"']
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM {} where itemId='DS_0'"
                           .format(table))
            # get id
            result = cursor.fetchone()

        self.assertEqual(client_result[0].get('id'), result.get('id'))

    def test_select_without_filter_succeed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        data = ['DS_00',
                '2020-03-13',
                1,
                2,
                3,
                4,
                5,
                6,
                7]

        self.client.insert(
            table=table,
            fields=schema,
            data=data
        )

        client_result = self.client.select(
            table=table,
            fields=['id']
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM {}".format(table))
            # get id
            result = cursor.fetchall()

        self.assertListEqual(client_result, result)

    def test_update_database_insert_a_new_data_succeed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        data = ['DS_1',
                '2020-03-13',
                1,
                2,
                3,
                4,
                5,
                6,
                7]

        self.client.insert(
            table=table,
            fields=schema,
            data=data
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where itemId='DS_1'"
                           .format(table))
            # get id
            result = cursor.fetchone()
            self.assertEqual(result.get('itemId'), "DS_1")
            self.assertEqual(result.get('date'), datetime.datetime(2020, 3, 13, 0, 0))
            self.assertEqual(result.get('field1'), 1)
            self.assertEqual(result.get('field2'), 2)
            self.assertEqual(result.get('field3'), 3)

    def test_update_database_insert_duplicated_data_failed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        data = ['DS_2',
                '2020-03-13',
                1,
                2,
                3,
                4,
                5,
                6,
                7]

        self.client.insert(
            table=table,
            fields=schema,
            data=data
        )

        with self.assertRaises(pymysql.err.IntegrityError):
            self.client.insert(
                table=table,
                fields=schema,
                data=data
            )

    def test_update_database_upsert_duplicated_data_succeed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        old_data = ['DS_3',
                    '2020-03-13',
                    1,
                    2,
                    0,
                    4,
                    7,
                    8,
                    9]

        new_data = ['DS_3',
                    '2020-03-13',
                    2,
                    2,
                    6,
                    4,
                    7,
                    8,
                    9]

        self.client.insert(
            table=table,
            fields=schema,
            data=old_data
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where itemId='DS_3'"
                           .format(table))
            # get id
            old_result = cursor.fetchone()
            old_result_id = old_result.get('id')

        self.client.insert(
            table=table,
            fields=schema,
            data=new_data,
            on_duplicate='update'
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where itemId='DS_3'"
                           .format(table))
            # get id
            new_result = cursor.fetchone()

        self.assertEqual(new_result.get('id'), old_result_id)
        self.assertEqual(new_result.get('itemId'), "DS_3")
        self.assertEqual(new_result.get('date'), datetime.datetime(2020, 3, 13, 0, 0))
        self.assertEqual(new_result.get('field1'), 2)
        self.assertEqual(new_result.get('field2'), 2)
        self.assertEqual(new_result.get('field3'), 6)
        self.assertEqual(new_result.get('field4'), 4)
        self.assertEqual(new_result.get('field5'), None)
        self.assertEqual(new_result.get('field6'), None)
        self.assertEqual(new_result.get('field7'), 7)
        self.assertEqual(new_result.get('field8'), 8)
        self.assertEqual(new_result.get('field9'), 9)

    def test_ignore_duplicated_data_succeed(self):
        table = 'ComplexTable'
        schema = ['itemId',
                  'date',
                  'field1',
                  'field2',
                  'field3',
                  'field4',
                  'field7',
                  'field8',
                  'field9']

        old_data = ['DS_4',
                    '2020-03-13',
                    1,
                    2,
                    0,
                    4,
                    7,
                    8,
                    9]

        new_data = ['DS_4',
                    '2020-03-13',
                    2,
                    2,
                    6,
                    4,
                    7,
                    8,
                    9]

        self.client.insert(
            table=table,
            fields=schema,
            data=old_data
        )

        self.client.insert(
            table=table,
            fields=schema,
            data=new_data,
            on_duplicate='ignore'
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where itemId='DS_4'"
                           .format(table))
            # get id
            result = cursor.fetchone()

        self.assertEqual(result.get('itemId'), "DS_4")
        self.assertEqual(result.get('date'), datetime.datetime(2020, 3, 13, 0, 0))
        self.assertEqual(result.get('field1'), 1)
        self.assertEqual(result.get('field2'), 2)
        self.assertEqual(result.get('field3'), 0)

    def test_upsert_single_duplicated_data_succeed(self):
        table = 'BasicTable'
        schema = ['basic']

        data = ['foo']

        self.client.insert(
            table=table,
            fields=schema,
            data=data
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where basic='foo'"
                           .format(table))
            # get id
            old_result = cursor.fetchone()
            old_id = old_result.get('id')

        # insert/update data
        self.client.insert(
            table=table,
            fields=schema,
            data=data,
            on_duplicate='update'
        )

        with self.client.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} where basic='foo'"
                           .format(table))
            # get id
            new_result = cursor.fetchone()
            new_id = new_result.get('id')

        self.assertEqual(new_id, old_id)

    def tearDown(self) -> None:
        self.client.connection.close()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.stop()
