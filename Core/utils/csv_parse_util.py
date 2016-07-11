__author__ = 'shankar'

import csv


# Every row in file is converted to an array.
# All rows are returned as one big array.
# Basically an array of arrays.
def parse_csv_dump(data_dump):
    from Core.utils import output_util as out
    try:
        data_array = []

        if not data_dump:
            out.write_verbose_msg("engine", 2, "Empty data dump to process in CSV processing.")
            return None

        reader = csv.reader(data_dump.split('\n'), delimiter=',')
        for row in reader:
            data_array.append(row)

        return data_array
    except Exception as ex:
        out.write_verbose_msg("engine", 2, "Error while processing CSV dump." + ex)
        return None
