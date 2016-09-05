from Core.globals import service_global
from Core.utils import general_utils as gu
from Core.wrappers import context_manager as cm


# Hard reset for the given session id if already present
def delete_session(session_id):
    if session_id in service_global.running_sessions:
        del service_global.running_sessions[session_id]

    if session_id in service_global.training_sessions:
        service_global.training_sessions.remove(session_id)

    gu.delete_session_directory(session_id)

    # Also notify the leader that this session is deleted. Very important.

def session_exists(session_id):
    if session_id in service_global.running_sessions:
        return True
    else:
        return  False

def create_session(session_id):
    from Core.utils import output_util as out

    method_success = False

    try:
        if session_id is not None:
            gu.create_session_directory(session_id)

            service_global.running_sessions[session_id] = {}
            service_global.running_sessions[session_id]["context_props"] = {}
            service_global.running_sessions[session_id]["network_structure"] = {}
            service_global.running_sessions[session_id]["network_conns"] = {}
            service_global.running_sessions[session_id]["training_profile"] = {}
            service_global.running_sessions[session_id]["training_data"] = {}

            method_success = True

    except Exception as ex:
        out.write_verbose_msg(session_id, "engine", 2, "Session create failed. " + str(ex))

    return method_success