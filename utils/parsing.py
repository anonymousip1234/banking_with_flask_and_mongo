from flask import jsonify
from pydantic import ValidationError



def parse_request(request,schema):
    data = request.get_data()
    if not data:
        return None,jsonify({"message" : "empty request!"})
    json = request.get_json()
    if not json:
        return None,jsonify({"message" : "invalid data"})
    try:
        parsed_data = schema(**json)
        return parsed_data,None
    except ValidationError as e:
        errors = e.errors()
        return None,errors
    

def serialize_data_lists(data_list,schema):
    try:
        serialized_data_lists = [schema(**data).model_dump() for data in data_list]
    except ValidationError as e:
        return jsonify({"errors" : e.errors()}),400


    return jsonify({"serialized_list" : serialized_data_lists}),201