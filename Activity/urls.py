from django.conf.urls import patterns, url

urlpatterns = patterns('Activity.views',
                       url(r'^create/$', 'activity_create', name='create'),
                       url(r'^(?P<act_id>\d+)/$', 'activity_detail', name='detail'),
                       url(r'^(?P<act_id>\d+)/comment$', 'post_activity_comment', name='comment')
                       )
