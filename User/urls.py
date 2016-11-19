from django.conf.urls import patterns, url

from .views import ProfileOperation

urlpatterns = patterns('User.views',
                       url(r'^register$', 'account_register', name='register'),
                       url(r'^sendcode$', 'account_send_code', name='send_code'),
                       url(r'^login$', 'account_login', name='login'),
                       url(r'^profile$', 'account_set_profile', name="set_profile"),
                       url(r'^logout$', 'account_logout', name='logout'),
                       url(r'^reset$', 'account_reset_password', name='reset'),
                       url(r'^modify$', 'profile_modify', name='modify'),
                       url(r'^blacklist$', 'blacklist', name='blacklist'),
                       url(r'^permission', 'permission_sync', name="permission"),
                       url(r'^token', 'update_token', name="token"),
                       url(r'^(?P<user_id>\d+)/status$', 'profile_status_list', name='status'),
                       url(r'^(?P<user_id>\d+)/info$', 'profile_info', name='info'),
                       url(r'^(?P<user_id>\d+)/fans$', 'profile_fans_list', name='fans'),
                       url(r'^(?P<user_id>\d+)/follows$', 'profile_follow_list', name='follows'),
                       url(r'^(?P<user_id>\d+)/operation', ProfileOperation.as_view(), name='operation'),
                       url(r'^(?P<user_id>\d+)/settings', 'profile_chat_settings', name='settings'),
                       url(r'^(?P<user_id>\d+)/authed_cars', 'profile_authed_cars', name='authed_cars'),
                       )
