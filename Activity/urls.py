from django.conf.urls import patterns, url
from .views import ActivityOperation

urlpatterns = patterns('Activity.views',
                       url(r'^mine$', 'activity_mine', name="mine"),
                       url(r'^create$', 'activity_create', name='create'),
                       url(r'^applied$', 'activity_applied', name='applied'),
                       url(r'^discover$', 'activity_discover', name='discover'),
                       url(r'^(?P<act_id>\d+)$', 'activity_detail', name='detail'),
                       url(r'^(?P<act_id>\d+)/edit$', 'activity_edit', name='edit'),
                       url(r'^(?P<act_id>\d+)/apply$', 'activity_apply', name='apply'),
                       url(r'^(?P<act_id>\d+)/close$', 'activity_close', name='close'),
                       url(r'^(?P<act_id>\d+)/comments$', 'activity_detail_comment', name='detail_comment'),
                       url(r'^(?P<act_id>\d+)/post_comment$', 'post_activity_comment', name='comment'),
                       url(r'^(?P<act_id>\d+)/operation$', ActivityOperation.as_view(), name='operation'),
                       url(r'^(?P<act_id>\d+)/like_users', 'activity_like_users', name='like_users'),
                       )
