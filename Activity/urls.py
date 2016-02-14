from django.conf.urls import patterns, url

urlpatterns = patterns('Activity.views',
                       url(r'^mine$', 'activity_mine', name="mine"),
                       url(r'^create/$', 'activity_create', name='create'),
                       url(r'^discover$', 'activity_discover', name='discover'),
                       url(r'^(?P<act_id>\d+)/$', 'activity_detail', name='detail'),
                       url(r'^(?P<act_id>\d+)/comment$', 'post_activity_comment', name='comment')
                       )
