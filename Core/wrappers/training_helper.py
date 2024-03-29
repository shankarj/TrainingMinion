from Core.globals import service_global
import Core.wrappers.elements_manager as em
from Core.utils import network_util as nu
from Core.wrappers import ns_wrapper as ns
from Core.enums.network_call_type import NetworkCallType
from Core.wrappers import context_manager as cm

# Remove the given session id from the list of running training session ids
def get_training_sessions():
    return service_global.training_sessions


# Remove the given session id from the list of running training session ids
def set_post_training(session_id, training_success):
    if session_id in service_global.training_sessions:
        service_global.training_sessions.remove(session_id)

    network_structure = "none"
    network_conns = "none"
    parent_id = cm.get_network_id(session_id) if cm.get_snap_id(session_id) == "none" else cm.get_snap_id(session_id)
    create_new = False

    if training_success:
        network_structure = ns.get_network_structure(session_id)
        network_conns = ns.get_network_conns(session_id)

        if cm.get_training_profile_id(session_id) != "none":
            create_new = True

    # Notify leader of completion
    nu.network_call(NetworkCallType.notify_training_done, sess_id=session_id, parent_id=parent_id,
                    project_name=cm.get_project_name(session_id), structure=network_structure, conns=network_conns,
                    create_new_snapshot=create_new, training_result=training_success)


# Add the given session id to the list of running training session ids
def add_to_training_sessions(session_id):
    service_global.training_sessions.append(session_id)


# Increments curr_row, curr_batch's size and clears
# counter on reaching dataset end (epoch done).
def update_training_counters(session_id):
    from Core.utils import output_util as out

    load_success = False

    # Get the curr_training_row data and the expected values from each
    # of the input dataset as given during designing.
    input_dataset_elems = ns.get_input_elem_list(session_id)

    if input_dataset_elems and not len(input_dataset_elems) < 1:
        all_success = True
        for elem in input_dataset_elems:
            elem_obj = em.get_elem_obj(session_id, elem)

            if elem_obj:
                curr_index = service_global.running_sessions[session_id]["context_props"]["curr_training_row"]
                elem_obj.props["curr_row_index"] = curr_index
            else:
                out.write_verbose_msg("engine", 2, "No such element found in PyObj list : " + elem)
                all_success = False
                break

        if all_success:
            # Increment batch and epochs accordingly
            service_global.running_sessions[session_id]["context_props"]["curr_batch_size"] += 1
            service_global.running_sessions[session_id]["context_props"]["curr_training_row"] += 1

            if service_global.running_sessions[session_id]["context_props"]["curr_training_row"] == \
                    service_global.running_sessions[session_id]["training_profile"]["dataset_size"]:
                service_global.running_sessions[session_id]["context_props"]["curr_training_row"] = 0
                increment_epoch(session_id)

            load_success = True

    return load_success


# Checks if current batch is full. If True, clears it as well.
def is_batch_full(session_id):
    if service_global.running_sessions[session_id]["context_props"]["curr_batch_size"] == \
            service_global.running_sessions[session_id]["training_profile"]["batch_size"]:
        service_global.running_sessions[session_id]["context_props"]["curr_batch_size"] = 0
        return True

    return False


def all_epochs_done(session_id):
    if service_global.running_sessions[session_id]["context_props"]["curr_epoch"] >= \
            service_global.running_sessions[session_id]["training_profile"]["epochs"]:
        service_global.running_sessions[session_id]["context_props"]["curr_epoch"] = 0
        return True
    else:
        return False


def increment_epoch(session_id):
    service_global.running_sessions[session_id]["context_props"]["curr_epoch"] += 1


def set_forward_direction(session_id):
    service_global.running_sessions[session_id]["context_props"]["training_direction"] = "forward"


def set_backward_direction(session_id):
    service_global.running_sessions[session_id]["context_props"]["training_direction"] = "backward"


def change_train_direction(session_id):
    if service_global.running_sessions[session_id]["context_props"]["training_direction"] == "forward":
        service_global.running_sessions[session_id]["context_props"]["training_direction"] = "backward"
    else:
        service_global.running_sessions[session_id]["context_props"]["training_direction"] = "forward"
