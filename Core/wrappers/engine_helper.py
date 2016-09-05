from Core.globals import service_global
import Core.wrappers.elements_manager as em
from Core.wrappers import ns_wrapper as ns
import Core.wrappers.training_helper as th
from Core.wrappers import context_manager as cm
from Core.utils import network_util as nu
from Core.enums.network_call_type import NetworkCallType
from Core.utils import general_utils as gu
import copy

# Sets the needed context variables for the engine.
def set_network_context(session_id):
    method_success = False

    # Break the session id to get the variables : uid, nid, prof_id, verbose.
    session_vars = gu.get_session_variables(session_id)
    context_vars = nu.network_call(NetworkCallType.get_network_context)

    if context_vars:
        context_set = cm.set_network_context(session_vars["user_id"], session_vars["network_id"], session_vars["snap_id"], context_vars["training_profile_id"], context_vars["verbose"], session_id)

        if context_set:
            method_success = True
            service_global.running_sessions[session_id]["endpoint"] = "sample_endpoint"

    return method_success

def set_engine_id(id):
    service_global.my_id = id

def get_engine_id():
    return service_global.my_id

# Get the engine mode
def get_engine_mode(session_id):
    return service_global.running_sessions[session_id]["context_props"]["engine_mode"]

# Get the status endpoint for the session id.
def get_endpoint(session_id):
    return service_global.running_sessions[session_id]["endpoint"]

# Get a list of running sessions in engine
def get_running_sessions():
    sessions_list = []
    for key in service_global.running_sessions.keys():
        sessions_list.append(key)

    return sessions_list

# Assigns from the input data, the data for each of the input element.
def set_input_elem_data(session_id, inp_data):
    set_success = False

    from Core.utils import output_util as out
    input_dataset_elems = ns.get_input_elem_list(session_id)

    if not len(input_dataset_elems) < 1:
        loop_success = True
        for elem in input_dataset_elems:
            elem_data = inp_data[elem]

            if elem_data:
                elem_obj = em.get_elem_obj(session_id, elem)
                elem_obj.props["curr_data"] = elem_data
            else:
                out.write_verbose_msg("engine", 2, "Can't find the input data for the input element : " + elem)
                loop_success = False
                break

    if loop_success:
        set_success = True

    return set_success


# Returns the output of current run.
def get_output_data(session_id):
    # Get all the elements connected to output element
    out_elems = ns.get_input_elements_in_direction(session_id, "_out", "forward")

    output_json = {}
    for elem in out_elems:
        # Get all the properties connected to _out from these elements
        prop_names = ns.get_prop_map_in_direction(session_id, elem, "_out", "forward")

        # Get all of those properties' values.
        for prop in prop_names:
            output_json[prop + "-" + elem] = em.get_prop_val(session_id, elem, prop)

    # Send it the output utils to be sent
    return output_json

