from django.conf.urls import patterns, url


urlpatterns = patterns('Club.views',
                       url(r'^create$', 'club_create', name="create"),
                       url(r'^list$', 'club_list', name='list'),
                       url(r'^discover$', 'club_discover', name='discover'),
                       url(r'^(?P<club_id>\d+)/info$', 'club_infos', name="info"),
                       url(r'^(?P<club_id>\d+)/update$', 'update_club_settings', name="update"),
                       url(r'^(?P<club_id>\d+)/members$', 'club_member_change', name="members_update"),
                       )

