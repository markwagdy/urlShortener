from django.http import JsonResponse, HttpResponse
from .const_general import APPLICATION_JSON_UTF8,ALLOW_ORIGIN

def success(message):
    body = {
        "data": message,
    }
    response = JsonResponse(body)
    response[ALLOW_ORIGIN] = "*"
    return response

def badrequest(message):
    return JsonResponse(
        {"message": message},
        status=400,
        content_type=APPLICATION_JSON_UTF8
    )

def notfound(message):
    return JsonResponse(
        {"message": message},
        status=404,
        content_type=APPLICATION_JSON_UTF8
    )

def servererror(message):
    return JsonResponse(
        {"message": message},
        status=500,
        content_type=APPLICATION_JSON_UTF8
    )
