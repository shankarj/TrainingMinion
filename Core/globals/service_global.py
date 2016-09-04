__author_ = "shankar"

import Core.globals as global_files
import os

# Minion id
my_id = ""

# Minion port
my_port = 0000

# PyObjects of elements in Network structure stored in this dictionary.
# Wrapper for operations on this : elements_manager.py
elements_obj_dict = {}

# Session ids of the networks that are currently being trained.
training_sessions = []

# Global variables for the engine. Following vars are stored for each session:
# 1. context_props
# 2. network_conns
# 3. network_structure
# 4. training_data
# 5. training_profile
running_sessions = {

}

# Path where the global json files are stored
globals_path = os.path.dirname(global_files.__file__)
