import json
import logging

from athom.common.net import post
from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomAPISessionError

log = logging.getLogger(__name__)

class Token:

    def __init__(self, athom, **kwargs):
        self._access_token = kwargs.get('access_token', None)
        self.expires_in = kwargs.get('expires_in', -1)
        self.token_type = kwargs.get('token_type', 'bearer')
        self.refresh_token = kwargs.get('refresh_token', None)

        self.athom = athom


    @property
    def access_token(self):
        if self._access_token is None:
            raise AthomAPISessionError()

        return self._access_token


    @access_token.setter
    def access_token(self, token):
        self._access_token = token


    def jsonify(self):
        columns = ['access_token', 'expires_in', 'token_type', 'refresh_token']
        return {k:getattr(self, k) for k in columns}


    def refresh(self):
        url = "https://api.athom.com/oauth2/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.athom.clientId,
            'client_secret': self.athom.clientSecret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        try:
            log.info("Refreshing token")
            r = post(url, data=data, headers=headers, refresh=False)

        except AthomCloudAuthenticationError:
            self.destroy()
            log.error("OAUTH2 session has expired, required to login again!")
            raise AthomAPISessionError()

        data = json.loads(r)
        for key, value in data.items():
            setattr(self, key, value)

        self.athom.storage.set('token', self.jsonify())


    def destroy(self):
        self._access_token = None
        self.expires_in = -1
        self.token_type = None
        self.refresh_token = None


    def __str__(self):
        """ Standard string representation. Access_token defines Token object
        """
        return self.access_token


    def __bool__(self):
        return self._access_token is not None


    @staticmethod
    def generate_token(athom, json_str):
        token = Token(athom)
        data = json.loads(json_str)

        for key, value in data.items():
            setattr(token, key, value)

        return token
