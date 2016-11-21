from django.conf.urls import url, patterns

urlpatterns = patterns('Status.views',
                       url('^list$', 'status_list', name='status_list'),
                       url('^post$', 'post_new_status', name='post_status'),
                       url('^(?P<status_id>\d+)$', 'status_detail', name='detail'),
                       url('^(?P<status_id>\d+)/comments$', 'status_comments', name='status_comments'),
                       url('^(?P<status_id>\d+)/post_comments$', 'status_post_comment', name='post_comments'),
                       url('^(?P<status_id>\d+)/operation$', 'status_operation', name='status_operation'),
                       url('^(?P<status_id>\d+)/like_users', 'status_like_users', name='like_users')
                       )
