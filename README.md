```
config = {
  "username": "<USERNAME>",
  "totp_key": "<TOTP_KEY>",
  "pin": "<PIN>",
  "client_id": "<CLIENT_ID>",
  "secret_key": "<SECRET_KEY>",
  "redirect_uri": <REDIRECT_URL>
}
```

## Install

```
pip install fyers-token-manager-v2
```

## Fyers Token Generator

```
from fyers_api import accessToken, fyersModel
from fyers_api.Websocket import ws

from fyers_token_manager_v2 import FyersTokenManager
```

#### Initialization

```
fyersTokenManager = FyersTokenManager(config, accessToken, fyersModel, ws)

print(fyersTokenManager.http_access_token)
print(fyersTokenManager.ws_access_token)
```

#### HTTP Client

- fyersTokenManager.http_client.get_profile()

#### WebSocket Client

- fyersTokenManager.ws_client.subscribe(payload)
