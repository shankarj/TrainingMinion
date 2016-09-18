__author__ = 'shankar'

import json


def json_to_dict(inp_json):
    from Core.utils import output_util as oa
    json_obj = json.loads(inp_json)
    final_obj = {}

    if json_obj:
        for key in json_obj:
            # if isinstance(json_obj[key], unicode):
            #     final_obj[key] = json_obj[key].encode('utf-8')
            # else:
            try:
                final_obj[key] = json_to_dict(json_obj[key])
            except Exception as ex:
                final_obj[key] = json_obj[key]
    else:
        oa.write_verbose_msg("Not a valid JSON.")
        return None

    return final_obj