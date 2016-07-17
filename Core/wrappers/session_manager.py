from Core.globals import service_global
from Core.utils import general_utils as gu
from Core.wrappers import context_manager as cm


def create_session(session_id):
    from Core.utils import output_util as out
    method_success = False

    try:
        # Break the session id to get the variables : uid, nid, prof_id, verbose.
        session_vars = gu.get_session_variables(session_id)
        if session_vars is not None:
            gu.create_session_directory(session_id)
            context_set = cm.set_network_context(session_vars["user_id"], session_vars["network_id"], session_vars["training_profile_id"], session_vars["verbose"], session_id)

            if context_set:
                method_success = True
                service_global.running_sessions[session_id]["endpoint"] = "sample_endpoint"
    except Exception as ex:
        out.write_verbose_msg(session_id, "engine", 2, "Session create failed. " + str(ex))

    return method_success