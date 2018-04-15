# -*- coding: utf-8 -*-
import requests
import json
import settings

MESSAGE = "Achtung es chunnt öppis"


def send_push():
    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic {}".format(settings.ONESIGNAL_APP_REST_KEY)}

    payload = {"app_id": settings.ONESIGNAL_APP_ID,
               "included_segments": ["All"],
               "contents": {"en": MESSAGE, "de": MESSAGE, "fr": MESSAGE}}

    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    print(req.status_code, req.reason)