import numpy as np

from Core.elements.abstract_element import *


class SquaredErrorElement(AbstractElement):
	def __init__(self, my_id):
		self.my_id = my_id
		self.props = {
			"weight_updates": np.zeros(2),
			"squared_error": [],
			"cost_vals": [],
			"prediction_val": 0.0,
			"curr_features": [],
			"curr_expected_vals": 0.0,
			"training_data_size": []
		}

	def train_forward_pass(self):
		# Gradient part of the formula
		err_val = self.props["prediction_val"] - self.props["curr_expected_vals"]
		np_err_gradient = np.array([err_val] * len(self.props["curr_features"]))
		self.props["weight_updates"] += self.props["curr_features"] * np_err_gradient

		# Add the current example's squared error.
		# Mean is calculated when backward pass starts and pushed into cost_vals.
		err_sq = err_val ** 2
		self.props["squared_error"].append(err_sq)

	def train_backward_pass(self):
		# Calculate squared cost values and push it to cost_vals to be
		# marked for output during forward pass.
		# We can observe that the first finish of forward pass will have no
		# cost_vals in the output.
		self.props["cost_vals"].append(sum(self.props["squared_error"])/(2.0 *  self.props["training_data_size"]))

		# Notify engine that training backward pass is completenetwork_conns
		# Backward pass for this module passes the calculated weight_updates to
		# the next module in the backward flow.
		self.props["weight_updates"] = np.true_divide(self.props["weight_updates"], self.props["training_data_size"])

	def execute(self, **args):
		pass

	def on_train_done(self):
		pass