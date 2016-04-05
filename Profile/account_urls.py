from django.conf.urls import patterns, url


urlpatterns = patterns('Profile.views',
                       url(r'^login$', 'account_login', name='login'),
                       url(r'^sendcode$', 'account_send_code', name='send_code'),
                       url(r'^reset$', 'account_reset_password', name='reset'),
                       url(r'^register$', 'account_register', name='register'),
                       url(r'^profile$', 'account_profile', name='profile'),
                       url(r'^logout$', 'account_logout', name='logout')
                       )
