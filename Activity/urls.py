from django.conf.urls import patterns, url

urlpatterns = patterns('Activity.views',
                       url(r'^mine$', 'activity_mine', name="mine"),
                       url(r'^create$', 'activity_create', name='create'),
                       url(r'^applied$', 'activity_applied', name='applied'),
                       url(r'^discover$', 'activity_discover', name='discover'),
                       url(r'^(?P<act_id>\d+)$', 'activity_detail', name='detail'),
                       url(r'^(?P<act_id>\d+)/comments$', 'activity_detail_comment', name='detail_comment'),
                       url(r'^(?P<act_id>\d+)/post_comment$', 'post_activity_comment', name='comment')
                       )
