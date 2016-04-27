from django.conf.urls import patterns, url

urlpatterns = patterns('User.views',
                       url(r'^register$', 'account_register', name='register'),
                       url(r'^sendcode$', 'account_send_code', name='send_code'),
                       url(r'^login$', 'account_login', name='login'),
                       url(r'^logout$', 'account_logout', name='logout'),
                       url(r'^reset$', 'account_reset_password', name='reset')
                       )
