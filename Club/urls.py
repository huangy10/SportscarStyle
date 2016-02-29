from django.conf.urls import patterns, url


urlpatterns = patterns('Club.views',
                       url(r'^create$', 'club_create', name="create"),
                       url(r'^list$', 'club_list', name='list'),
                       )

