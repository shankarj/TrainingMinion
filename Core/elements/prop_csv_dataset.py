from Core.elements.abstract_property_element import *
from Core.utils import dataset_parser as parser
from Core.utils import output_util as out
from Core.utils import network_util as nu
from Core.enums.network_call_type import NetworkCallType as nctype

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
                try:
                    # Download the training dataset
                    out.write_verbose_msg(self.props["_session_id"], "element", 0,
                                          "From " + self.my_id + ". Downloading dataset : " + self.props["file_name"])
                    training_data = nu.network_call(nctype.download_dataset, file_name=self.props["file_name"])
                    file_path = self.props["_session_path"] + "/" + self.props[
                        "_session_id"] + "/data/" + self.props["file_name"] + ".csv"
                    data_file = open(file_path, "w+")
                    data_file.write(training_data)
                    data_file.close()

                    # Read and parse the training data and represent them in-memory
                    # to continue with the training process.
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
