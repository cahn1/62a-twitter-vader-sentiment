#https://datascienceparichay.com/article/get-data-from-twitter-api-in-python-step-by-step-guide/

import os
import requests
from requests.exceptions import RequestException
import logging
from common.log_handler import LogHandler

component = 'twitter_api'
bearer_token = os.environ.get('bearer_token', '')


class Twitter:
    def __init__(self, txid=''):
        super().__init__()
        self.log_handle = LogHandler(f'{component}:{txid}').logger
        self.extra = {}
        self.log = logging.LoggerAdapter(self.log_handle, self.extra)
        self.search_url = 'https://api.twitter.com/2/tweets/search/recent'

    # Inject bearer auth token to header
    @staticmethod
    def bearer_oauth():
        return {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'v2RecentSearchPython'
        }

    # Submit a request to url
    def submit(self, params, tid=''):
        try:
            r = requests.get(self.search_url, headers=self.bearer_oauth(),
                             params=params, timeout=120)
        except RequestException as e:
            self.log.error(f'Request Error: {e}. tid: {tid}')
            return ''
        if r.status_code in range(200, 300):
            if r.json().get('errors', []):
                return []
        else:
            msg = f'Request Error, status code {r.status_code}, ' \
                  f'tid: {tid}'
            raise Exception(msg+f'response {r.text}')
        return r.json()
