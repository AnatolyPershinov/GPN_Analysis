import csv
import warnings
import logging
import os
import pandas as pd
import sys
import time

from getfiles import save_to_csv, check_files
from parse_words import Calc 


warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.info("script started")


def check_matching(word: str, keywords: list[str]):
    """метод проверяет входит ли хотя-бы одно слово из списка keywords в строку word"""
    for k in keywords:
        if k in word:
            return True
    return False


def simple_str(string: str):
    """Мето удаляет символы пробела, переноса строки, табуляции, избавляется от заглавных букв
    если строка, после удаления из неё точек, может быть считана как число, то, функция вернёт None"""
    res = string.lower().replace("_", "").replace(" ", "")
    res = res.replace("\n", "").replace("\t", "")
    res = res.replace(".", "").replace(",", "")
    if res.isdigit() or res == "":
       return None
    else:
        return res

def read(file):
    """считывает файлы xl
    возращает список с уникальными словами для каждого файла"""

    engines = {
        "lsb": "pyxlsb",
        "lsm": "openpyxl",
        "xls": "xlrd",
        "lsx": "openpyxl",
    }
    
    ext = file[-3:]
    df_dict = pd.read_excel(file, engine=engines[ext], sheet_name=None, header=None)
    
    res = []
    for k, v in df_dict.items():
        for r in v.values.tolist():
            res.extend(r)
            
    res = {simple_str(k) for k in res if type(k) is str}
    if None in res:
        res.remove(None)
    
    return res
    

def parse_all_words(files):
    """основной метод. отправляет файлы на чтение 
    затем вызывает метод обработки для каждого файла
    собирает данные в список result"""
    count = 0
   
    for path in files:
        count+=1
        try:
            group = path[0]
            file = path[1]
        except IndexError as e: 
            logging.error(f"{e} {path}")
        try:
            array = read(file)
        except Exception as e:
            print("НЕ УДАЛОСЬ ПРОЧИТАТЬ ФАЙЛ {} {}".format(path, e))
        try:
            result.handle_data(array, group)
            print("ПРОЧИТАН ФАЙЛ {}/{}   {}".format(count, len(files), path[1]))
        except Exception as e:
            print("ПРОПУЩЕН ФАЙЛ {} {}".format(count, path))
            logging.error(f"{e} {path}")

        
def find_files_with_param(files: list, keywords: list):
    res = []
    """метод, которые ищет файлы, со словами из списка keywords"""
    count = 0
   
    for path in files:
        count+=1
        try:
            group = path[0]
            file = path[1]
            _file = file.split(group)[1]

        except IndexError as e: 
            logging.error(f"{e} {path}")
        try:
            words = read(file)
            array = [k for k in words if check_matching(word=k, keywords=keywords)]
            print("ПРОЧИТАН ФАЙЛ {}/{}   {}".format(count, len(files), path[1]))
            res.append({
                "group": group,
                "file": f"{group}\\{_file}",
                "guid_count": len(array),
                "body": None if len(array) == 0 else str(array), 
            })
        except Exception as e:
            print("НЕ УДАЛОСЬ ПРОЧИТАТЬ ФАЙЛ {} {}".format(path, e))
            continue

    return res


def prepare_files():
    """находит все xl файлы по пути DATA\\<group_name>, 
    где имя группы - название месторождения сохраняет их в csv"""
    
    __GROUPS__ = ["\\СМГ Зима", "\\СМГ Мессояха", "\\Томский интегрированный проект", "\\СМГ Н.Порт"]
    
    try:
        save_to_csv("results\\files.csv", check_files(__GROUPS__))
    except Exception as e:
        logging.error(f"{e}")
        




if __name__ == "__main__":   
    """точка входа"""
    
    prepare_files()
    result = Calc()
    """считать список файлов"""
    with open("results\\files.csv", "r", encoding="UTF-8", newline="") as f:
        files = csv.reader(f, delimiter="\t", quotechar='|')
        files = list(files)[1:]
    
    
    # result = find_files_with_param(files, keywords=["id"])
    # save_to_csv("results\\files_guid.csv", result)
    
    parse_all_words(files)
    save_to_csv('results\\result_04_11_2022.csv', result.get_report())
    
    # выделить в отдельный метод
    # df = pd.read_csv("results\\mpresult.csv", delimiter="\t")
    # df = df.sort_values(by='total_count',  ascending=False)
    # df.to_csv("results\\result.csv")
    