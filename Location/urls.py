from django.conf.urls import patterns, url


urlpatterns = patterns('Location.views',
                       url(r'^update$', 'radar_user_location_udpate', name="update"),
                       url(r'^nearby$', 'radar_cars', name="home"),
                       url(r'^(?P<user_id>\d+)/track', 'track_user', name="track"))
