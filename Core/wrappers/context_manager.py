__author__ = 'shankar'

from Core.globals import service_global
from Core.utils import global_var_utils as gvu
from Core.enums.engine_mode import EngineMode


# Set the context of a given session variables
def set_network_context(session_id, session_vars, settings_vars):
    from Core.utils import output_util as out

    method_success = False

    try:
        # Create the context dict to be persisted.
        network_context = {
            "project_name": settings_vars["project_name"],
            "verbose": settings_vars["settings_json"]["verbose"],
            "training_profile_id": settings_vars["settings_json"]["training_profile_id"],
            "user_id": session_vars["user_id"],
            "network_id": session_vars["network_id"],
            "snap_id": session_vars["snap_id"]
        }

        method_success = out.persist_context_props(session_id, network_context)
        gvu.load_context_props(session_id)
    except Exception as ex:
        out.write_verbose_msg("engine", 100, "Error setting context variables.")

    return method_success


def get_network_id(session_id):
    return service_global.running_sessions[session_id]["context_props"]["network_id"]


def get_training_profile_id(session_id):
    return service_global.running_sessions[session_id]["context_props"]["training_profile_id"]


def get_project_name(session_id):
    return service_global.running_sessions[session_id]["context_props"]["project_name"]

def get_snap_id(session_id):
    return service_global.running_sessions[session_id]["context_props"]["snap_id"]


def is_verbose_mode(session_id):
    return service_global.running_sessions[session_id]["context_props"]["verbose"]


def set_verbose_mode(session_id):
    service_global.running_sessions[session_id]["context_props"]["verbose"] = True


def unset_verbose_mode(session_id):
    service_global.running_sessions[session_id]["context_props"]["verbose"] = False


def is_network_initialized(session_id):
    if session_id in service_global.running_sessions:
        return service_global.running_sessions[session_id]["context_props"]["init_done"]
    else:
        return False


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
    if service_global.running_sessions[session_id]["context_props"]["engine_mode"] == EngineMode.stopped.name:
        return True
    else:
        return False


def get_engine_mode(session_id):
    return service_global.running_sessions[session_id]["context_props"]["engine_mode"]


def needs_training(session_id):
    if service_global.running_sessions[session_id]["context_props"]["training_profile_id"] != "none":
        return True
    else:
        return False
