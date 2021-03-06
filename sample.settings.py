# -*- coding: utf-8 -*-

# General
DEBUG = True
DATE_FORMAT = "%Y%m%d%H%M00"

# Radar

## Berne, Baby, Berne!
X_LOCATION = 364
Y_LOCATION = 366

# Twitter

## Schiffts

# update messages used for twitter
RAIN_MESSAGES = ["S'schifft.", "Es schifft.", "Es rägnet.", "S'rägnet.", "Räge Rägetröpfli...", "Wieder eis nass.",
                 "Nassi Sach dusse."]
NO_RAIN_MESSAGES = ["S'schifft nümme.", "Es schifft nümme.", "Es rägnet nümme.", "S'rägnet nümme.",
                    "Es isch wieder troche."]
SNOW_MESSAGES = ["S'schneit.", "Es schneit.", "Wieder eis Schnee.", "Es schneielet.", "S'schneielet"]
NO_SNOW_MESSAGES = ["S'schneit nümme.", "Es schneit nümme.", "Wieder troche.", "Es isch wieder troche"]

CONSUMER_KEY = 'consumer-key'
CONSUMER_SECRET = 'consumer-secret'
ACCESS_TOKEN = 'access-token'
ACCESS_TOKEN_SECRET ='token-secret'

TWEET_SCHIFFTS = False

# Code for smn measurement location
SMN_CITY_NAME = "Bern"

# GraphQL
GRAPH_COOL_ENDPOINT = 'https://api.graph.cool/simple/v1/__PROJECT_ID__'
GRAPH_COOL_TOKEN = 'TOKEN'

# OneSignal
ONESIGNAL_APP_ID = 'app_id'
ONESIGNAL_APP_REST_KEY = 'app_key'

# S3
SAVE_TO_S3 = True
S3_BUCKET = 'mybucket.ch'
S3_ACCESS_ID = 'MYKEY'
S3_ACCESS_SECRET = 'MYSECRET'