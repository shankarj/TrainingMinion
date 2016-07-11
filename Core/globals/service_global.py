__author_ = "shankar"

from Core.utils import json_util as ju
import Core.globals as global_files

import os

# PyObjects of elements in Network structure stored in this dictionary.
# Wrapper for operations on this : elements_manager.py
elements_obj_dict = {}

# Global variables for the engine
running_sessions = {

}

# Path where the global json files are stored
globals_path = os.path.dirname(global_files.__file__)
