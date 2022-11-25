
from analyze import getfiles
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

import sys
print(sys.path)


def simple_str(string: str):
    res = string.lower().replace(" ", "").replace("\n", "").replace(".", "").replace(",", "")
    return res


def analyze(sheet: pd.DataFrame):
    """получить таблицу работ"""
    res = pd.DataFrame()
    guid = guid_contain(sheet)

    if guid == -1:
        return None
    
    res = sheet[(sheet == "план").any(axis=1)]
    head = [guid + k for k in [0, 1, 2, 3]]
    res = res[head]
    # res.dropna(subset=[head[:-1]])
    res = res.rename(columns={guid+0: "guid", guid+1: "work id", guid+2: "work title", guid+3: "contractor"})
    return res[1:]


def guid_contain(sheet):
    """есть ли на странице упоминание guid 
    если есть - венуть номер колонки с ним"""
    res = []
    array = sheet.values.tolist()
    for i in range(len(array)):
        # поиск строки с guid
        res = [simple_str(k) for k in array[i] if type(k) is str]
        _res = [k for k in res if "guid" in k]

        if len(_res) > 0:
            # поиск номера столбца guid
            for cell in array[i]:
                if not type(cell) is str:
                    continue
                if "guid" in simple_str(cell):
                    return array[i].index(cell)
    return -1
        

def read(file):    
    """считывает файлы xl
    возращает список с уникальными словами для каждого файла"""

    json_file_name = file.split("DATA\\")[1]
    json_file_name = json_file_name.replace("\\", "/")

    print(json_file_name)
    engines = {
        "lsb": "pyxlsb",
        "lsm": "openpyxl",
        "xls": "xlrd",
        "lsx": "openpyxl",
    }
    
    ext = file[-3:] # берём расширение файла. в зависимости от него выбираем движок
    df_dict = pd.read_excel(file, engine=engines[ext], sheet_name=None, header=None)

    res = pd.DataFrame()
        
    for k, sheet in df_dict.items():
        df = analyze(sheet)
        if df is None:
            continue
        df[["sheet", "file_name"]] = [k, json_file_name]
        res = res.append(df)

    return res
    

def save(res, count):
    res.dropna(subset=["guid"])
    res.dropna(subset=["work title"])
    getfiles.save_to_csv(f"parse_guid_xl\\result\\work_guid{count}.csv", res, is_dataframe=True)
    

def main():
    k = getfiles.check_files(["СМГ Мессояха"])
    getfiles.save_to_csv("parse_guid_xl\\result\\files.csv", k)
    res = pd.DataFrame()
    filenumber = 0
    count = 0
    for file in k:
        df = read(file["path"])
        res = res.append(df)
        filenumber += 1
        if filenumber % 150 == 0:
            save(res, count)
            count += 1
    
