from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from Core import core_api


def trainingsessions(request):
    response_json = {}
    try:
        sessions = core_api.get_training_sessions()
        response_json["status"] = True
        response_json["sessions"] = sessions
    except Exception as e:
        response_json["status"] = False
        response_json["message"] = "Error while obtaining list of training sessions. " + str(e)

    return HttpResponse(json.dumps(response_json), content_type='application/json')


def runningsessions(request):
    response_json = {}
    try:
        sessions = core_api.get_running_sessions()
        response_json["status"] = True
        response_json["sessions"] = sessions
    except Exception as e:
        response_json["status"] = False
        response_json["message"] = "Error while obtaining list of running sessions. " + str(e)

    return HttpResponse(json.dumps(response_json), content_type='application/json')


def statusurl(request, session_id):
    response_json = {}
    try:
        url = core_api.get_endpoint(session_id)
        response_json["status"] = True
        response_json["url"] = url
    except Exception as e:
        response_json["status"] = False
        response_json["message"] = "Error while obtaining status url for " + session_id + ". " + str(e)

    return HttpResponse(json.dumps(response_json), content_type='application/json')

def health(request):
    response_json = {}
    response_json["status"] = True
    response_json["message"] = "Minion running. Status is healthy. Port : " + str(core_api.get_engine_port())
    return HttpResponse(json.dumps(response_json), content_type='application/json')

def state(request, session_id):
    response_json = {}
    try:
        mode = core_api.get_engine_state(session_id)
        response_json["status"] = True
        response_json["state"] = mode
    except Exception as e:
        response_json["status"] = False
        response_json["message"] = "Error while obtaining engine state for " + session_id + ". " + str(e)

    return HttpResponse(json.dumps(response_json), content_type='application/json')


def delete(request, session_id):
    pass


def train(request, session_id):
    response_json = {"status": None}
    if session_id:
        try:
            status, msg = core_api.start_training(session_id)
            response_json["status"] = status
            response_json["endpoint"] = "sample_endpoint"
            response_json[
                "message"] = msg
        except Exception as ex:
            response_json["status"] = "Error"
            response_json["message"] = str(ex)
    else:
        response_json["status"] = "Error"
        response_json["message"] = "Session id not given."

    return HttpResponse(json.dumps(response_json), content_type='application/json')


@csrf_exempt
def run(request, session_id):
    response_json = {"status": None}
    if session_id:
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            status = core_api.run_network(session_id, json.dumps(json_data))
            response_json["status"] = status
            response_json["output"] = core_api.get_output(session_id)
        except Exception as ex:
            response_json["status"] = "Error"
            response_json["message"] = str(ex)
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
