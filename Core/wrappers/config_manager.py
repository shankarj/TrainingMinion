__author__ = 'shankar'

import json

config_json = None

def read_config_file():
    from Core.utils import output_util as out
    try:
        with open('./Core/config.json') as data_file:
            global config_json
            config_json = json.load(data_file)
            print (config_json)
    except Exception as ex:
        out.write_verbose_msg(session_id, "engine", 100, "Error while initializing config file : " + str(e))

def get_config_value(key):
    global config_json
    if key in config_json:
        return config_json[key]
    else:
        return None


if __name__ == "__main__":
    read_config_file()
    print(get_config_value("core_endpoint"))