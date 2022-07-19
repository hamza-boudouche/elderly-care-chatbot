from ast import Str
from typing import Tuple
import jwt
import requests
import json
from time import time
import os
from dotenv import load_dotenv

load_dotenv()

# your API key and your API secret
API_KEY = os.getenv('API_KEY')
API_SEC = os.getenv('API_SEC')

# create a function to generate a token
# using the pyjwt library


def generateToken():
    token = jwt.encode(

        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},

        # Secret used to generate token signature
        API_SEC,

        # Specify the hashing alg
        algorithm='HS256'
    )
    return token.decode('utf-8')


# send a request with headers including
# a token and meeting details


def createMeeting(title: str, time: str, duration: str) -> Tuple[str, str]:
    # create json data for post requests
    meetingdetails = {
        "topic": title,
        "type": 2,
        "start_time": time,
        "duration": duration,
        "timezone": "Africa/Casablanca",
                    "agenda": "test",

                    "recurrence": {
                        "type": 1,
                        "repeat_interval": 1
                    },
        "settings":
        {
                        "host_video": "true",
                        "participant_video": "true",
                        "join_before_host": "False",
                        "mute_upon_entry": "False",
                        "watermark": "true",
                        "audio": "voip",
                        "auto_recording": "cloud"
                    }
    }

    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json'
    }
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails)
    )

    print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]

    return (join_URL, meetingPassword)
