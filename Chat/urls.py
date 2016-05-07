from django.conf.urls import patterns, url


urlpatterns = patterns('Chat.views',
                       url(r"^list$", 'chat_list', name="home"),
                       url(r"^history$", 'historical_record', name="history"),
                       url(r"^start", 'start_chat', name="start"),
                       url(r"^unread$", 'unread_chat_message_num', name="unread"),
                       url(r"^unread/sync$", 'read_sync', name="sync"))
