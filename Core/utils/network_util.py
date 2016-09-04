__author__ = 'shankar'

from Core.enums.network_call_type import NetworkCallType as nctype
from Core.globals import service_global
import os
import Core.dataset as dataset
import requests

def network_call(call_type, **args):
    from Core.utils import output_util as out

    if isinstance(call_type, nctype):
        if call_type == nctype.download_dataset:
            file_path = os.path.dirname(dataset.__file__)
            the_file = open(file_path + "/sample_training_data_1.csv").read()
            return the_file
        elif call_type == nctype.get_dataset_prop:
            file_path = os.path.dirname(dataset.__file__)
            the_file = open(file_path + "/sample_dataset_prop_1.json").read()
            from Core.utils import json_util
            return json_util.json_to_dict(the_file)
        elif call_type == nctype.get_training_profile:
            file_path = os.path.dirname(dataset.__file__)
            the_file = open(file_path + "/sample_training_profile.json").read()
            from Core.utils import json_util
            return json_util.json_to_dict(the_file)
        elif call_type == nctype.get_network_structure:
            file_path = os.path.dirname(dataset.__file__)
            the_file = open(file_path + "/sample_structure.json").read()
            from Core.utils import json_util
            return json_util.json_to_dict(the_file)
        elif call_type == nctype.get_network_context:
            file_path = os.path.dirname(dataset.__file__)
            the_file = open(file_path + "/sample_context.json").read()
            from Core.utils import json_util
            return json_util.json_to_dict(the_file)
        elif call_type == nctype.notify_training_done:
            headers = {'content-type': 'application/json'}
            url = "http://localhost:8081/api/training/notifydone/"
            data = {"sessionid" : args["sess_id"], "minionid": service_global.my_id}
            resp = requests.post(url, json=data)
            if not resp.status_code == 200:
                out.write_verbose_msg(session_id, "engine", 100, "Error while notifying training done for id : " + args["sess_id"])

    else:
        print ("Type of input not the correct enum")
