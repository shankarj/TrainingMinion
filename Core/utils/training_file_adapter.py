__author__ = 'shankar'

from Core.utils import network_util as nu
from Core.globals import service_global
from Core.enums.network_call_type import NetworkCallType as nctype
from Core.utils import output_util as out
from Core.wrappers import ns_wrapper as ns


def download_training_profile(session_id, training_profile_id):
    download_success = False
    try:
        training_profile = nu.network_call(nctype.get_training_profile, sess_id=session_id, profile_id=training_profile_id)

        if training_profile is not None:
            # Load it to the memory
            training_profile["profile_id"] = training_profile_id
            service_global.running_sessions[session_id]["training_profile"] = training_profile

            out.persist_training_profile(session_id, training_profile)
            download_success = True
        else:
            raise Exception("Empty training profile returned.")
    except Exception as ex:
        out.write_verbose_msg("Error : Failed downloading training profile. " + ex)

    return download_success


# Downloads the dataset and it's properties.
def download_training_data(session_id):
    from Core.utils import output_util as out
    download_success = False
    tdset_ids = ns.get_input_elem_list(session_id)

    if tdset_ids:
        all_success = True
        for tdset_id in tdset_ids:
            try:
                # Get properties and the actual data
                dataset_prop = nu.network_call(nctype.get_dataset_prop, sess_id=session_id, dataset_id=tdset_id)
                training_data = nu.network_call(nctype.download_dataset, sess_id=session_id, dataset_id=tdset_id)

                if training_data is not None and dataset_prop is not None:
                    service_global.running_sessions[session_id]["training_data"][tdset_id] = {}
                    service_global.running_sessions[session_id]["training_data"][tdset_id]["prop"] = dataset_prop
                else:
                    out.write_verbose_msg("engine", 2, "Network call to get training data/prop returned null")
                    all_success = False

                # Write it the json file to persist.
                persist_success = out.persist_training_data(session_id, tdset_id, training_data,
                                                            service_global.running_sessions[session_id][
                                                                "training_data"][tdset_id]["prop"])

                if not persist_success:
                    out.write_verbose_msg(session_id, "engine", 2, "Persist failed for training prop.")
                    all_success = False
                    break
            except Exception as ex:
                out.write_verbose_msg(session_id, "engine", 2,
                                      "Error : Failed downloading dataset " + tdset_id + ". " + str(ex))
                all_success = False
                return False

        if all_success:
            download_success = True
    else:
        out.write_verbose_msg(session_id, "engine", 2, "Failed getting dataset ids.")

    return download_success
