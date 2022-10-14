import pandas as pd
import psycopg2
import csv


from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return cur


def get_report(cursor):
    """ Метод создающий файл отчёта по базе данных"""

    # 1 информация по таблицам
    t_query = """SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = 'public'"""
    cursor.execute(t_query)
    names = [names[0] for names in cursor.fetchall()]

    tables_report = []

    for table_name in names:
        # взять мощность отношения
        cursor.execute("""
            SELECT COUNT(1) FROM {}
            """.format(table_name))
        cardinality = cursor.fetchone()[0]
        # взять степень отношения
        cursor.execute("""
            SELECT COUNT(1) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{}'
            """.format(table_name))
        degree = cursor.fetchone()[0]

        tables_report.append({
            "table_name": table_name,
            "cardinality": cardinality,
            "degree": degree,
        })

    # 2 информация по столбцам таблицы
    columns_report = []

    for table_name in names:
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{}'
        """.format(table_name))

        columns = [(c[0], c[1]) for c in cursor.fetchall()]

        for column in columns:
            column_name = column[0]
            data_type = column[1]
            unique = None
            max_value = None
            min_value = None

            if data_type in ["character varying", "text"]:
                # количество уникальных значений в таблице
                cursor.execute(f"""
                    SELECT DISTINCT {column_name}
                    FROM {table_name}
                """)
                unique = len(cursor.fetchall())
                # минимальная и максимальная длина строки
                cursor.execute(f"""
                    SELECT MAX(LENGTH({column_name})), MIN(LENGTH({column_name}))
                    FROM {table_name}
                """)
                res = cursor.fetchone()
                max_value, min_value = res[0], res[1]
            elif data_type in ["daterange", "ARRAY"]:
                pass
            else:
                cursor.execute(f"""
                    SELECT MAX({column_name}), MIN({column_name})
                    FROM {table_name}
                    BETWEEN 
                """)
                res = cursor.fetchone()
                max_value, min_value = res[0], res[1]

            columns_report.append({
                "table_name": table_name,
                "column_name": column_name,
                "data_type": data_type,
                "unique_values_count": unique,
                "max_value": max_value,
                "min_value": min_value,
            })

    save_to_csv("tables.csv", tables_report)
    save_to_csv("columns.csv", columns_report)


def save_to_csv(filename, array):
    with open("../results/"+filename, "w", encoding="UTF-8", newline='\r\n') as csvfile:
        header = array[0].keys()
        writer = csv.DictWriter(f=csvfile, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for k in array:
            writer.writerow(k)


if __name__ == '__main__':
    cur = connect()
    get_report(cur)
