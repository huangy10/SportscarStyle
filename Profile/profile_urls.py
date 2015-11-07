from django.conf.urls import patterns, url


urlpatterns = patterns('Profile.views',
                       url(r'^/(?P<user_id>\d+)/info$', 'profile_info', name='profile_info'),
                       url(r'^/(?P<user_id>\d+)/status', 'profile_status_list', name='status_list'),
                       url(r'^/modify', 'profile_modify', name='modify'),
                       )
