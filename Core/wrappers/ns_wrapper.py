from Core.enums.network_call_type import NetworkCallType as nctype
from Core.utils import network_util as nu
from Core.utils import output_util as out
from Core.utils import global_var_utils as gvu
from Core.globals import service_global
import copy


# Download the network structure and writes it to network.json.
# Also loads the network connection as well.
# Loads the network to memory from the json file.
def download_structure(session_id, network_id):
    method_success = False
    network_struct_full = nu.network_call(nctype.get_network_structure)

    if network_struct_full:
        network_structure = network_struct_full["network_structure"]
        network_conns = network_struct_full["network_conns"]

        if network_structure and network_conns:
            # Persist them on file.
            status_one = out.persist_network_structure(session_id, network_structure)
            status_two = out.persist_network_conns(session_id, network_conns)

            if status_one and status_two:
                # Load the structure and connections to memory.
                load_status = gvu.load_network_file(session_id)

                if load_status:
                    method_success = True

    return method_success


# Get the complete network structure
def get_network_structure(session_id):
    return service_global.running_sessions[session_id]["network_structure"]


# Get all property name, value of the given element
def get_all_props(session_id, elem_id):
    return service_global.running_sessions[session_id]["network_structure"][elem_id]["props"]


# Get a map of all properties and it's init value for a given element.
def get_all_props_inits(session_id, elem_id):
    return service_global.running_sessions[session_id]["network_structure"][elem_id]["init"]


def get_elem_type(session_id, elem_id):
    return service_global.running_sessions[session_id]["network_structure"][elem_id]["_type"]


# Gets the input elements in the network.
# Processes by it's name being input_*
def get_input_elem_list(session_id):
    input_elems = []

    for elem in get_elems_id_list(session_id):
        elem_type = service_global.running_sessions[session_id]["network_structure"][elem]["_type"]
        if elem_type.split('_')[1].lower() == "input":
            input_elems.append(elem)

    return input_elems


# Gets the ids of all the elements in the network.
def get_elems_id_list(session_id):
    return service_global.running_sessions[session_id]["network_structure"].keys()


# Return the connected elements to a given element in a given direction of pass.
# Ex. a->b; c->b. Then for b in forward : return [a, c]
def get_input_elements_in_direction(session_id, elem_id, direction):
    elems = []
    for i in range(0, len(service_global.running_sessions[session_id]["network_conns"])):
        conn_element = service_global.running_sessions[session_id]["network_conns"][i]
        if conn_element['direction'] == direction and conn_element['dest'] == elem_id:
            elems.append(conn_element['source'])
    return elems


# Gets the type of the given element id
def get_elem_type(session_id, elem_id):
    return service_global.running_sessions[session_id]["network_structure"][elem_id]["_type"]


def get_prop_val(session_id, elem_id, prop_name):
    return copy.deepcopy(service_global.running_sessions[session_id]["network_structure"][elem_id]["props"][prop_name])


def set_prop_val(session_id, elem_id, prop_name, prop_val):
    service_global.running_sessions[session_id]["network_structure"][elem_id]["props"][prop_name] = prop_val


# Gets all the property names in the source/dest element of a given connection
def get_prop_map_in_direction(session_id, source_elem_id, dest_elem_id, direction):
    prop_names = {}

    for conn in service_global.running_sessions[session_id]["network_conns"]:
        if conn["source"] == source_elem_id and conn["dest"] == dest_elem_id and conn["direction"] == direction:
            prop_names[conn["source_prop"]] = conn["dest_prop"]

    return prop_names
