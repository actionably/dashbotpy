from __future__ import print_function

import json
import logging
import os

import requests

from .version import __version__


class Generic():
    def __init__(self, api_key, debug=False, print_errors=False):
        domain = os.environ.get('DASHBOT_SERVER_ROOT', 'https://tracker.dashbot.io')
        url_root = '{domain}/track'.format(domain=domain)
        url = '{url_root}?apiKey={api_key}&type={{}}&platform={platform}&v={version}-{source}'
        self.api_key = api_key
        self.url = url.format(**{
            'url_root': url_root,
            'api_key': api_key,
            'platform': type(self).__name__,
            'version': __version__,
            'source': 'pip',
        })
        self.print_errors = print_errors
        self.debug = debug

    def _load_data(self, **kwargs):
        return json.loads(**kwargs['data'])

    def _make_request(self, url, method, json):
        try:
            if method == 'GET':
                r = requests.get(url, params=json)
            elif method == 'POST':
                r = requests.post(url, json=json)
            else:
                print('Error in _make_request, unsupported method')
            if self.debug:
                print('dashbot response')
                print(r.text)
            if r.status_code != 200:
                logging.error(
                    "ERROR: occurred sending data. "
                    "Non 200 response from server: {code}".format(code=r.status_code)
                )
        except ValueError as e:
            logging.error("ERROR: occurred sending data. Exception: {e}".format(e=e))

    def log_incoming(self, **kwargs):
        url = self.url.format('incoming')
        data = self._load_data(**kwargs)

        if self.debug:
            print('Dashbot Incoming:' + url)
            print(json.dumps(data))

        self._make_request(url, 'POST', data)

    def log_outgoing(self, **kwargs):
        url = self.url.format('outcoming')
        data = self._load_data(**kwargs)

        if self.debug:
            print('Dashbot Outgoing:' + url)
            print(json.dumps(data))

        self._make_request(url, 'POST', data)
