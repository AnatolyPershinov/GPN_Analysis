'''
Метод заполняет requirements.txt
Заполняет exceptions.csv
'''


import os
import csv



def check_files(groups):
    """проходит по всей директории. ищет xl файлы"""
    folders = [os.getcwd() + "\\DATA" + d for d in groups]

    filelist = []
    for directory in folders:
        for root, _, files in os.walk(directory):
            if "venv" in root or "__pycache__" in root or "check" in root:
                continue
            for file in files:
                if os.stat(f"{root}\\{file}").st_size <= 1000:
                    continue
                if ".xl" in file:
                    filelist.append({
                        "group": directory.split("\\")[-1],
                        "path": f"{root}\\{file}",
                    })
    return filelist



def save_to_csv(filename, array):
    """запись данных в csv"""
    with open(
        f'{filename}',
        "w", encoding="UTF-8",
        newline='\r\n'
    ) as csvfile:

        header = array[0].keys()
        writer = csv.DictWriter(f=csvfile, fieldnames=header, lineterminator="\n", delimiter="\t")
        writer.writeheader()

        for k in array:
            writer.writerow(k)



