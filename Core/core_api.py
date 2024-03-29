__author__ = 'shankar'

import Core.utils.output_util as oa
from Core.wrappers import context_manager as cm
from Core.engine import exec_engine as engine
import Core.wrappers.engine_helper as engine_helper
import Core.wrappers.training_helper as training_helper
from Core.wrappers import session_manager as sm
import threading


# ----------------
# Network routines
# ----------------
def initialize_network(session_id):
    return engine.init_engine(session_id)

def start_training(session_id):
    if len(training_helper.get_training_sessions()) == 0:
        training_thread = threading.Thread(target=engine.train_network, args=(session_id,))
        training_thread.start()
        return True, "Training request has been initiated. Please connect to the socket endpoint for updates."
    else:
        return False, "Currently running a training session. Exiting."

def run_network(session_id, input_data):
    return engine.run_network(session_id, input_data)


def get_output(session_id):
    return engine_helper.get_output_data(session_id)


# ----------------
# Additional routines
# ----------------
def delete_session(session_id):
    return sm.delete_session(session_id)

def get_training_sessions():
    return training_helper.get_training_sessions()

def get_running_sessions():
    return engine_helper.get_running_sessions()

def get_endpoint(session_id):
    return engine_helper.get_endpoint(session_id)

def get_engine_state(session_id):
    return engine_helper.get_engine_mode(session_id)

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

def set_engine_id(id):
    engine_helper.set_engine_id(id)

def get_engine_id():
    return engine_helper.get_engine_id()

def reset_network(session_id):
    cm.set_network_deinitialized(session_id)


if __name__ == '__main__':
    user_id = "shankar"
    network_id = "n001"
    session_id = user_id + "!" + network_id + "!none"

    import base64
    import json

    encoded_session_id = base64.b64encode(bytes(session_id, "utf-8")).decode('ascii')
    # c2hhbmthciFuMDAxIW5vbmU=

    sample_input = {"i001": ["i001"]}

    start_training(encoded_session_id)

    # import time
    # time.sleep(1)
    # run_network(encoded_session_id, json.dumps(sample_input))

    #
    # sample_input = {"i001": ["i003"]}
    # run_network(encoded_session_id, json.dumps(sample_input))
    # print(get_output(encoded_session_id))
