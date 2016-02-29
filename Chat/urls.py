from django.conf.urls import patterns, url


urlpatterns = patterns('Chat.views',
                       url(r"^list$", 'chat_list', name="home"),
                       url(r"^history$", 'historical_record', name="history"))
