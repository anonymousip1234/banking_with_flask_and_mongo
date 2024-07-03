from flask import jsonify
from pydantic import ValidationError



def parse_request(request,schema):
    data = request.get_data()
    if not data:
        return None,jsonify({"message" : "empty request!"}),400
    json = request.get_json()
    if not json:
        return None,jsonify({"message" : "invalid data"}),400
    try:
        parsed_data = schema(**json)
        return parsed_data,None
    except ValidationError as e:
        errors = e.errors()
        return None,errors