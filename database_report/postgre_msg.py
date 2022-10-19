import numpy as np
import pandas as pd
import psycopg2
import csv
import warnings

from config import config


warnings.filterwarnings(action='ignore')


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
            return conn


def cut_tails(array, min, max):
    array_cut = []
    qmax, qmin = np.percentile(array, [max, min])
    interval = qmax - qmin

    min_dist = qmin - (1.5 * interval)
    max_dist = qmax + (1.5 * interval)
    
    if min_dist is None or max_dist is None:
        return array
    for data in array:
        if data < max_dist and data > min_dist:
            array_cut.append(data)
            
    return array_cut


def get_report(conn):
    """ Метод создающий файл отчёта по базе данных"""
    cursor = conn.cursor()
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

            print(f"handle {column_name} from {table_name}")

            if data_type != "daterange":
                max_value, min_value = findbounds(conn, table_name, column_name, data_type)

            # количество уникальных значений в таблице (и)

            cursor.execute(f"""
                SELECT DISTINCT {column_name}
                FROM {table_name}
            """)
            unique = len(cursor.fetchall())
                
            cursor.execute(f"""
                SELECT {column_name}
                FROM {table_name}
                WHERE {column_name} IS NOT Null 
            """)
            not_null = len(cursor.fetchall())

            cursor.execute(f"""
                SELECT {column_name}
                FROM {table_name}
            """)
            total = len(cursor.fetchall())

            columns_report.append({
                "table_name": table_name,
                "column_name": column_name,
                "data_type": data_type,
                "unique_values_count": unique,
                "max_value": max_value,
                "min_value": min_value,
                "not_null_count": not_null,
                "total_count": total,
            })

    save_to_csv("tables.csv", tables_report)
    save_to_csv("columns.csv", columns_report)


# функция обрежет выборку и найдет по ним min / max
def findbounds(connect, table, column, data_type):
    query = f"SELECT {column} from {table}"
    df = pd.read_sql_query(query, con=connect)
    # обрезаем хвосты только для чисел и строк. 
    # в сулчае с id и датой просто берем максимум и минимум
    if column == "rid":
        cut_array = [d[0] for d in df.values]
    elif data_type == "date":
        cut_array = [d[0] for d in df.values]
    else:
        if data_type in ["character varying", "text", "ARRAY"]:  # формируем массивы для анализа данных.
            array = np.array([len(d[0]) if d[0] is not None else 0 for d in df.values])  # в случае текстовых полей записываем длину в список
        else:
            array = np.array([d[0] if d[0] is not None else 0 for d in df.values])  # числа приводим к единому виду
        
        cut_array = cut_tails(array, 5, 95)  # обрезка хвостов. 5% и 95%

    try:
        return min(cut_array), max(cut_array)
    except Exception as e:
        print(column, data_type, e)
        return 0, 0


def save_to_csv(filename, array):
    with open("results/"+filename, "w", encoding="UTF-8", newline='\r\n') as csvfile:
        header = array[0].keys()
        writer = csv.DictWriter(f=csvfile, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for k in array:
            writer.writerow(k)


if __name__ == '__main__':
    conn = connect()
    get_report(conn)
