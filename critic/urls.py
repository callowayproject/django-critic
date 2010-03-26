from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('critic.views',
    url(r'^(?P<instance_id>\d+)/(?P<option_id>\d+)/(?P<content_type_id>\d+)/(?P<object_id>.*)/vote/$', 
        'make_vote', 
        name='c_make_vote'),
    url(r'^(?P<instance_id>\d+)/(?P<content_type_id>\d+)/(?P<object_id>.*)/data/', 
        'json_data', 
        name='c_data')
)
    