import numpy as np

from Core.elements.abstract_element import *
from Core.utils import output_util as out


class SimpleForwarderElement(AbstractElement):
    def __init__(self, my_id):
        self.my_id = my_id
        self.props = {
            "prop1": "",
            "prop2": 0,
            "_type": "element"
        }

    def init_element(self):
        return True

    def train_forward_pass(self):
        self.props["prop1"].append(self.my_id)
        self.props["prop2"] += 1
        print("FROM : " + self.my_id + ". " + str(self.props["prop1"]))

        return True

    def train_backward_pass(self):
        self.props["prop1"].append(self.my_id)
        print("FROM : " + self.my_id + ". " + str(self.props["prop1"]))
        return True

    def execute(self):
        self.props["prop1"].append(self.my_id)
        print("FROM : " + self.my_id + ". " + str(self.props["prop1"]))
        print("FROM : " + self.my_id + ". PROP 2 VAL : " + str(self.props["prop2"]))
        return True

    def on_train_done(self):
        pass
