__author__ = 'shankar'

from Core.enums.network_call_type import NetworkCallType as nctype
import os
import Core.dataset as dataset

def network_call(call_type, **args):
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
    else:
        print ("Type of input not the correct enum")
