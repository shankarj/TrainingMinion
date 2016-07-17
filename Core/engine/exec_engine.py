from Core.wrappers import engine_helper as eh
from Core.wrappers import context_manager as cm
from Core.wrappers import training_helper as th
from Core.wrappers import session_manager as sm
from Core.utils import training_file_adapter as tfa
from Core.utils import json_util as ju
from Core.utils import output_util as out
from Core.utils import general_utils as gu
from Core.wrappers import ns_wrapper as ns


# Prepares the network for execution by downloading network structure and connections.
# Downloads the datasets as well.
def init_engine(session_id):
    init_success = False

    # Set engine as init because we don't want to serve any requests even while init
    # is running
    cm.set_engine_init(session_id)

    # Get the session variables
    session_variables = gu.get_session_variables(session_id)

    # Set verbose option
    if session_variables["verbose"]:
        cm.set_verbose_mode(session_id)

    # Create the session variables and set the context variables for the
    # network for the given session id
    out.write_verbose_msg(session_id, "engine", 0, "Creating the network session.")
    status_one = sm.create_session(session_id)

    # Download and init the network structure
    out.write_verbose_msg(session_id, "engine", 0, "Downloading network structure")
    status_two = ns.download_structure(session_id, session_variables["network_id"])

    if status_one and status_two:
        # Load configs and reset config variables
        out.write_verbose_msg(session_id, "engine", 0, "Setting engine properties.")
        cm.set_network_deinitialized(session_id)
        cm.set_training_not_done(session_id)

        # Load training data if available
        training_check_success = False
        if cm.needs_training(session_id):
            profile_id = cm.get_training_profile_id(session_id)

            if profile_id:
                profile_status = tfa.download_training_profile(session_id, session_variables["training_profile_id"])
                dataset_status = tfa.download_training_data(session_id)

                if profile_status and dataset_status:
                    training_check_success = True
                else:
                    out.write_verbose_msg(session_id, "engine", 2, "Profile or dataset not downloaded.")
            else:
                out.write_verbose_msg(session_id, "engine", 2, "Training profile id not set.")
        else:
            # If training is not needed, we assign training checks are done.
            training_check_success = True

        # Initialize the network elements and connections if everything looks good.
        # Creates PyObjects for all the elements
        # Runs init as well of all elements for it's properties (static value assigning)
        if training_check_success:
            create_status = eh.create_init_network(session_id)

            if create_status:
                init_success = True
                cm.set_network_initialized(session_id)
            else:
                out.write_verbose_msg(session_id, "engine", 2, "Network init failed.")
    else:
        out.write_verbose_msg(session_id, "engine", 2, "Network structure download failed. Exiting.")

    cm.set_engine_stopped(session_id)
    return init_success

def train_network(session_id):
    training_success = False
    init_done = True

    # Check if init is done already or kick init process.
    if not cm.is_network_initialized(session_id):
        init_done = init_engine(session_id)

    if init_done:
        # Set the mode to be training
        cm.set_engine_training(session_id)

        if cm.needs_training(session_id):
            out.write_verbose_msg(session_id, "element", 0, "Network initialized. Init engine for training.")
            cm.set_training_not_done(session_id)

            # Loop until training is not finished.
            # One loop does one iteration (set of forward and one backward pass).
            out.write_verbose_msg(session_id, "element", 0, "Starting training.")
            while not cm.is_training_done(session_id):
                if not cm.is_engine_paused(session_id):
                    # Start the forward pass.
                    out.write_verbose_msg(session_id, "engine", 0, "Engine running. Forward pass.")
                    forward_pass_success = eh.execute_forward_pass(session_id, None)

                    if not forward_pass_success:
                        break

                    # Check if current batch size limit reached.
                    # If reached then start backward pass by resetting curr batch size and
                    # change training direction also.
                    if th.is_batch_full(session_id):
                        out.write_verbose_msg(session_id, "engine", 0, "Batch full. Backward pass.")
                        eh.execute_backward_pass(session_id)

                        # If we reach the end of the dataset, increase the curr_epoch count
                        # by 1. If curr_epoch count equals total epochs then assign training
                        # to be done.
                        if th.all_epochs_done(session_id):
                            out.write_verbose_msg(session_id, "engine", 0, "Epochs done. Training over.")
                            cm.set_training_done(session_id)

            # Set engine to be idle if training is done.
            if cm.is_training_done(session_id):
                out.write_verbose_msg(session_id, "engine", 0, "Engine stopped.")
                cm.set_engine_stopped(session_id)
                training_success = True
            else:
                out.write_verbose_msg(session_id, "engine", 2, "Training exited before completing.")
        else:
            out.write_verbose_msg(session_id, "element", 1,
                                  "Network initialized. Settings indicate NO training needed.")
    else:
        out.write_verbose_msg(session_id, "element", 2, "Error while initializing network for id : " + session_id)

    cm.set_engine_stopped(session_id)
    return training_success


def run_network(session_id, inp):
    run_success = False

    # Set the mode to be executing
    cm.set_engine_executing(session_id)

    network_trained = False
    if cm.is_network_initialized(session_id):
        # Check if training is done (if needed). Otherwise assume training is done
        if cm.needs_training(session_id):
            if cm.is_training_done(session_id):
                network_trained = True
        else:
            network_trained = True

        if network_trained:
            out.write_verbose_msg(session_id, "element", 0, "Network initialized. Reading the input.")
            inp_dict = ju.json_to_dict(inp)

            if inp_dict:
                out.write_verbose_msg(session_id, "element", 0, "Input parsed. Starting engine.")
                cm.set_engine_executing(session_id)

                # Actual forward pass call
                if not eh.execute_forward_pass(session_id, inp_dict):
                    out.write_verbose_msg(session_id, "element", 2, "Execution failure. Exiting")

                run_success = True
    else:
        out.write_verbose_msg(session_id, "element", 2, "Network not initialized before running.")

    cm.set_engine_stopped(session_id)
    return run_success