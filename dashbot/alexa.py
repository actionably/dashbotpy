import time

from .generic import Generic


class Alexa(Generic):
    def _load_data(**kwargs):
        event = kwargs['request_envelope'].to_dict()
        event['request']['timestamp'] = event['request']['timestamp'].isoformat()
        data = {
            'dashbot_timestamp': int(time.time() * 1000),
            'event': event,
        }
        if 'response' in kwargs:
            data['response'] = kwargs['response'].to_dict()

        return data
