import json
import logging
import azure.functions as func


def main(event: func.EventHubEvent):
    event_json = event.get_body().decode('utf-8')
    event_item = json.loads(event_json)

    return json.dumps({
        'target': 'newDeviceMessage',
        'arguments': [ event_item ]
    })