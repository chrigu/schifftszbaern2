# -*- coding: utf-8 -*-
import logging
from graphql.graphql import save_hit, get_last_hit
from radar.forecast import find_cell_index_in_history
from schiffts_twitter.schiffts_twitter import tweet_prediction
from dateutil.parser import parse
from datetime import  datetime
from push import send_push

TIME_THRESHOLD = 45

# create logger
module_logger = logging.getLogger('schiffts.hit')


def _is_new_hit(old_hit, forecast):
    return not old_hit or not find_cell_index_in_history(forecast['hit_history'], old_hit)


def _last_hit_not_relevant(last_hit):
    timedelta_to_now = datetime.now() - parse(last_hit['createdAt'])
    return timedelta_to_now.seconds > TIME_THRESHOLD * 60


def _has_no_last_hit(last_hit):
    return len(last_hit) == 0


def handle_new_hit(forecast):

    if not forecast['next_hit']:
        module_logger.info("No hit")
        return

    module_logger.info("next hitdelta:{}, s:{}".format(datetime.strftime(forecast['next_hit'].timestamp,
                                                                         "%H%M"), forecast['next_hit'].size))
    save_hit(forecast['next_hit'])
    last_hits = get_last_hit()

    if not _has_no_last_hit(last_hits):
        module_logger.info("Has no last hits")
        return

    if _last_hit_not_relevant(last_hits[0]):
        module_logger.info("Has no relevant hit")
        return

    module_logger.info("Sending push")
    send_push()
    tweet_prediction(forecast['next_hit'])

    #check cratedAt to now
    #if > 45min since last push