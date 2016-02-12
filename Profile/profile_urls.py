from django.conf.urls import patterns, url


urlpatterns = patterns('Profile.views',
                       url(r'^(?P<user_id>\d+)/info$', 'profile_info', name='profile_info'),
                       url(r'^(?P<user_id>\d+)/status', 'profile_status_list', name='status_list'),
                       url(r'^modify', 'profile_modify', name='modify'),
                       url(r'^(?P<user_id>\d+)/fans', 'profile_fans_list', name='fans'),
                       url(r'^(?P<user_id>\d+)/follows', 'profile_follow_list', name='follows'),
                       url(r'^(?P<user_id>\d+)/operation', 'profile_operation', name='operation'),
                       url(r'^(?P<user_id>\d+)/authed_cars', 'profile_authed_cars', name='authed_cars'),
                       url(r'^(?P<target_id>\d+)/settings', 'profile_chat_settings', name='chat_settings'),
                       url(r'^blacklist/update', 'profile_black_list_update', name='blacklist_update'),
                       url(r'^blacklist', 'profile_black_list', name='blacklist'),
                       )
