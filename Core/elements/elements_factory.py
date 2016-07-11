__author__ = 'shankar'

import importlib
from Core.utils import output_util as out

def create_object(session_id, elem_id, elem_file_name):
    if not elem_id or not elem_file_name:
        out.write_verbose_msg(session_id, "engine", 2, "create_object arguments can't be null.")
        return None

    elem_obj = None

    try:
        elem_obj_file = importlib.import_module('Core.elements.' + elem_file_name)

        # Expecting sample format : input_csv (or) element_simple_forwarder
        # which converts to InputCsvElement and SimpleForwarderElement
        first_index = elem_file_name.index("_")
        suffix = "_" + elem_file_name[0:first_index+1]
        class_name = elem_file_name[first_index+1:len(elem_file_name)] + suffix
        class_name = class_name.replace("_"," ")
        class_name = class_name.title()
        class_name = class_name.replace(" ", "")
        class_obj = getattr(elem_obj_file, class_name)

        if not class_obj:
            out.write_verbose_msg(session_id, "engine", 2, "No such element : " + elem_file_name + " exists in local database.")
            return None
        else:
            elem_obj = class_obj(elem_id)
            out.write_verbose_msg(session_id, "engine", 0, "Created new object for element " + elem_file_name + " with id : " + elem_id)
    except Exception as e:
        out.write_verbose_msg(session_id, "engine", 2, "No such element : " + elem_file_name + " exists in local database.")

    return elem_obj

