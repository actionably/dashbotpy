import time

from .generic import Generic


class Alexa(Generic):
    def _load_data(**kwargs):
        data = {
            'dashbot_timestamp': int(time.time() * 1000),
            'event': kwargs['event'],
        }
        if 'response' in kwargs:
            data['response'] = kwargs['response']

        return data
