__author__ = 'shankar'

import Core.utils.output_util as oa
from Core.wrappers import context_manager as cm
from Core.engine import exec_engine as engine
import Core.wrappers.engine_helper as engine_help


# ----------------
# Network routines
# ----------------
def initialize_network(session_id):
    return engine.init_engine(session_id)


def start_training(session_id):
    return engine.train_network(session_id)


def run_network(session_id, input_data):
    return engine.run_network(session_id, input_data)


def get_output(session_id):
    return engine_help.get_output_data(session_id)


# ----------------
# Additional routines
# ----------------
def update_training_profile():
    pass


def refresh_training_data():
    pass


# ----------------
# Config updates
# ----------------
def set_verbose(session_id, verbose):
    if isinstance(verbose, bool):
        if verbose:
            cm.set_verbose_mode(session_id)
        else:
            cm.unset_verbose_mode(session_id)
    else:
        oa.write_verbose_msg("Verbose input should be a bool.")


def reset_network(session_id):
    cm.set_network_deinitialized(session_id)


def get_socket_endpoint():
    pass


if __name__ == '__main__':
    user_id = "shankar"
    network_id = "n001"
    training_profile_id = "tr001"
    verbose = True
    session_id = user_id + "!" + network_id + "!" + training_profile_id + "!" + str(verbose)

    import base64

    encoded_session_id = base64.b64encode(bytes(session_id, "utf-8")).decode('ascii')

    init_success = initialize_network(encoded_session_id)

    sample_input = {"i001": ["i001"]}
    if init_success:
        import json
        start_training(encoded_session_id)
        print("Training done.");
        run_network(encoded_session_id, json.dumps(sample_input))
        print (get_output(encoded_session_id))
