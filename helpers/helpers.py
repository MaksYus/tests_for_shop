# тут лежат вспомогательные ф-ции
import os
import pytest
import csv
import json


def get_settings():
    settings_config = {}
    spis = os.environ
    for key, value in spis.items():
        settings_config[key] = value
    return settings_config


def get_fixtures():
    files_list = []
    for root, dirs, files in (os.walk("./fixtures")):
        for file in files:
            if '.pyc' not in file:
                root_folder = root[root.find('fixtures'):].replace(
                    '\\', '.').replace('/', '.')
                file_name = file[:len(file) - 3]
                files_list.append(f'{root_folder}.{file_name}')
    if len(files_list) == 0:
        raise pytest.PytestWarning('Не поддерживаемый запуск')
    return files_list


def load_test_data_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_test_data_json():
    with open('test_data.json', 'r') as f:
        return json.load(f)
