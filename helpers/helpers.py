# тут лежат вспомогательные ф-ции
import os

def get_settings():
    settings_config={}
    spis = os.environ
    for key, value in spis.items():
        settings_config[key] = value
    return settings_config