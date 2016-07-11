from Core.globals import service_global
from Core.utils import json_util as ju

def load_context_props(session_id):
    from Core.utils import output_util as oa
    try:
        context_file = open(service_global.globals_path + "/" + session_id + "/context.json").read()
        service_global.running_sessions[session_id]["context_props"] = ju.json_to_dict(context_file)
        return True
    except Exception as ex:
        oa.write_verbose_msg("Error while loading context properties. " + str(ex))
        return False


def load_network_file(session_id):
    from Core.utils import output_util as oa
    try:
        network_file = open(service_global.globals_path + "/" + session_id + "/network.json").read()
        network_dict = ju.json_to_dict(network_file)
        service_global.running_sessions[session_id]["network_structure"] = network_dict["network_structure"]
        service_global.running_sessions[session_id]["network_conns"] = network_dict["network_conns"]
        return True
    except Exception as ex:
        oa.write_verbose_msg("Error while loading context properties. " + str(ex))
        return False


def load_training_file(session_id):
    from Core.utils import output_util as oa
    try:
        training_file = open(service_global.globals_path + "/" + session_id + "/training.json").read()
        training_dict = ju.json_to_dict(training_file)
        service_global.running_sessions[session_id]["training_profile"] = training_dict["training_profile"]
        service_global.running_sessions[session_id]["training_data"] = training_dict["training_data"]
    except Exception as ex:
        oa.write_verbose_msg("Error while loading training properties. " + str(ex))
