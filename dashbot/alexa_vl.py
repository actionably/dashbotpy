from .alexa import Alexa


class AlexaVL(Alexa):
    def __init__(self, api_key=None, debug=False, print_errors=False):
        super(self).__init__()
        self.source = 'pip_vl'

    # VL initialize
    def initialize(self, api_key, session):
        self.api_key = api_key
        self.session = session

    # VL track
    def track(self, intent_request, response):
        event = self.regenerate_event(intent_request)
        self.log_incoming(event)
        self.log_outgoing(event, response)

    # VL helper
    def regenerate_event(self, intent_request):
        event = {
            'session': self.session,
            'request': intent_request,
            'context': {
                'System': {
                    'application': self.session['application'],
                    'user': self.session['user']
                }
            }
        }
        return event

    # VL helper
    def generate_response(self, speech_text):
        if speech_text[0:7] == '<speak>':
            output_speech = {
                'type': 'SSML',
                'ssml': speech_text,
            }

        else:
            output_speech = {
                'text': speech_text,
                'type': 'Plaintext',
            }

        return {
            'response': {
                'outputSpeech': output_speech
            }
        }
