import psycopg2
from env import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from sqlOperations import Sql


sql = Sql("user")


class DatabaseError(Exception):
    pass


class PostgreSQLDatabase:

    def __init__(self):
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD
        self.db_host = DB_HOST
        self.db_port = DB_PORT

    def connect(self):
        try:
            connection = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
        except Exception:
            raise DatabaseError
        return connection

    def init_table(self):
        with self.connect() as c:
            cur = c.cursor()
            query = """
                    CREATE TABLE IF NOT EXISTS "user" (
                    user_id VARCHAR(255),
                    server_id VARCHAR(255), 
                    status INTEGER,
                    in_time REAL,
                    total_time REAL,
                    weekly_time REAL,
                    daily_time REAL,
                    last_updated DATE,
                    PRIMARY KEY (user_id, server_id)
                    );
                    """
            cur.execute(query)
            c.commit()

    def insert(self, fields, values):
        with self.connect() as c:
            cur = c.cursor()
            query = sql.insert(fields)
            cur.execute(query, values)
            c.commit()

    def select(self, fields, constraint_key, constraint_value):
        with self.connect() as c:
            cur = c.cursor()
            query = sql.select(fields, constraint_key)
            if constraint_value is not None:
                cur.execute(query, constraint_value)
            else:
                cur.execute(query)
            val = cur.fetchall()
        return val

    def delete(self, constraint_key, constraint_value):
        with self.connect() as c:
            cur = c.cursor()
            query = sql.delete(constraint_key)
            cur.execute(query, constraint_value)
            c.commit()

    def update(self, fields, values, constraint_key, constraint_value):
        with self.connect() as c:
            cur = c.cursor()
            query = sql.update(fields, constraint_key)
            cur.execute(query, values + constraint_value)
            c.commit()

    def update_many(self, fields, values_list, constraint_key, constraint_value_list):
        with self.connect() as c:
            cur = c.cursor()
            query = sql.update(fields, constraint_key)
            for i, values in enumerate(values_list):
                cur.execute(query, values + constraint_value_list[i])
            c.commit()

    def drop_table(self):
        with self.connect() as c:
            cur = c.cursor()
            cur.execute(sql.drop_table())
            c.commit()


def list_tables(connection):
    query = """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE (table_schema = 'public')
            ORDER BY table_name;
            """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    result = cursor.fetchall()
    return result


def list_fields(connection, name):
    """
    returns a python list of field names
    """
    query = """ 
            SELECT column_name FROM
            INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s;
            """
    cursor = connection.cursor()
    cursor.execute(query, (name, ))
    result = cursor.fetchall()
    fields = [field[0] for field in result]
    return fields


def list_schema(connection):
    table_names = list_tables(connection)
    with open("DB_SCHEMA.txt", "w", encoding="utf-8") as f:
        cur = connection.cursor()
        for el in table_names:
            if el[1] != 'pg_stat_statements':
                query = f""" SELECT * FROM "{el[1]}" ; """
                cur.execute(query)
                result = cur.fetchall()
                f.write(f"===TABLE: {el[1]}===\n")
                f.write(f"Columns: {list_fields(connection, el[1])}\n")
                for r in result:
                    f.write(f"{r}\n")


if __name__ == "__main__":
    db = PostgreSQLDatabase()
    all_fields = ['user_id', 'server_id', 'status', 'in_time',
                  'total_time', 'weekly_time', 'daily_time', 'last_updated']
    with db.connect() as c:
        list_schema(c)
