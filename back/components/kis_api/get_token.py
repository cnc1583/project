import requests
import time
import redis
import json
from back.infrastructure.config.kis_config import kis_settings

redis_client = redis.Redis(host="localhost", port=6379, db=0)
TOKEN_KEY = "kis_access_token"

"""KIS TOKEN ISSUANCE"""
def get_token():

    cached = redis_client.get(TOKEN_KEY)
    if cached:
        token_data = json.loads(cached)
        if token_data["expires_in"] > int(time.time()):
            return token_data["access_token"]

    base = "https://openapi.koreainvestment.com:9443"
    url = f"{base}/oauth2/tokenP"

    data = {
        "grant_type": "client_credentials",
        "appkey": kis_settings.KIS_API_CLIENT_ID,
        "appsecret": kis_settings.KIS_API_CLIENT_SECRET
    }

    res = requests.post(url, json=data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return None

    token_data = res.json()
    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 86400)

    redis_client.set(TOKEN_KEY, json.dumps({"access_token": access_token, "expires_in": int(time.time()) + expires_in - 30}))

    return access_token
