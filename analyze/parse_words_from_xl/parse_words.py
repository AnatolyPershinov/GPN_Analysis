
class Word:
    """класс отвечающий за обработку слов"""
    word: str
    groups: dict
    total_count: int
    
    def __init__(self, word, group):
        # класс инициализируется
        self.word = word
        self.total_count = 1
        self.groups = {
            "СМГ Зима": 0,
            "СМГ Мессояха": 0,
            "СМГ Н.Порт": 0,
            "Томский интегрированный проект": 0,
        }
                
        self.groups[group] = 1
        
    def increase(self, group):
        """нашлось совпадение по словам"""
        self.total_count += 1
        if self.groups.get(group, None) == None:
            self.groups[group] = 1
        else:
            self.groups[group] += 1
            
            
    def get_dict(self):
        """преобразовать в словарь"""
        res = {
            "word": self.word, 
            "total_count": self.total_count,
        }
        res.update(self.groups)
        
        return res
    

class Calc:
    """класс оработчик общего отчёта. хранит всё множество найденных слов"""
    def __init__(self):
        self.res = {}

    def handle_data(self, array, group):
        """считает слова во множестве"""
        for word in array:
            if self.res.get(word, None) == None:
                self.res[word] = Word(word=word, group=group)
            else:
                self.res[word].increase(group)
        
    def get_report(self):
        """возвращает список со словарями для каждого уникального слова"""
        return [v.get_dict() for v in self.res.values()]
