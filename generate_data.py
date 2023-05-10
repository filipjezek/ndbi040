#!/usr/bin/python3
import pyodbc
import os
import random
import wonderwords
from faker import Faker


class DataGenerator:
    def __init__(self) -> None:
        conn = pyodbc.connect(
            'DRIVER={VIRTUOSO_DRIVER};UID={VIRTUOSO_USER};PWD={VIRTUOSO_PASSWORD};HOST={VIRTUOSO_HOST}'.format(
                **os.environ),
            autocommit=True
        )
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
        conn.setencoding(encoding='utf-8')
        self.__cursor = conn.cursor()
        self.__cursor.execute('USE db')
        self.__word = wonderwords.RandomWord()
        self.__fake = Faker()

    def generate(self, programmes: int, subjects: int, subj_instances: int, students: int, teachers: int):
        self.__drop_tables()
        print('generating programmes...')
        self.__generate_programmes(programmes)
        print('generate subjects...')
        self.__generate_subjects(subjects)
        print('generate subject instances...')
        self.__generate_subject_instances(subj_instances)
        print('generate students...')
        self.__generate_students(students)
        print('generate teachers...')
        self.__generate_teachers(teachers)

    def __generate_programmes(self, count: int):
        self.__cursor.execute(
            'CREATE TABLE programmes (id INT PRIMARY KEY IDENTITY, name VARCHAR)')
        self.__cursor.executemany(
            'INSERT INTO programmes (name) VALUES (?)',
            ((val,) for val in self.__random_programmes(count))
        )

    def __generate_subjects(self, count: int):
        self.__cursor.execute(
            'CREATE TABLE subjects (id INT PRIMARY KEY IDENTITY, name VARCHAR)')
        self.__cursor.executemany(
            'INSERT INTO subjects (name) VALUES (?)',
            ((val,) for val in self.__random_subjects(count))
        )

    def __generate_subject_instances(self, count: int):
        max_id = self.__cursor.execute(
            'SELECT MAX(id) FROM subjects'
        ).fetchval()
        self.__cursor.execute(
            """CREATE TABLE subject_instances (
                id INT PRIMARY KEY IDENTITY,
                year INT,
                instanceof INT,
                FOREIGN KEY (instanceof) REFERENCES subjects(id)
            )""")
        self.__cursor.executemany(
            'INSERT INTO subject_instances (year, instanceof) VALUES (?, ?)',
            ((random.randint(2000, 2023), random.randint(1, max_id))
             for _ in range(count))
        )

    def __generate_students(self, count: int):
        self.__cursor.execute(
            """CREATE TABLE addresses (
                id INT PRIMARY KEY IDENTITY,
                city VARCHAR,
                line1 VARCHAR,
                line2 VARCHAR
            )""")
        self.__cursor.execute(
            """CREATE TABLE people (
                id INT PRIMARY KEY IDENTITY,
                name VARCHAR,
                birth_date VARCHAR,
                address INT,
                FOREIGN KEY (address) REFERENCES addresses(id)
            )""")
        self.__cursor.execute(
            """CREATE TABLE students (
                id INT,
                FOREIGN KEY (id) REFERENCES people(id),
                UNIQUE (id)
            )""")
        self.__cursor.execute(
            """CREATE TABLE students_programmes (
                id INT PRIMARY KEY IDENTITY,
                student INT,
                programme INT,
                since_date VARCHAR,
                to_date VARCHAR,
                FOREIGN KEY (student) REFERENCES students(id),
                FOREIGN KEY (programme) REFERENCES programmes(id)
            )""")
        self.__cursor.execute(
            """CREATE TABLE students_subjects (
                id INT PRIMARY KEY IDENTITY,
                subject INT,
                student INT,
                FOREIGN KEY (subject) REFERENCES subject_instances(id),
                FOREIGN KEY (student) REFERENCES students(id),
                UNIQUE(student, subject)
            )""")

        self.__cursor.executemany(
            'INSERT INTO addresses (city, line1, line2) VALUES (?, ?, ?)',
            (val for val in self.__random_addresses(count))
        )
        self.__cursor.executemany(
            'INSERT INTO people (name, birth_date, address) VALUES (?, ?, ?)',
            ((*val, i) for i, val in enumerate(self.__random_people(count), 1))
        )
        self.__cursor.executemany(
            'INSERT INTO students (id) VALUES (?)',
            ((i + 1,) for i in range(count))
        )
        self.__cursor.executemany(
            'INSERT INTO students_programmes (student, programme, since_date, to_date) VALUES (?, ?, ?, ?)',
            self.__random_student_programmes(count)
        )
        max_subj = self.__cursor.execute(
            'SELECT MAX(id) FROM subject_instances').fetchval()
        self.__cursor.executemany(
            'INSERT INTO students_subjects (student, subject) VALUES (?, ?)',
            ((i + 1, random.randint(1, max_subj)) for i in range(count))
        )

    def __generate_teachers(self, count: int):
        self.__cursor.execute(
            """CREATE TABLE teachers (
                id INT,
                salary INT,
                FOREIGN KEY (id) REFERENCES people(id)
            )""")
        self.__cursor.execute(
            'ALTER TABLE teachers ADD UNIQUE(id)')
        self.__cursor.execute(
            """CREATE TABLE teachers_degrees (
                id INT PRIMARY KEY IDENTITY,
                teacher INT,
                degree VARCHAR,
                FOREIGN KEY (teacher) REFERENCES teachers(id)
            )""")
        self.__cursor.execute(
            """CREATE TABLE teachers_subjects (
                id INT PRIMARY KEY IDENTITY,
                teacher INT,
                subject INT,
                FOREIGN KEY (teacher) REFERENCES teachers(id),
                FOREIGN KEY (subject) REFERENCES subject_instances(id),
                UNIQUE(teacher, subject)
            )""")

        self.__cursor.executemany(
            'INSERT INTO addresses (city, line1, line2) VALUES (?, ?, ?)',
            (val for val in self.__random_addresses(count))
        )
        self.__cursor.executemany(
            'INSERT INTO people (name, birth_date, address) VALUES (?, ?, ?)',
            ((*val, i) for i, val in enumerate(self.__random_people(count), 1))
        )
        self.__cursor.executemany(
            'INSERT INTO teachers (id, salary) VALUES (?, ?)',
            ((i + 1, random.randint(30000, 60000)) for i in range(count))
        )
        self.__cursor.executemany(
            'INSERT INTO teachers_degrees (teacher, degree) VALUES (?, ?)',
            ((random.randint(1, count), self.__fake.suffix())
             for _ in range(int(count * 1.5)))
        )
        max_subj = self.__cursor.execute(
            'SELECT MAX(id) FROM subject_instances').fetchval()
        self.__cursor.executemany(
            'INSERT INTO teachers_subjects (teacher, subject) VALUES (?, ?)',
            ((i + 1, random.randint(1, max_subj)) for i in range(count))
        )

    def __random_programmes(self, count: int):
        suffixes = ['Theory', 'Management', 'Systems']
        for i in range(count):
            if random.random() < 1 / 3:
                prog: str = self.__word.word(include_categories=['noun'])
            elif random.random() < .5:
                prog = self.__word.word(include_categories=['noun']) +  \
                    ' ' + random.choice(suffixes)
            else:
                prog = self.__word.word(include_categories=['noun']) + \
                    ' and ' + \
                    self.__word.word(include_categories=['noun'])
            yield f'PROG#{i + 1} {prog.title()}'

    def __random_subjects(self, count: int):
        suffixes = ['Theory', 'Management', 'Systems',
                    '101', 'Introduction', 'Seminar']
        for i in range(count):
            if random.random() < 1 / 3:
                prog: str = self.__word.word(include_categories=['noun'])
            elif random.random() < .5:
                prog = self.__word.word(include_categories=['noun']) +  \
                    ' ' + random.choice(suffixes)
            else:
                prog = self.__word.word(include_categories=['noun']) + \
                    ' and ' + \
                    self.__word.word(include_categories=['noun'])
            yield f'SUBJ#{i + 1} {prog.title()}'

    def __random_addresses(self, count: int):
        line2_prefixes = ['Box', 'Suite', 'Appt']

        for _ in range(count):
            city: str = self.__fake.city()
            street: str = self.__fake.street_name()

            if random.random() < .8:
                line2: str = None
            else:
                line2 = random.choice(line2_prefixes) + \
                    ' ' + str(random.randint(10, 200))
            yield (city, str(random.randint(10, 1000)) + ' ' + street, line2)

    def __random_people(self, count: int):
        for i in range(count):
            yield (self.__fake.last_name() + ' ' + self.__fake.first_name(), self.__fake.date_between('-60y', '-20y'))

    def __random_student_programmes(self, count: int):
        max_prog = self.__cursor.execute(
            'SELECT MAX(id) FROM programmes').fetchval()
        for i in range(count):
            date1 = self.__fake.date()
            date2 = self.__fake.date()
            yield (
                i + 1,
                random.randint(1, max_prog),
                min(date1, date2),
                max(date1, date2) if random.random() < .7 else None
            )

    def __drop_table(self, name: str):
        try:
            self.__cursor.execute('DROP TABLE ' + name)
        except:
            pass

    def __drop_tables(self):
        """
        we need to drop the tables in inverse order of their creation
        because of foreign keys
        """
        for table in [
            'teachers_subjects',
            'teachers_degrees',
            'teachers',
            'students_subjects',
            'students_programmes',
            'students',
            'people',
            'addresses',
            'subject_instances',
            'subjects',
            'programmes'
        ]:
            self.__drop_table(table)


if __name__ == '__main__':
    DataGenerator().generate(30, 50, 100, 300, 90)