# -------- Important routine ------------------------------------------------
# Creates PyObject for all the elements in service_global.py (given structure).
# Initializes the values as needed.
# ---------------------------------------------------------------------------
def create_init_network(session_id):
    from Core.utils import output_util as out
    method_success = False

    # Get all elements from service_global still stored as JSON.
    try:
        elem_list = ns.get_elems_id_list(session_id)
        all_success = True

        # Initialize elem object dictionary for the session
        service_global.elements_obj_dict[session_id] = {}

        # For each element in JSON, create the PyObject and initialize it
        # with static values as well.
        for elem_id in elem_list:
            elem_type = ns.get_elem_type(session_id, elem_id)

            # Do not create the property elements here. When an element's properties are initialized,
            # the corresponding property elements will be created.
            if elem_type.split("_")[0] == "prop":
                continue

            # Create the element represented as PyObjects.
            create_status = em.create_elem_obj(session_id, elem_id, elem_type)

            if create_status:
                # Get the object created in previous step
                elem_obj = em.get_elem_obj(session_id, elem_id)

                # # Create all the properties for the current element
                # prop_dict = ns.get_all_props(session_id, elem)
                # for prop in prop_dict:
                #     elem_obj.props[prop] = {}

                # Initialize for this element any static values if present. Also
                # create any property elements as well.
                prop_init_dict = ns.get_all_props_inits(session_id, elem_id)
                for prop in prop_init_dict:
                    if not prop_init_dict[prop] == None:
                        prop_val = prop_init_dict[prop]
                        if isinstance(prop_val, str) and prop_val.split(":")[0] == "prop_elem":
                            # This means that the current property has a property element
                            # associated with it. Let us create that element and assign it.
                            try:
                                prop_elem_id = prop_val.split(":")[1]
                                elem_type = ns.get_elem_type(session_id, prop_elem_id)
                                prop_create_status = em.create_elem_obj(session_id, prop_elem_id, elem_type)

                                if prop_create_status:
                                    prop_elem_obj = em.get_elem_obj(session_id, prop_elem_id)
                                    prop_elem_obj.props["_session_id"] = session_id
                                    prop_elem_obj.props["_session_path"] = service_global.globals_path
                                    elem_obj.props[prop] = prop_elem_obj
                                else:
                                    all_success = False
                                    break
                            except Exception as e:
                                out.write_verbose_msg(session_id, "engine", 2,
                                                      "Error while creating property element for : " + elem_id + ". Error : " + str(
                                                          e))
                                all_success = False
                                break
                        else:
                            elem_obj.props[prop] = prop_init_dict[prop]

                if all_success:
                    # Run the element's init method after setting default context variables
                    elem_obj.props["_session_id"] = session_id
                    elem_obj.props["_session_path"] = service_global.globals_path

                    # Call the element's init ( only if it's not a property element. This
                    # is checked in the beginning itself)
                    if not elem_obj.init_element():
                        out.write_verbose_msg(session_id, "engine", 2, "Error while element initialization : " + str(e))
                        all_success = False
                        break
            else:
                all_success = False
                break

        if all_success:
            method_success = True
    except Exception as e:
        out.write_verbose_msg(session_id, "engine", 2, "Error while initialization : " + str(e))

    return method_success


def execute_forward_pass(session_id, inp_data):
    from Core.utils import output_util as out
    pass_success = False
    th.set_forward_direction(session_id)

    # Set training direction.
    data_success = True
    if cm.is_engine_training(session_id):
        # Get the next training data for all the input elements.
        data_success = th.update_training_counters(session_id)
    elif cm.is_engine_executing(session_id):
        data_success = set_input_elem_data(session_id, inp_data)

    # Call the recursive forward pass utility starting from _out
    if data_success:
        # We start from output element and recursively execute forward pass
        try:
            recursive_forward_pass(session_id, "_out", None)
            get_output_data(session_id)
            pass_success = True
        except Exception as e:
            out.write_verbose_msg(session_id, "engine", 2, "Forward pass failed.")
    else:
        out.write_verbose_msg(session_id, "engine", 2,
                              "Exiting because input data is not valid for executing forward pass.")

    # Deactivating all the elements after the forward pass is done.
    em.deactivate_all_elements(session_id)

    return pass_success


def recursive_forward_pass(session_id, source_elem_id, dest_elem_id):
    # Base case being input element or an element already
    # activated.
    input_elems = ns.get_input_elem_list(session_id)
    if not source_elem_id == "_out" and em.is_elem_activated(session_id, source_elem_id):
        return em.get_conn_prop_values(session_id, source_elem_id, dest_elem_id, "forward", True)
    else:
        # Get all elems connected to new source
        new_dest_elem_id = source_elem_id
        connected_elems = ns.get_input_elements_in_direction(session_id, new_dest_elem_id, "forward")
        forward_input_args = {}

        # We recursively call the current element's dependents to get its
        # input arguments.
        for elem_id in connected_elems:
            # Recursive call to forward pass with new pair of source and dest
            curr_args = recursive_forward_pass(session_id, elem_id, new_dest_elem_id)
            for arg in curr_args:
                if arg not in forward_input_args:
                    forward_input_args[arg] = copy.copy(curr_args[arg])
                else:
                    forward_input_args[arg].extend(copy.copy(curr_args[arg]))

        # Run forward pass in training if the current element is not '_out'
        if source_elem_id is "_out":
            return forward_input_args
        else:
            # Set the prop value for current element from complete args
            # and call the forward pass
            curr_elem_obj = em.get_elem_obj(session_id, source_elem_id)
            for prop_name in forward_input_args:
                curr_elem_obj.props[prop_name] = forward_input_args[prop_name]

            # Call training forward pass or execute depending on mode.
            pass_success = False
            if cm.is_engine_training(session_id):
                pass_success = curr_elem_obj.train_forward_pass()
            elif cm.is_engine_executing(session_id):
                pass_success = curr_elem_obj.execute()

            if pass_success:
                # Activate this element
                em.activate_element(session_id, source_elem_id)

                # Write the dest elem's prop to the main JSON
                if cm.is_engine_training(session_id):
                    em.write_props_to_structure(session_id, source_elem_id)

                # Return the property values of the current element to it's destination
                return em.get_conn_prop_values(session_id, source_elem_id, dest_elem_id, "forward", True)
            else:
                raise Exception("Forward pass fail")


