from django.conf.urls import url, patterns


urlpatterns = patterns('SettingCenter.views',
                       url(r'^settings$', 'settings', name='settings'),
                       url(r'^suggestions$', 'give_suggestions', name='suggestions'))
