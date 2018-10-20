"""A set of utility functions for creating messages"""

import json


def message(type, body):
    """ Returns a message in the form of a dictionary """
    return json.dumps(dict(type=type, body=body))


def error_message(error_description):
    """ Shortcut for creating an error message """
    return message('error', {'message': error_description})
