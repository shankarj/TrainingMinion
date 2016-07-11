__author__ = 'shankar'

from Core.utils import csv_parse_util as csv_util


def parse_data(data_dump, data_type):
    from Core.utils import output_util as out
    processed_data = None

    if data_type == "csv":
        processed_data = csv_util.parse_csv_dump(data_dump)

    if processed_data is None:
        out.write_verbose_msg("engine", 2, "Error in parsing training data")

    return processed_data
