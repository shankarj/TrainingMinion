__author__ = 'shankar'

import json
import os
from Core.utils import json_util as ju
from Core.wrappers import context_manager as cm
from Core.globals import service_global
from Core.enums.engine_mode import EngineMode


# Writes all the verbose messages onto console or to sockets as needed.
def write_verbose_msg(session_id, source, type, msg):
    if source == "engine":
        if type == 100:
            print(str(type) + " : " + msg)
        else:
            if cm.is_verbose_mode(session_id):
                print(str(type) + " : " + msg)
    elif source == "element":
        if cm.is_verbose_mode(session_id):
            print(str(type) + " : " + msg)
    else:
        print("Invalid source of logging.")


def send_output(output_json):
    # Check for the necessary way to send the output.
    # We can also edit as needed here.
    # For now let us print it on the console.
    # We can also return the JSON to be returned back to the client.
    print(output_json)
    return True


# Writes the given network structure to the global json file.
# Used during execution/training time as well to write the updated
# network structure. Hence the need for injection via parameter.
def persist_network_structure(session_id, network_structure):
    persist_success = False
    try:
        file_path = service_global.globals_path + "/" + session_id + "/network.json"
        old_network_dict = {}

        if os.path.isfile(file_path):
            network_file = open(file_path)
            network_file_content = network_file.read()
            old_network_dict = ju.json_to_dict(network_file_content)
            network_file.close()

        old_network_dict["network_structure"] = network_structure

        network_file = open(file_path, "w+")
        network_file.write(json.dumps(old_network_dict))
        network_file.close()
        persist_success = True
    except Exception as ex:
        write_verbose_msg("Failed to update network structure : " + ex)

    return persist_success


# Writes the given network structure to the global json file.
def persist_network_conns(session_id, network_conns):
    persist_success = False
    try:
        file_path = service_global.globals_path + "/" + session_id + "/network.json"
        old_network_dict = {}

        if os.path.isfile(file_path):
            network_file = open(file_path)
            network_file_content = network_file.read()
            old_network_dict = ju.json_to_dict(network_file_content)
            network_file.close()

        old_network_dict["network_conns"] = network_conns

        network_file = open(file_path, "w+")
        network_file.write(json.dumps(old_network_dict))
        network_file.close()
        persist_success = True
    except Exception as ex:
        write_verbose_msg("Failed to update network conns : " + ex.message)
    return persist_success


def persist_training_profile(session_id, training_profile):
    persist_success = False
    try:
        file_path = service_global.globals_path + "/" + session_id + "/training.json"
        old_training_data = {}

        if os.path.isfile(file_path):
            training_data_file = open(file_path)
            file_content = training_data_file.read()
            old_training_data = ju.json_to_dict(file_content)
            training_data_file.close()

        old_training_data["training_profile"] = training_profile

        training_data_file = open(file_path, "w+")
        training_data_file.write(json.dumps(old_training_data))
        training_data_file.close()
        persist_success = True
    except Exception as ex:
        write_verbose_msg("Failed to update training json file : " + ex.message)

    return persist_success


def persist_training_data(session_id, tdset_id, data, prop):
    persist_success = False
    try:
        # First let us store the properties of the input training data file.
        file_path = service_global.globals_path + "/" + session_id + "/training.json"
        old_training_data = {}

        if os.path.isfile(file_path):
            training_prop_file = open(file_path)
            file_content = training_prop_file.read()
            old_training_data = ju.json_to_dict(file_content)
            training_prop_file.close()

        if "training_data" not in old_training_data:
            old_training_data["training_data"] = {}

        old_training_data["training_data"][tdset_id] = {}
        old_training_data["training_data"][tdset_id]["prop"] = prop

        training_prop_file = open(file_path, "w+")
        training_prop_file.write(json.dumps(old_training_data))
        training_prop_file.close()

        # Now store the actual dump of data file itself.
        file_path = service_global.globals_path + "/" + session_id + "/data/" + tdset_id + "." + prop["type"]
        data_file = open(file_path, "w+")
        data_file.write(data)
        data_file.close()

        persist_success = True
    except Exception as ex:
        write_verbose_msg("Failed to update training json file : " + ex.message)

    return persist_success


def persist_context_props(session_id, network_context):
    persist_success = False
    try:
        file_path = service_global.globals_path + "/" + session_id + "/context.json"
        old_context_props = {}

        if os.path.isfile(file_path):
            context_props_file = open(file_path)
            context_props_file_content = context_props_file.read()
            old_context_props = ju.json_to_dict(context_props_file_content)
            context_props_file.close()
        else:
            old_context_props["training_direction"] = ""
            old_context_props["engine_mode"] = EngineMode.stopped.name
            old_context_props["init_done"] = False
            old_context_props["training_done"] = False
            old_context_props["curr_batch_size"] = 0
            old_context_props["curr_epoch"] = 0
            old_context_props["curr_training_row"] = 0

        old_context_props["network_id"] = network_context["network_id"]
        old_context_props["training_profile_id"] = network_context["training_profile_id"]
        old_context_props["verbose"] = network_context["verbose"]

        context_props_file = open(file_path, "w+")
        context_props_file.write(json.dumps(old_context_props))
        context_props_file.close()

        persist_success = True
    except Exception as ex:
        write_verbose_msg("Failed to update context properties : " + ex.message)

    return persist_success
