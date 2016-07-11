import numpy as np

from Core.elements.abstract_element import *
from Core.utils import output_util as out


class LinearPredictorElement(AbstractElement):
    def __init__(self, my_id):
        self.my_id = my_id
        self.props = {}

    def train_forward_pass(self):
        # Multiply features and transpose of weights
        self.props["prediction_val"] = np.matrix(self.props["curr_features"]) * np.matrix(
            self.props["weights"]).transpose()
        out.write_verbose_msg("element", 0, "Prediction value : " + str(self.props["prediction_val"]))

    def train_backward_pass(self):
        # Multiply the weight updates from an error module with the learning rate.
        # And update the current weight values in the props.
        curr_weight_updates = np.multiply(self.props["learning_rate"], self.props["weight_updates"])
        out.write_verbose_msg("element", 0, "Weight updates : " + str(curr_weight_updates))

        self.props["weights"] = np.subtract(self.props["weights"], curr_weight_updates)
        out.write_verbose_msg("element", 0, "New weights : " + str(self.props["weights"]))

    def execute(self):
        # Multiply features and transpose of weights
        self.props["prediction_val"] = np.matrix(self.props["curr_features"]) * np.matrix(
            self.props["weights"]).transpose()
        out.write_verbose_msg("element", 0, "Prediction value : " + str(self.props["prediction_val"]))

    def on_train_done(self):
        pass
