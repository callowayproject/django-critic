"""
django-critic: urls
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('critic.views',

    url(r'^add/$',
        'add_rating',
        name='add_rating'),
        
    url(r'^render/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'render_rating',
        name='rating_render'),
        
    url(r'^user_rating/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'user_rating_json',
        name='user_rating_json'),
    
    url(r'^data/(?P<content_type_id>\d+)/(?P<object_id>\d+)/(?P<option>.*)/$',
        'rating_data_json',
        name='rating_data_json_by_option'),
        
    url(r'^data/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
        'rating_data_json',
        name='rating_data_json'),
)
    