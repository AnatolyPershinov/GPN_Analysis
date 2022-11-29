import os
import csv
import sys

a = os.path.basename(__file__)

__ROOT__ = os.path.abspath(__file__).replace(a, '')
print(__ROOT__)

def check_files(groups, name=".xl"):
    """проходит по всей директории. ищет файлы"""
    folders = [__ROOT__ + d for d in groups]
    filelist = []
    for directory in folders:
        for root, _, files in os.walk(directory):
            if "venv" in root or "__pycache__" in root or "check" in root:
                continue
            for file in files:
                if os.stat(f"{root}\\{file}").st_size <= 1000:
                    continue
                if name in file:
                    filelist.append({
                        "group": directory.split("\\")[-1],
                        "path": f"{root}\\{file}",
                    })
    return filelist


def save_to_csv(filename: str, array: list[dict], is_dataframe=None):
    """запись данных в csv"""
    filename = __ROOT__ + filename
    if is_dataframe:
        array.to_csv(filename, sep=";", index=False)
    else:
        with open(
            f'{filename}',
            "w", encoding="UTF-8",
            newline='\r\n'
        ) as csvfile:

            header = array[0].keys()
            writer = csv.DictWriter(f=csvfile, fieldnames=header, lineterminator="\n", delimiter=";")
            writer.writeheader()

            for k in array:
                writer.writerow(k)

