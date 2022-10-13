from mysql.connector import MySQLConnection

class SqlWorker:

    SELECT_DUPLICATES_SQL = """
    select count(*) as _count from module_record where id not in
    (
        select *
        from (select min(mr.id) from module_record mr group by mr.module_id, mr.user_id) as temp
    )
    """

    DELETE_DUPLICATES_SQL = """
    delete from module_record where id not in
    (
        select *
        from (select min(mr.id) from module_record mr group by mr.module_id, mr.user_id) as temp
    )
    """

    def __init__(self, mysql_connection: MySQLConnection):
        self.mysql_connection = mysql_connection
    
    def _execute(self, sql):
        with self.mysql_connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def delete_duplicates(self):
        print("Deleting duplicated module record rows")
        self._execute(self.DELETE_DUPLICATES_SQL)
        self.mysql_connection.commit()

    def get_duplicate_count(self):
        print("Getting number of duplicated module record rows")
        res = self._execute(self.SELECT_DUPLICATES_SQL)
        return res[0][0]