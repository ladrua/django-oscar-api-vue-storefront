import requests
import json
from rest_framework.response import Response

def elastic_result(self, request):

    path = request.META['PATH_INFO'].partition("catalog")[2]
    fullpath = 'http://db.local:9200' + path
    
    if request.method == "POST":
        requestdata = json.loads(request.body)
        r = requests.post(fullpath, json=requestdata)

    if request.method == "GET":
        r = requests.get(fullpath)
    
    items = r.json()
    return Response(items)
