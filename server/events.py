import json

from rx.concurrency import AsyncIOScheduler
from rx.subjects import Subject

from .messages import error_message
from .socket import connections

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
            try:
                command = json.loads(command_string)
                await events.on_next(Event(connection, command))
            except:
                await connection.send(error_message(f'Failed to pass json: {command_string}'))
        except:
            print('Connection dropped due to an error')
            break


connections.subscribe_on(AsyncIOScheduler()).subscribe(await_events)
