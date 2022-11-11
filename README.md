# Парсеры МСГ

## Описание репозитория:
- Полный репозиторий со всеми данными располжен ```\\10.9.14.41\share\GPN_KIP\GPN_Data```
- Для каждого месторождения создана своя директория со всей информацией по месторождению
- В каждой директории есть данные, парсеры и результаты парсеров
- В каждой директории свой requirements.txt необходимый для запуска парсера
- Если парсер выполнен в формате ipynb - к нему прилагается его аналог в формате py

## Результаты парсинга:
https://docs.google.com/spreadsheets/d/11YSqVGaLmcarCkn8bFotQqUFthASLNQQl9qMz3krs08/edit#gid=0

## Схема json 
Единая для всех парсеров и всех месторождения
```
{
    "file_name": "str",
    "work": [{
        "work title": "str",
        "work id": "str",
        "upper works": ["str"],
        "measurements": "str",
        "amount": "int",
        "work_data": {
            "start_date": {
                "plan": "float",
                "estimate": "float",
                "fact": "float"
            },
            "stop_date": {
                "plan": "float",
                "estimate": "float",
                "fact": "float"
            },
            "complite_state_perc": {
                "plan": "float",
                "fact": "float"
            },
            "complite_state_value": {
                "plan": "float",
                "fact": "float"
            },
            "current_remain_perc": "NoneType",
            "current_remain_value": "int",
            "whole_remain_perc": "float",
            "whole_remain_value": "float",
            "mounth_complite_value": {
                "plan": "float",
                "fact": "float"
            },
            "mounth_complite_perc": {
                "plan": "float",
                "fact": "float"
            },
            "progress": [
                {
                    "01.01.2017": {
                        "plan": "float",
                        "fact": "float"
                    }
                },
                {
                    "02.01.2017": {
                        "plan": "float",
                        "fact": "float"
                    }
                },
                ...
                {
                    "31.01.2017": {
                        "plan": "float",
                        "fact": "float"
                    }
                }
            ],
            "comments": "str"
        }
    }, 
    ...
    ]
    "resource": [{
        "resource_id": "int",
        "resource_name": "str",
        "type": "str",
        "progress": [
            {
                "1": "float"
            },
            {
                "2": "float"
            },
            ...
            {
                "31": "float"
            }
        ],
        "comments": "str"
    },
    ...
    ]
}
```

## Схема ядра в базе данных postgreSQL
![ER Diagram](/extra/kernel_psql.png)