def execute_backward_pass(session_id):
    from Core.utils import output_util as out
    pass_success = False

    # Set training direction.
    if cm.is_engine_training(session_id):
        th.set_backward_direction(session_id)

    # Call the backward pass utility starting for each element other than props.
    try:
        for elem in ns.get_elems_id_list(session_id):
            elem_obj = em.get_elem_obj(session_id, elem)
            if elem_obj.props["_type"] == "element":
                pass_success = elem_obj.train_backward_pass()
                if not pass_success:
                    out.write_verbose_msg("engine", 2, "Backward pass failed for " + elem_obj.my_id)
                    break

        pass_success = True
    except Exception as e:
        out.write_verbose_msg("engine", 2, "Backward pass failed : " + e.message)

    # Deactivating all the elements after the backward pass is done.
    if cm.is_engine_training(session_id):
        em.deactivate_all_elements(session_id)

    return pass_success

def execute_backward_pass_old(session_id):
    from Core.utils import output_util as out
    pass_success = False

    # Set training direction.
    if cm.is_engine_training(session_id):
        th.set_backward_direction(session_id)

    # Call the recursive backward pass utility starting from each input element.
    try:
        for elem in ns.get_input_elem_list(session_id):
            ns.get_elems_id_list()
            recursive_backward_pass(session_id, None, elem)

        pass_success = True
    except Exception as e:
        out.write_verbose_msg("engine", 2, "Backward pass failed : " + e.message)

    # Deactivating all the elements after the backward pass is done.
    if cm.is_engine_training(session_id):
        em.deactivate_all_elements(session_id)

    return pass_success


def recursive_backward_pass(session_id, dest_elem_id, source_elem_id):
    from Core.utils import output_util as out

    # Base case being input element or an element already
    # activated.
    input_elems = ns.get_input_elem_list(session_id)
    if source_elem_id == "_out" or em.is_elem_activated(session_id, source_elem_id):
        return em.get_conn_prop_values(session_id, source_elem_id, dest_elem_id, "backward", True)
    else:
        # Get all elems connected to dest.
        new_dest_elem_id = source_elem_id
        connected_elems = ns.get_input_elements_in_direction(session_id, new_dest_elem_id, "backward")
        backward_input_args = {}

        for elem_id in connected_elems:
            # Recursive call to backward pass with new pair of source and dest
            curr_args = recursive_backward_pass(session_id, new_dest_elem_id, elem_id)
            for arg in curr_args:
                if arg not in backward_input_args:
                    backward_input_args[arg] = copy.copy(curr_args[arg])
                else:
                    backward_input_args[arg].extend(copy.copy(curr_args[arg]))

        # Run backward pass in training if the current element is not _in
        if source_elem_id not in input_elems:
            # Set the prop value for current element from complete args
            # and call the forward pass
            curr_elem_obj = em.get_elem_obj(session_id, source_elem_id)
            for prop_name in backward_input_args:
                curr_elem_obj.props[prop_name] = backward_input_args[prop_name]

            curr_elem_obj.train_backward_pass()

            # Write the dest elem's prop to the main JSON
            em.write_props_to_structure(session_id, source_elem_id)

            # Return the property values of the current element to it's destination
            return em.get_conn_prop_values(session_id, source_elem_id, dest_elem_id, "backward", True)

        # Activate this element
        em.activate_element(session_id, source_elem_id)
