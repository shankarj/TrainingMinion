__author__ = "Shankar"

from Core.globals import service_global
from Core.wrappers import ns_wrapper as ns
from Core.elements import elements_factory as ef
from Core.elements import abstract_property_element as ape
from Core.utils import output_util as out


def create_elem_obj(session_id, elem_id, elem_type):
    elem = ef.create_object(session_id, elem_id, elem_type)
    if elem is None:
        out.write_verbose_msg(session_id, "engine", 2, "Element not created : " + elem_id)
        return False
    else:
        elem.activated = False
        service_global.elements_obj_dict[session_id][elem_id] = elem
        return True


def get_elem_obj(session_id, elem_id):
    return service_global.elements_obj_dict[session_id][elem_id]


def get_prop_val(session_id, elem_id, prop_name):
    return service_global.elements_obj_dict[session_id][elem_id].props[prop_name]


def set_prop_val(session_id, elem_id, prop_name, prop_val):
    service_global.elements_obj_dict[session_id][elem_id].props[prop_name] = prop_val


# This routine writes the in memory representation of the individual
# elements' properties to its respective dictionary representation
# in service_global.py
def write_props_to_structure(session_id, elem_id):
    prop_val_map = get_elem_obj(session_id, elem_id).props

    if prop_val_map:
        for prop in prop_val_map:
            if isinstance(prop_val_map[prop], ape.AbstractPropertyElement):
                ns.set_prop_val(session_id, elem_id, prop, "")
            else:
                ns.set_prop_val(session_id, elem_id, prop, prop_val_map[prop])
    else:
        out.write_verbose_msg(session_id, "engine", 2,
                              "Element object not found in em to be written to output network.")

    network_structure = ns.get_network_structure(session_id)

    if network_structure:
        out.persist_network_structure(session_id, network_structure)
    else:
        out.write_verbose_msg(session_id, "engine", 2,
                              "Failed to write network structure. Empty structure from wrapper.")


# Checks if a given property name exists in the given element.
def is_prop_present(session_id, elem_id, prop_name):
    if prop_name in service_global.elements_obj_dict[session_id][elem_id].props.keys():
        return True

    return False


def is_elem_present(session_id, elem_id):
    if elem_id in service_global.elements_obj_dict[session_id]:
        return True

    return False


def is_elem_activated(session_id, elem_id):
    return service_global.elements_obj_dict[session_id][elem_id].activated


def activate_element(session_id, elem_id):
    service_global.elements_obj_dict[session_id][elem_id].activated = True


def deactivate_element(session_id, elem_id):
    service_global.elements_obj_dict[session_id][elem_id].activated = False


def deactivate_all_elements(session_id):
    for elem_id in service_global.elements_obj_dict[session_id]:
        deactivate_element(session_id, elem_id)


# Get values of properties in source element that are connected to
# given destination element in the given direction. You can choose to
# keep the key to be source property name or dest property name.
# Useful while changing the destination property value given a source
# property name in a connection.
def get_conn_prop_values(session_id, source_elem_id, dest_elem_id, direction, give_dest_keys):
    args = {}

    # Return empty args if the current element is _out while backtracking.
    if direction == "backward":
        if source_elem_id == "_out":
            return args

    # Get all source property names connected to dest elem.
    needed_key = ""
    if give_dest_keys:
        needed_key = "dest"
    else:
        needed_key = "source"

    prop_names = ns.get_prop_map_in_direction(session_id, source_elem_id, dest_elem_id, direction)
    if not prop_names:
        out.write_verbose_msg(session_id, "engine", 2,
                              "No property connections between " + source_elem_id + " and " + dest_elem_id)
        return args

    # Get all the dest props for which source elem is connected to
    # and assign its value from source elem props.
    for prop in prop_names:
        if is_prop_present(session_id, source_elem_id, prop):
            args[prop_names[prop]] = get_prop_val(session_id, source_elem_id, prop)
        else:
            out.write_verbose_msg(session_id, "engine", 2, "Skipping for property " + prop + " in " + source_elem_id)

    return args
