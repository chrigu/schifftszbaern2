# -*- coding: utf-8 -*-

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
          print("twittercon: %s"%rain)
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
