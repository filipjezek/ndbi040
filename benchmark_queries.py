#!/usr/bin/python3
import pyodbc
import os
from pathlib import Path
import timeit


class Benchmark:
    def __init__(self) -> None:
        conn = pyodbc.connect(
            'DRIVER={VIRTUOSO_DRIVER};UID={VIRTUOSO_USER};PWD={VIRTUOSO_PASSWORD};HOST={VIRTUOSO_HOST}'.format(
                **os.environ),
            autocommit=True
        )
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')
        self.__cursor = conn.cursor()
        self.__cursor.execute('USE db')

    def __test_query(self, query: str, iterations=500):
        start = timeit.default_timer()

        # executemany compiles and reuses the statement
        # this means that the actual parsing will only be
        # done once
        self.__cursor.executemany(query, (tuple() for _ in range(iterations)))

        end = timeit.default_timer()
        print(f'{(end - start) / iterations} seconds')

    def test_queries(self, iterations=500):
        curdir = Path(__file__).parent / 'queries'
        for file in sorted(curdir.glob('*.sql')):
            with open(str(file), 'r') as query:
                print(f'{file}:')
                self.__test_query(query.read(), iterations)
                print('')


if __name__ == '__main__':
    b = Benchmark()
    b.test_queries()
