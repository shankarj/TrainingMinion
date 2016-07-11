from Core.elements.abstract_property_element import *
from Core.utils import dataset_parser as parser
from Core.utils import output_util as out


class CsvDatasetProp(AbstractPropertyElement):
    def __init__(self, my_id):
        self.my_id = my_id
        self.props = {
            "_type": "prop",
            "file_name": None,
            "data": None,
            "curr_data": None,
            "curr_row_index": None
        }

    def init_element(self):
        method_success = False

        if not self.props["file_name"] is None:
            if self.props["data"] is None:
                # Read and parse the training data from local directory if present. Represent them in-memory
                # to continue with the training process.
                try:
                    file_path = self.props["_session_path"] + "/" + self.props[
                        "_session_id"] + "/data/" + self.props["file_name"] + ".csv"
                    training_data = open(file_path).read()
                    self.props["data"] = parser.parse_data(training_data, "csv")
                    method_success = True
                except Exception as ex:
                    out.write_verbose_msg(self.props["_session_id"], "element", 2,
                                          "Error while loading dataset. " + str(ex))

        return method_success

    def get_prop_val(self, prop_name):
        if prop_name == "curr_data":
            self.props["curr_data"] = self.props["data"][self.props["curr_row_index"]]
            return self.props["curr_data"]

    def set_prop_val(self, prop_name, prop_val):
        self.props[prop_name] = prop_val
