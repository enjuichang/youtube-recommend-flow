from app.configs import config
from app.jwt_utils import Jwt
import hashlib
import requests


class ApiClient:
    def __init__(self):
        self.brus_users_me_url = "{}/api/users/me".format(config['BRUS_SERVER_URL'])

    def _get_jwt_headers(self, brain_user_id):
        jwt_token = Jwt.encode(dict(user_id=brain_user_id))
        return {"Authorization": "Bearer {}".format(jwt_token)}

    def get_brain_user_token(self, brain_user_id):
        headers = self._get_jwt_headers(brain_user_id)
        res = requests.get(self.brus_users_me_url, headers=headers)
        if res.status_code == 200:
            return res.json().get("auth_token", {}).get("key")
        else:
            # TODO: raise BrainException
            return None

    def get_users_roles(self, brain_user_id):
        headers = self._get_jwt_headers(brain_user_id)
        res = requests.get(self.brus_users_me_url, headers=headers)
        if res.status_code == 200:
            user_roles = res.json().get("roles", [])
            return user_roles
        else:
            # TODO: raise BrainException
            return None


class Pubsub(ApiClient):
    def __init__(self):
        super(self, Pubsub).__init__()
        self.topic_format = "/{app_name}/{user_id}/{user_token_hashed}/{suffix}"
        self.pubsub_url = "{}/publish".format(config['PUBSUB_SERVER_URL'])

    def websocket_publish(self, app_name, brain_user_id, topic_suffix, redis_key, redis_data):
        user_token = self.get_brain_user_token(brain_user_id)
        if not user_token:
            return False
        user_token_hashed = hashlib.sha256(user_token.encode('utf-8')).hexdigest()
        topic = self.topic_format.format(app_name=app_name, user_id=brain_user_id, user_token_hashed=user_token_hashed, suffix=topic_suffix)
        post_data = {
            "redis": {
                "key": redis_key,
                "data": redis_data,
            },
            "channel": {"topic": topic, "name": "websockets"}
        }
        headers = {"content-type": "application/json"}
        if config['ENVIRONMENT'] == "development":
            headers["Authorization"] = "token {}".format(config['BRUS_AUTH_TOKEN'])
        res = requests.post(self.pubsub_url, json=post_data, headers=headers)
        if res.status_code == 200:
            return True
        else:
            # TODO: raise BrainException
            return False
