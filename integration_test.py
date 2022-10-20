import random
from script import run
from config import LEARNER_RECORD_DATABASE_DATABASE, LEARNER_RECORD_DATABASE_HOST, LEARNER_RECORD_DATABASE_PW, LEARNER_RECORD_DATABASE_USER
from mysql import connector

from sql import SqlWorker

conn = connector.connect(
        user=LEARNER_RECORD_DATABASE_USER,
        password=LEARNER_RECORD_DATABASE_PW,
        host=LEARNER_RECORD_DATABASE_HOST,
        port=3306,
        database=LEARNER_RECORD_DATABASE_DATABASE
    )

conn.autocommit = True

INSERT_COURSE_RECORD_SQL = """
INSERT INTO course_record
(course_id, user_id)
VALUES {values};
"""

INSERT_COURSE_RECORD_VALUES_SQL = "('{course_id}', '{user_id}')"

INSERT_MODULE_RECORD_SQL = """
INSERT INTO module_record
(module_id, course_id, user_id)
VALUES {values};
"""

INSERT_MODULE_RECORD_VALUES_SQL = "('{module_id}', '{course_id}', '{user_id}')"

TEARDOWN_COURSE_RECORD_SQL = """
DELETE FROM course_record
WHERE course_id like 'DUP_TEST_%'
"""

TEARDOWN_MODULE_RECORD_SQL = """
DELETE FROM module_record
WHERE course_id like 'DUP_TEST_%'
"""

COUNT_TEST_RECORDS_SQL = """
SELECT COUNT(*)
FROM module_record
WHERE module_id like 'DUP_TEST_%'
"""

def generate_random_id():
    random_id = ''.join(random.choice('0123456789ABCDEF') for i in range(20))
    return f"DUP_TEST_{random_id}"

def teardown():
    print("Tearing down")
    with conn.cursor() as cursor:
        cursor.execute(TEARDOWN_MODULE_RECORD_SQL)
        cursor.execute(TEARDOWN_COURSE_RECORD_SQL)

def insert_course_records(rows):
    values_sql = ",".join([INSERT_COURSE_RECORD_VALUES_SQL.format(course_id=row['course_id'], user_id=row['user_id']) for row in rows])
    sql = INSERT_COURSE_RECORD_SQL.format(values=values_sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)

def insert_module_records(rows):
    values_sql = ",".join([INSERT_MODULE_RECORD_VALUES_SQL.format(course_id=row['course_id'], user_id=row['user_id'], module_id=row['module_id']) for row in rows])
    sql = INSERT_MODULE_RECORD_SQL.format(values=values_sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)

def count_test_records():
    with conn.cursor() as cursor:
        cursor.execute(COUNT_TEST_RECORDS_SQL)
        return cursor.fetchall()[0][0]

def generate_records(number_of_users, number_of_duplicates_per_user):
    course_record_rows = []
    module_record_rows = []
    for u in range(number_of_users):
        user_id = generate_random_id()
        course_id = generate_random_id()
        module_id = generate_random_id()
        print(f"inserting course record {course_id}, {user_id}")
        course_record_rows.append({"course_id": course_id, "user_id": user_id})
        for i in range(number_of_duplicates_per_user):
            print(f"inserting module record {module_id}, {course_id}, {user_id}")
            module_record_rows.append({"course_id": course_id, "user_id": user_id, "module_id": module_id})

    insert_course_records(course_record_rows)
    insert_module_records(module_record_rows)


def test_record_deletion():
    number_of_users = 20
    number_of_duplicates_per_user = 3
    expected_duplicates = number_of_users * number_of_duplicates_per_user
    teardown()
    worker = SqlWorker(conn)
    # + 1 for the rows that are intended to be left behind after the deletion
    generate_records(number_of_users, number_of_duplicates_per_user+1)
    duplicate_count = worker.get_duplicate_count()

    print(f"Expected duplicates {expected_duplicates} and duplicate count was {duplicate_count}")
    assert duplicate_count == expected_duplicates
    
    worker.delete_duplicates()
    remaining_rows = count_test_records()

    print(f"Expected remaining rows {number_of_users} and actual count was {remaining_rows}")
    assert remaining_rows == number_of_users
    teardown()

test_record_deletion()