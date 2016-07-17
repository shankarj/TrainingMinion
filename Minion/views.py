from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from Core import core_api

def train(request, session_id):
    response_json = {"status": None}
    if session_id:
        print (session_id)
        status = core_api.start_training(session_id)
        response_json["status"] = status
        response_json["endpoint"] = "sample_endpoint"
        response_json[
            "message"] = "Training request has been initiated. Please connect to the socket endpoint for updates."
    else:
        response_json["status"] = "Error"

    return HttpResponse(json.dumps(response_json), content_type='application/json')

@csrf_exempt
def run(request, session_id):
    response_json = {"status": None}
    if session_id:
        json_data = json.loads(request.body.decode("utf-8"))
        status = core_api.run_network(session_id, json.dumps(json_data))
        response_json["status"] = status
        response_json["output"] = core_api.get_output(session_id)
    else:
        response_json["status"] = "Error"

    return HttpResponse(json.dumps(response_json), content_type='application/json')


if __name__ == "__main__":
    user_id = "shankar"
    network_id = "n001"
    training_profile_id = "tr001"
    verbose = True
    session_id = user_id + "!" + network_id + "!" + training_profile_id + "!" + str(verbose)
    import base64

    encoded_session_id = base64.b64encode(bytes(session_id, "utf-8")).decode('ascii')
    print(encoded_session_id)
