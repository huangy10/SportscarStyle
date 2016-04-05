import logging
import os
import sys
from apnsclient import *
import OpenSSL

from SportscarStyle.celery import app
from django.contrib.auth.models import User
import redis_operation as my_redis

OpenSSL.SSL.SSLv3_METHOD = OpenSSL.SSL.TLSv1_METHOD

session = Session()
logger = logging.getLogger(__name__)


@app.task()
def push_notification(user, tokens, badge_incr, message_body, data=None):
    """ push notification to the user
    """
    if tokens is None or len(tokens) == 0:
        return
    badge = my_redis.incr(user.id, badge_incr)
    message = Message(tokens, alert=message_body, badge=badge, sound="default")
    con = session.get_connection(
        "push_sandbox", cert_file=os.path.abspath(os.path.join(__file__, os.pardir, "data", "sportcar.pem")))
    srv = APNs(con)
    try:
        res = srv.send(message)
    except Exception, e:
        logger.warn(u"Fail to push notification to {0}, error info: {1}".format(user, e))
    else:
        for token, reason in res.failed.items():
            code, errmsg = reason
            logger.warn(u"Device failed: {0}, reason: {1}".format(token, errmsg))

        for code, errmsg in res.errors:
            logger.warn("Error: {}".format(errmsg))

        if res.needs_retry():
            retry_message = res.retry()
            logger.debug("Retry sending message to {0}, message: {1}".format(user, retry_message))

