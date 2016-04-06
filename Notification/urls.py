from django.conf.urls import patterns, url


urlpatterns = patterns('Notification.views',
                       url(r'^$', 'notification_list', name="list"),
                       url(r'^clear$', 'notification_clear', name="clear"),
                       url(r'^(?P<notif_id>\d+)$', 'notification_mark_read', name="mark_read")
                       )
