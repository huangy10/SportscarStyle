from django.conf.urls import patterns, url


urlpatterns = patterns('Club.views',
                       url(r'^create$', 'club_create', name="create"),
                       url(r'^list$', 'club_list', name='list'),
                       url(r'^discover$', 'club_discover', name='discover'),
                       url(r'^(?P<club_id>\d+)/info$', 'club_infos', name="info"),
                       url(r'^(?P<club_id>\d+)/update$', 'update_club_settings', name="update"),
                       url(r'^(?P<club_id>\d+)/members$', 'club_member_change', name="members_update"),
                       url(r'^(?P<club_id>\d+)/auth$', 'club_auth', name="auth"),
                       url(r'^(?P<club_id>\d+)/quit$', 'club_quit', name="auth"),
                       url(r'^(?P<club_id>\d+)/apply', 'club_apply', name="apply"),
                       url(r'^(?P<club_id>\d+)/operation', 'club_operation', name="operation"),
                       url(r'^billboard$', 'club_billboard', name='billboard')
                       )

