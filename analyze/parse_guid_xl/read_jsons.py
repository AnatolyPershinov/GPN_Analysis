# обновляет имеющиеся json файлы с результатами. для каждой работы добавляет guid


import getfiles

jsons = getfiles.check_files(["СМГ Мессояха"], name=".json")
getfiles.save_to_csv(filename="parse_guid_xl\\results\\jsons.csv")

