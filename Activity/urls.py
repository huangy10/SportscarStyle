from django.conf.urls import patterns, url

urlpatterns = patterns('Activity.views',
                       url(r'^create/$', 'activity_create', name='create'),
                       )