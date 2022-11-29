from pathlib import Path
import sys
import json

print(sys.path.insert(0, str(Path(__file__).parent.parent.parent)))

from analyze import getfiles
    




def work_handle(work):
    d = {
    "group": work["upper works"][-1],
    "upper_works": work["upper works"][:-1],
    "guid": work["guid"],
    "title": work["work title"],
    "work_id": work["work id"],
    "work_object": work["upper works"][-1],
    "amount": work["amount"],
    "measurements": work["measurements"],
    "xlfilename": work["xlfile_name"],
    "jsonfilename": work["json_path"],
    "sum_fact": sum([list(p.values())[0]["fact"] for p in work["work_data"]["progress"]]),
    }
    if len(work["upper works"]) > 3:
        d["object"] = [work["upper works"][i] for i in [0, 1, 3]] 
    else:
        d["object"] = work["upper works"]

    return d

def is_right_work(work):
    guid = work["guid"]
    title = work["work title"]
    work_id = work["work id"]
    if guid == None or title == None or work_id == None:
        return False
    
    progress = work["work_data"]["progress"]
    prog_contain = [list(p.values())[0]["fact"] for p in progress]
    if sum(prog_contain) > 0:
        return True
    else: 
        return False

def json_handle(obj, path):
    # выбираем правильные работы из файла
    works = obj["work"]
    
    right_works = [w for w in works if is_right_work(w)] # работы, значение факта которых больше 0
    for k in right_works:
        k["xlfile_name"] = obj["file_name"]
        k["json_path"] = path
        
    return right_works
    
def main():
    right_works = [] # правильные работы
    files = getfiles.check_files(["\\jsons_analyze"], name=".json")
    
    # собираем правильные работы
    for row in files:
        path = row["path"]
        # print(path)
        with open(file=path, mode="r", encoding="UTF-8") as f:

            obj = json.load(f)
            right_works.extend(json_handle(obj, path.split("DATA")[-1]))
            
    result = []    
    for k in right_works:
        result.append(work_handle(k))
    # print(result)
    getfiles.save_to_csv("jsons_analyze\\results\\works.csv", result)
            
main()