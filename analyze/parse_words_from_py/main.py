from pathlib import Path
import sys

import csv
import warnings
import logging
import os
import sys
import time
import re

from getfiles import check_files, save_to_csv


warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.info("script started")


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
    """считывает файлы py
    возращает список с русскими словами"""
    
    r = re.compile('[А-яё]+')

    with open(file, "r", encoding="UTF-8") as f:
        content = f.read()

    rows = content.split("\n")

    content = [k.split("#")[0] if "#" in k else k for k in rows] # очистить код от комментариев
    content = [k.replace("\t", "") for k in content]
    content = [k for k in content if k != None and k != ""] # оставить только строки с кодом

    res_rows = [k for k in content if len(re.findall(r"[А-яё№]+", k)) > 0] # найти строки с русскими словами

    res_rows = [re.findall(r"[/\\А-яё№ ]+", k) for k in res_rows]
    return res_rows
    

def handle(files):
    """основной метод. отправляет файлы на чтение 
    затем вызывает метод обработки для каждого файла
    собирает данные в список result"""
    count = 0

    result = []
   
    for path in files:
        count+=1
        try:
            group = path[0]
            file = path[1]
        except IndexError as e: 
            logging.error(f"{e} {path}")

        array = read(file)

        for rows in array:
            rows = set(rows)
            for k in rows:
                if k == "" or k == "" or k == " " or k.replace(" ", "") == '':
                    continue

                result.append({
                    "group": group,
                    "file": file,
                    "keywords": k
                })
        
    return result


            

def prepare_files():
    """находит все xl файлы по пути DATA\\<group_name>, 
    где имя группы - название месторождения сохраняет их в csv"""
    
    __GROUPS__ = ["\\СМГ Мессояха", "\\СМГ ННГ", "\\Томский интегрированный проект"]
    
    try:
        save_to_csv("parse_words_from_py\\results\\files.csv", check_files(__GROUPS__, name=".py"))
    except Exception as e:
        logging.error(f"{e}")


def main():
    """точка входа"""
    
    prepare_files()
    """считать список файлов"""
    with open("parse_words_from_py\\results\\files.csv", "r", encoding="UTF-8", newline="") as f:
        files = csv.reader(f, delimiter="\t", quotechar='|')
        files = list(files)[1:]

    

    save_to_csv('parse_words_from_py\\results\\keywords.csv', handle(files))
    
    # выделить в отдельный метод
    # df = pd.read_csv("results\\mpresult.csv", delimiter="\t")
    # df = df.sort_values(by='total_count',  ascending=False)
    # df.to_csv("results\\result.csv")
    