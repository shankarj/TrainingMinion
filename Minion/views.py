import json
from django.http import HttpResponse
from Core import core_api

def index(request, temp_id):
    user_id = "shankar"
    network_id = "n001"
    training_profile_id = "tr001"
    verbose = True
    session_id = user_id + "!" + network_id + "!" + training_profile_id + "!" + str(verbose)

    import base64

    encoded_session_id = base64.b64encode(bytes(session_id, "utf-8")).decode('ascii')

    init_success = core_api.initialize_network(encoded_session_id)

    sample_input = {"i001": ["i001"]}
    status = False
    if init_success:
        import json
        core_api.start_training(encoded_session_id)
        print("Training done.");
        status = core_api.run_network(encoded_session_id, json.dumps(sample_input))

    data = {'status': status, 'output': core_api.get_output(encoded_session_id)}
    return HttpResponse(json.dumps(data), content_type='application/json')