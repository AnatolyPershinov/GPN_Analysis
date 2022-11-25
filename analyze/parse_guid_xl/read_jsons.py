# обновляет имеющиеся json файлы с результатами. для каждой работы добавляет guid
from pathlib import Path
import sys
import json
import pandas as pd


print(sys.path.insert(0, str(Path(__file__).parent.parent.parent)))

from analyze import getfiles

def json_handle(js: dict):
    file = js["file_name"]
    works = js["work"]
    return file, works
    

def compare(data: pd.DataFrame, works: list):
    for work in works:

        df = data.loc[(data["work title"] == work["work title"]) & (data["work id"] == work["work id"])]
        if df.shape[0] > 1:
            df = df.drop_duplicates(subset="guid")
            if df.shape[0] > 1:
                df.to_csv("test.csv")
        guid = df["guid"].values
        work["guid"] = guid[0] if len(guid) > 0 else None
        
        


def main():
    row_files = getfiles.check_files(["СМГ Мессояха"], name=".json")
    df = pd.read_csv("parse_guid_xl\\result\\work_guid.csv", sep=";")
    df = df.dropna(subset=["guid"])
    df["short_name"] = df["file_name"].apply(lambda s: s.split("/")[-1])
    files = [k["path"] for k in row_files]

    for file in files:
        with open(file=file, mode="r", encoding="UTF-8") as f:
            obj = json.load(f)
            file_name, works = json_handle(obj)

        json_short_name = file_name.split("/")[-1]
        # print(json_short_name) 

        tmp = df.loc[df["short_name"] == json_short_name]
        if tmp.shape[0] == 0:
            continue

        # print(works)
        compare(tmp, works)
        path = "parse_guid_xl\\result\\jsons\\" + "_".join(file.split('\\')[-2:])
        with open(file=path, mode="w", encoding="UTF-8") as f:
            json.dump(obj=obj, fp=f, ensure_ascii=False)

main()
