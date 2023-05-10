import base64
import os
import pyotp
import requests

from datetime import datetime
from urllib.parse import parse_qs, urlparse

current_directory = os.path.dirname(os.path.realpath(__file__))

data_path = os.path.join(current_directory, "data")
data_file = datetime.now().strftime("%Y-%m-%d")
fyers_access_token_path = os.path.join(data_path, data_file)

log_path = os.path.join(current_directory, "logs")


class FyersTokenManager:
    def __init__(self, config, accessToken, fyersModel, ws):
        self.username = config["username"]
        self.totp_key = config["totp_key"]
        self.pin = config["pin"]
        self.client_id = config["client_id"]
        self.secret_key = config["secret_key"]
        self.redirect_uri = config["redirect_uri"]

        self.__accessToken = accessToken
        self.__fyersModel = fyersModel
        self.__ws = ws

        self.__generate_folders_if_not_exists()
        self.__initialize()

    def __generate_folders_if_not_exists(self):
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

    def __set_initial_values(self, token):
        self.http_access_token = token

        self.ws_access_token = f"{self.client_id}:{self.http_access_token}"

        self.http_client = self.__fyersModel.FyersModel(
            client_id=self.client_id, token=token, log_path=log_path
        )

        self.ws_client = self.__ws.FyersSocket(
            access_token=self.ws_access_token, run_background=False, log_path=log_path
        )

    def __initialize(self):
        try:
            token = self.__read_file()
            self.__set_initial_values(token)
        except FileNotFoundError:
            token = self.__setup()
            self.__set_initial_values(token)

    def __read_file(self):
        with open(f"{fyers_access_token_path}", "r") as f:
            token = f.read()

        return token

    def __write_file(self, token):
        with open(f"{fyers_access_token_path}", "w") as f:
            f.write(token)

    def __get_token(self):
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        s = requests.Session()
        s.headers.update(headers)

        data1 = f'{{"fy_id":"{base64.b64encode(f"{self.username}".encode()).decode()}","app_id":"2"}}'
        r1 = s.post("https://api-t2.fyers.in/vagator/v2/send_login_otp_v2", data=data1)
        assert r1.status_code == 200, f"Error in r1:\n {r1.json()}"

        request_key = r1.json()["request_key"]
        data2 = (
            f'{{"request_key":"{request_key}","otp":{pyotp.TOTP(self.totp_key).now()}}}'
        )
        r2 = s.post("https://api-t2.fyers.in/vagator/v2/verify_otp", data=data2)
        assert r2.status_code == 200, f"Error in r2:\n {r2.text}"

        request_key = r2.json()["request_key"]
        data3 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{base64.b64encode(f"{self.pin}".encode()).decode()}"}}'
        r3 = s.post("https://api-t2.fyers.in/vagator/v2/verify_pin_v2", data=data3)
        assert r3.status_code == 200, f"Error in r3:\n {r3.json()}"

        headers = {
            "authorization": f"Bearer {r3.json()['data']['access_token']}",
            "content-type": "application/json; charset=UTF-8",
        }
        data4 = f'{{"fyers_id":"{self.username}","app_id":"{self.client_id[:-4]}","redirect_uri":"{self.redirect_uri}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
        r4 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data4)
        assert r4.status_code == 308, f"Error in r4:\n {r4.json()}"

        parsed = urlparse(r4.json()["Url"])
        auth_code = parse_qs(parsed.query)["auth_code"][0]

        session = self.__accessToken.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            grant_type="authorization_code",
        )

        session.set_token(auth_code)
        response = session.generate_token()

        return response["access_token"]

    def __setup(self):
        token = self.__get_token()
        self.__write_file(token)

        return token
