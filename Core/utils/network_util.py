__author__ = 'shankar'

from Core.enums.network_call_type import NetworkCallType as nctype
from Core.globals import service_global
from Core.wrappers import config_manager as conf
import os
import Core.dataset as dataset
import requests


def network_call(call_type, **args):
    from Core.utils import output_util as out
    from Core.utils import json_util

    if isinstance(call_type, nctype):
        core_endpoint = conf.get_config_value("core_endpoint")
        try:
            if call_type == nctype.download_dataset:
                file_path = os.path.dirname(dataset.__file__)
                the_file = open(file_path + "/" + args["file_name"]).read()
                return the_file
            elif call_type == nctype.get_dataset_prop:
                if input_validate(args, call_type):
                    url = core_endpoint + "/dataset/properties/" + args["dataset_id"]
                    resp = requests.get(url)
                    if not resp.status_code == 200:
                        out.write_verbose_msg(args["sess_id"], "engine", 100,
                                              "Error while getting dataset properties for id : " + args[
                                                  "sess_id"] + ". Returned non 200")

                    return json_util.json_to_dict(resp.content.decode("utf-8"))
                else:
                    raise Exception("Input to get dataset properties not valid.")
            elif call_type == nctype.get_training_profile:
                if input_validate(args, call_type):
                    url = core_endpoint + "/training/profile/" + args["profile_id"]
                    resp = requests.get(url)
                    if not resp.status_code == 200:
                        out.write_verbose_msg(args["sess_id"], "engine", 100,
                                              "Error while getting training profile for id : " + args[
                                                  "sess_id"] + ". Returned non 200")

                    return json_util.json_to_dict(resp.content.decode("utf-8"))
                else:
                    raise Exception("Input to get dataset properties not valid.")
            elif call_type == nctype.get_network_structure:
                if input_validate(args, call_type):
                    url = core_endpoint + "/projects/structure/" + args["project_id"]
                    resp = requests.get(url)
                    if not resp.status_code == 200:
                        out.write_verbose_msg(args["sess_id"], "engine", 100,
                                              "Error while getting network structure for id : " + args[
                                                  "sess_id"] + ". Returned non 200")

                    return json_util.json_to_dict(resp.content.decode("utf-8"))
                else:
                    raise Exception("Input to get network structure not valid.")
            elif call_type == nctype.get_network_settings:
                if input_validate(args, call_type):
                    url = core_endpoint + "/projects/settings/" + args["project_id"]
                    resp = requests.get(url)
                    if not resp.status_code == 200:
                        out.write_verbose_msg(args["sess_id"], "engine", 100,
                                              "Error while getting network settings for id : " + args[
                                                  "sess_id"] + ". Returned non 200")
                    return json_util.json_to_dict(resp.content.decode("utf-8"))
                else:
                    raise Exception("Input to get network settings not valid.")
            elif call_type == nctype.notify_training_done:
                leader_endpoint = conf.get_config_value("leader_endpoint")
                if leader_endpoint is not None:
                    url = leader_endpoint + "/api/training/notifydone/"

                    if (input_validate(args, call_type)):
                        data = {"sessionid": args["sess_id"],
                                "minionid": service_global.my_id,
                                "project_name": args["project_name"],
                                "parent_id": args["parent_id"],
                                "network_structure": args["structure"],
                                "network_conns": args["conns"],
                                "create_new_snapshot": args["create_new_snapshot"],
                                "training_success": args["training_result"]}

                        resp = requests.post(url, json=data)
                        if not resp.status_code == 200:
                            out.write_verbose_msg(args["sess_id"], "engine", 100,
                                                  "Error while notifying training done for id : " + args[
                                                      "sess_id"] + ". Returned non 200")
                    else:
                        raise Exception("Invalid input to notifydone.")
                else:
                    raise Exception("Leader endpoint not found.")
        except Exception as ex:
            out.write_verbose_msg(args["sess_id"], "engine", 100,
                                  "Error while notifying training done for id : " + args["sess_id"] + ". " + str(ex))
            return None

    else:
        print ("Type of input not the correct enum")
        return None


def input_validate(args, call_type):
    if call_type == nctype.notify_training_done:
        if "sess_id" in args and "project_name" in args and "parent_id" in args and "structure" in args and "conns" in args and "create_new_snapshot" in args and "training_result" in args:
            return True
        else:
            return false
    elif call_type == nctype.get_dataset_prop:
        if "sess_id" in args and "dataset_id" in args:
            return True
        else:
            return False
    elif call_type == nctype.get_network_structure or call_type == nctype.get_network_settings:
        if "sess_id" in args and "project_id" in args:
            return True
        else:
            return False

