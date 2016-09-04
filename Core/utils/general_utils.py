import base64
import os
import shutil
from Core.globals import service_global

# Break the input session id to get the needed session variables
def get_session_variables(session_id):
    from Core.utils import output_util as out
    try:
        decoded_string = base64.b64decode(session_id)

        split_string = decoded_string.decode('utf-8').split("!")

        if len(split_string) == 2:
            session_variables = {
                "user_id" : split_string[0],
                "network_id" : split_string[1],
            }
            return session_variables
        else:
            out.write_verbose_msg("engine", 2, "Session variables parse fail.")
            return None
    except Exception as ex:
        out.write_verbose_msg("engine", 2, "Session variables parse fail.")

# Convert String to bool
def get_bool_value(string_val):
    if string_val in ["true", "True"]:
        return True
    elif string_val in ["false", "False"]:
        return False
    else:
        raise Exception("Invalid string value to convert to bool")

# Create the session directory to store its variables.
def create_session_directory(session_id):
    directory_path = service_global.globals_path + "/" + session_id
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        os.makedirs(directory_path + "/data")

def delete_session_directory(session_id):
    directory_path = service_global.globals_path + "/" + session_id
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path, ignore_errors=True)
