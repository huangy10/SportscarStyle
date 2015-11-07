from django.conf.urls import patterns, url


urlpatterns = patterns('News.views',
                       url(r'^/$', 'news_list', name='news_list'),
                       url(r'^(?P<news_id>\d+)$', 'news_detail', name='news_detail'),
                       url(r'^(?P<news_id>\d+)/comments$', 'news_comments_list', name='comments_list'),
                       url(r'^(?P<news_id>\d+)/post_comments$', 'news_post_comment', name='post_comment'),
                       url(r'^(?P<news_id>\d+)/operation$', 'news_operation', name='news_operation'),
                       )
