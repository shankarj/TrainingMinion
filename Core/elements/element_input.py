__author__ = 'shankar'

from Core.elements.abstract_element import *
from Core.elements.abstract_property_element import *
from Core.utils import output_util as out


class InputElement(AbstractElement):
    def __init__(self, my_id):
        self.my_id = my_id
        self.props = {
            "_type": "input",
            "dataset": None,
            "curr_data": None
        }
        self.prop_interface = {
            "dataset": ["data", "curr_row_index"]
        }

    def init_element(self):
        init_success = False
        if isinstance(self.props["dataset"], AbstractPropertyElement):
            self.props["dataset"].set_prop_val("file_name", self.my_id)

            if self.props["dataset"].init_element():
                init_success = True

        return init_success

    def train_forward_pass(self):
        if isinstance(self.props["dataset"], AbstractPropertyElement):
            self.props["dataset"].set_prop_val("curr_row_index", self.props["curr_row_index"])
            self.props["curr_data"] = self.props["dataset"].get_prop_val("curr_data")
        else:
            self.props["curr_data"] = self.props["dataset"][self.props["curr_row_index"]]

        return True

    def train_backward_pass(self):
        pass

    def execute(self):
        return True

    def on_train_done(self):
        pass

    def get_prop_interfaces(self):
        return self.prop_interface
