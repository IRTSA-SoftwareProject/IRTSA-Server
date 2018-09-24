import json


def message(name, data):
    """ Returns a message in the form of a dictionary """
    return json.dumps(dict(name=name, data=data))


def error_message(error_description):
    """ Shortcut for creating an error message """
    return message('error', {'message': error_description})
