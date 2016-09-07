__author__ = 'shankar'

from enum import Enum

class NetworkCallType(Enum):
    download_dataset = 0
    get_dataset_prop = 1
    get_training_profile = 2
    get_network_structure = 3
    get_network_settings = 4
    notify_training_done = 5