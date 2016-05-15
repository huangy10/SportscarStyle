from django.conf.urls import patterns, url


urlpatterns = patterns('Sportscar.views',
                       url(r'^type_list$', 'cars_type_list', name='type_list'),
                       url(r'^(?P<car_id>\d+)/detail$', 'cars_detail', name='car_detail'),
                       url(r'^(?P<car_id>\d+)/follow$', 'car_follow', name='car_follow'),
                       url(r'^(?P<car_id>\d+)/delete$', 'car_delete', name='car_delete'),
                       url(r'^(?P<car_id>\d+)/signature$', 'car_update_signature', name='signature'),
                       url(r'^auth$', 'car_auth', name='auth'),
                       url(r'^querybyname$', 'car_query_by_name', name='query')
                       )
