from mysql import connector

from sql import SqlWorker

def run(db_user, db_password, db_host, db_database, delete_records=False):
    conn = connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=3306,
        database=db_database
    )
    worker = SqlWorker(conn)
    number_of_duplicate_rows = worker.get_duplicate_count()
    print(f"There are currently {number_of_duplicate_rows} duplicate module record rows in the database")
    if number_of_duplicate_rows > 0 and delete_records:
        worker.delete_duplicates()
        print("Deleted duplicates")