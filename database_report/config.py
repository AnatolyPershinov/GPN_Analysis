import os

from configparser import ConfigParser


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
print(f'{ROOT_DIR}\database.ini')


def config(filename=f'{ROOT_DIR}\database.ini', section='postgres'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db