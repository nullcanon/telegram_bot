import httpx
import json


params = {'contract_addresses':'0xE070ccA5cdFB3F2B434fB91eAF67FA2084f324D7',
           'api-key':'',
           'api-secrect:':''}
result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)

print(result.text)


class goplusHelper:
    def __init__(self):
        pass

    def getTokenInfo(self, token):
        params = {'api-key':'',
           'api-secrect:':''}
        params["contract_addresses"] = token
        result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)
        return json.load(result.text)

