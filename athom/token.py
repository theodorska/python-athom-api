import json

class Token:

    def __init__(self, athom, access_token=None, expires_in=-1, token_type="bearer", refresh_token=None):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.refresh_token = refresh_token

        self.athom = athom


    def jsonify(self):
        columns = ['access_token', 'expires_in', 'token_type', 'refresh_token']
        return {k:v for k,v in self.__dict__.items() if k in columns}


    @staticmethod
    def generate_token(athom, json_str):
        token = Token(athom)
        data = json.loads(json_str)

        for key, value in data.items():
            setattr(token, key, value)

        return token
