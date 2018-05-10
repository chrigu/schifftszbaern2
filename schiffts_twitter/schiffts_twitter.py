# -*- coding: utf-8 -*-
from datetime import datetime

import twitter
import random
import settings


def do_twitter(rain):
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.ACCESS_TOKEN,
                      access_token_secret=settings.ACCESS_TOKEN_SECRET)

    print(api.VerifyCredentials())

    tried = []
    for i in range(0, 5):
        try:
            if rain:
                message = random.choice(settings.RAIN_MESSAGES)
            else:
                message = random.choice(settings.NO_RAIN_MESSAGES)

            if message in tried:
                continue

            api.PostUpdate(message)
            break

        except Exception as e:
            print(e)
            tried.append(message)
            pass


# todo: move twitter api code elsewhere

def tweet_prediction(next_hit):
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.ACCESS_TOKEN,
                      access_token_secret=settings.ACCESS_TOKEN_SECRET)

    try:
        send_tweet("delta:{}, s:{}".format(datetime.strftime(next_hit.timestamp, "%H%M"), next_hit.size),
                   api=api)
    except:
        pass

    return True


def send_tweet(message, api=None):
    return api.PostUpdate(message)
