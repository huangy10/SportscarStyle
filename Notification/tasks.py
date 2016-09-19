import os
import re
import urllib

from apnsclient import *
import OpenSSL
from tornado.httpclient import HTTPClient

from SportscarStyle.celery import app
from django.contrib.auth.models import User
from .redis_operation import UnreadUtil
from custom.utils import get_logger

OpenSSL.SSL.SSLv3_METHOD = OpenSSL.SSL.TLSv1_METHOD

session = Session()
logger = get_logger(__name__)


@app.task()
def push_notification(user, tokens, badge_incr, message_body, type="", data=None, callback=None):
    """ push notification to the user
    """
    print user
    if not user.setting_center.notification_accept:
        print "user not accept notifications"
        return
    if type not in ["chat", "notif"]:
        logger.warn("Invalid notification type")
        return
    if tokens is None or len(tokens) == 0:
        return
    if type == "chat":
        if badge_incr > 0:
            badge = UnreadUtil.incr(user.id)
        else:
            badge = UnreadUtil.get(user.id)
    else:
        if badge_incr > 0:
            badge = UnreadUtil.incr(user.id)
        else:
            badge = UnreadUtil.get(user.id)

    if user.setting_center.notification_sound:
        message = Message(tokens, alert=message_body, badge=badge, sound="default")
    else:
        message = Message(tokens, alert=message_body, badge=badge)

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


@app.task()
def clear_notification_unread_num(user):
    """ clear the notification unread number
    """
    UnreadUtil.clear(user.id)


def convert_camel_to_under_dash(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@app.task()
def send_notification_handler(sender, target, display_mode, extra_info="", **kwargs):
    from .models import Notification

    create_params = dict(
        display_mode=display_mode,
        target=target,
        extra_info=extra_info,
        sender_class_name=sender.__name__,
        related_user=kwargs.get("related_user", None),
        related_act=kwargs.get("related_act", None),
        related_act_invite=kwargs.get("related_act_invite", None),
        related_act_join=kwargs.get("related_act_join", None),
        related_act_comment=kwargs.get("related_act_comment", None),
        related_club=kwargs.get("related_club", None),
        related_status=kwargs.get("related_status", None),
        related_status_comment=kwargs.get("related_status_comment", None),
        related_news=kwargs.get("related_news", None),
        related_news_comment=kwargs.get("related_news_comment", None),
        related_own=kwargs.get("related_own", None)
    )

    try:
        notif, _ = Notification.objects.get_or_create(**create_params)
    except Exception, e:
        logger.error(u'-------->Fail to create Notification')
        logger.error(u'the error info is %s' % e)
        # re-throw the exception, let it crash
        raise e

    client = HTTPClient()
    client.fetch(
        "http://localhost:8887/notification/internal", method="POST",
        body=urllib.urlencode({"id": notif.id})
    )

    client.close()

