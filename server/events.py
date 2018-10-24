"""This module manages the parsing of client messages.
To access the events, you can subcribe to the events Subject.
"""
import asyncio
import json
import traceback

from rx.subjects import Subject

from .messages import error_message

events = Subject()


class Event:
    """ The class that represents all messages from clients """
    def __init__(self, connection, message):
        self.connection = connection
        self.message = message


def of_type(message_type):
    """ Returns a filter function that will only pass messages of a certain type """
    return lambda event: event.message['type'] == message_type


async def await_events(connection):
    """ Listens for all messages from new connections and creates an event for them """
    while True:
        try:
            command_string = await connection.recv()
            print('Received message', command_string)
            try:
                command = json.loads(command_string)
                events.on_next(Event(connection, command))
            except json.decoder.JSONDecodeError as json_exception:
                print('Failed to pass json', json_exception)
                await connection.send(error_message(f'Failed to pass json: {command_string}'))
            except:
                print('Unknown error')
                traceback.print_exc()
        except Exception as exception:
            print('Connection dropped due to an error', exception)
            break


def via_asyncio(fn):
    """ Returns a lambda that calls an async fn on the main event loop """
    return lambda event: asyncio.ensure_future(fn(event))
