import pytest

import os

def get_fixtures():
    files_list = []
    for root, dirs,files in (os.walk("./fixtures")):
        for file in files:
            if '.pyc' not in file:
                root_folder = root[root.find('fixtures'):].replace('\\','.').replace('/','.')
                file_name = file[:len(file) -3]
                files_list.append(f'{root_folder}.{file_name}')
    if len(files_list) == 0:
        raise pytest.PytestWarning('Не поддерживаемый запуск')
    return files_list

pytest_plugins = get_fixtures()

print(os.environ["DATABASE_URL"])
