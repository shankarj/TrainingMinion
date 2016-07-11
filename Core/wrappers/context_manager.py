__author__ = 'shankar'

from Core.globals import service_global
from Core.utils import global_var_utils as gvu
from Core.enums.engine_mode import EngineMode


# Set the context of a given session variables
def set_network_context(user_id, network_id, training_profile_id, verbose, actual_session_id):
    from Core.utils import output_util as out
    needs_training = False

    if training_profile_id:
        needs_training = True

    # Create the context dict to be persisted.
    network_context = {
        "verbose": verbose,
        "user_id": user_id,
        "network_id": network_id,
        "training_profile_id": training_profile_id,
        "needs_training": needs_training
    }

    method_success = out.persist_context_props(actual_session_id, network_context)
    gvu.load_context_props(actual_session_id)
    return method_success


def get_training_profile_id(session_id):
    return service_global.running_sessions[session_id]["context_props"]["training_profile_id"]


def is_verbose_mode(session_id):
    return service_global.running_sessions[session_id]["context_props"]["verbose"]


def set_verbose_mode(session_id):
    service_global.running_sessions[session_id]["context_props"]["verbose"] = True


def unset_verbose_mode(session_id):
    service_global.running_sessions[session_id]["context_props"]["verbose"] = False


def is_network_initialized(session_id):
    return service_global.running_sessions[session_id]["context_props"]["init_done"]


def set_network_initialized(session_id):
    service_global.running_sessions[session_id]["context_props"]["init_done"] = True


def set_network_deinitialized(session_id):
    service_global.running_sessions[session_id]["context_props"]["init_done"] = False


def is_training_done(session_id):
    return service_global.running_sessions[session_id]["context_props"]["training_done"]


def set_training_done(session_id):
    service_global.running_sessions[session_id]["context_props"]["training_done"] = True


def set_training_not_done(session_id):
    service_global.running_sessions[session_id]["context_props"]["training_done"] = False


def pause_engine(session_id):
    service_global.running_sessions[session_id]["context_props"]["engine_mode"] = EngineMode.paused.name


def is_engine_paused(session_id):
    if service_global.running_sessions[session_id]["context_props"]["engine_mode"] == EngineMode.paused.name:
        return True
    else:
        return False


def set_engine_executing(session_id):
    service_global.running_sessions[session_id]["context_props"]["engine_mode"] = EngineMode.executing.name


def set_engine_training(session_id):
    service_global.running_sessions[session_id]["context_props"]["engine_mode"] = EngineMode.training.name


def set_engine_init(session_id):
    service_global.running_sessions[session_id] = {}
    service_global.running_sessions[session_id]["context_props"] = {}
    service_global.running_sessions[session_id]["network_structure"] = {}
    service_global.running_sessions[session_id]["network_conns"] = {}
    service_global.running_sessions[session_id]["training_profile"] = {}
    service_global.running_sessions[session_id]["training_data"] = {}
    service_global.running_sessions[session_id]["context_props"]["engine_mode"] = EngineMode.init.name


def set_engine_stopped(session_id):
    service_global.running_sessions[session_id]["context_props"]["engine_mode"] = EngineMode.stopped.name


def is_engine_training(session_id):
    if service_global.running_sessions[session_id]["context_props"]["engine_mode"] == EngineMode.training.name:
        return True
    else:
        return False


def is_engine_executing(session_id):
    if service_global.running_sessions[session_id]["context_props"]["engine_mode"] == EngineMode.executing.name:
        return True
    else:
        return False


def is_engine_stopped(session_id):
    if service_global.running_sessions[session_id]["context_props"]["engine_mode"] == EngineMode.idle.name:
        return True
    else:
        return False


def needs_training(session_id):
    return service_global.running_sessions[session_id]["context_props"]["needs_training"]
